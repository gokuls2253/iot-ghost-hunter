from celery import shared_task
from scapy.all import ARP, Ether, srp
import socket
from django.utils import timezone
from .models import Device, ScanLog
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .ml_engine import GhostBrain

def get_local_subnet():
    """
    Helper to guess the local subnet based on the machine's IP.
    Assumes a standard /24 network (255.255.255.0).
    """
    try:
        # Connect to a public DNS to find our own IP (doesn't actually send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        # Convert 192.168.1.15 -> 192.168.1.0/24
        base_ip = ".".join(local_ip.split('.')[:3]) + ".0/24"
        return base_ip
    except Exception:
        return "192.168.1.0/24" # Fallback default

@shared_task
def scan_network():
    """
    Active ARP Scan using Scapy.
    """
    target_ip = get_local_subnet()
    print(f"[*] Starting ARP scan on {target_ip}...")

    # 1. Create ARP Request
    # Ether(dst="ff:...") = Broadcast to everyone
    # ARP(pdst=target_ip) = "Who has these IPs?"
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    # 2. Send & Receive (srp = Send/Receive Packet at Layer 2)
    # timeout=2: Wait 2 seconds for replies
    # verbose=0: Silence Scapy's own console output
    result = srp(packet, timeout=2, verbose=0)[0]

    # 3. Process Responses
    active_devices = []
    
    for sent, received in result:
        # received.psrc = Source IP
        # received.hwsrc = Source MAC Address
        device_info = {'ip': received.psrc, 'mac': received.hwsrc}
        active_devices.append(device_info)
        
        # 4. Update Database
        # update_or_create checks if MAC exists. 
        # If yes, updates IP/Time. If no, creates new row.
        obj, created = Device.objects.update_or_create(
            mac_address=device_info['mac'],
            defaults={
                'ip_address': device_info['ip'],
                'last_seen': timezone.now(),
                'is_active': True
            }
        )
    
    # 5. Mark missing devices as inactive
    # (Optional logic: if a device wasn't in this scan, set is_active=False)
    current_macs = [d['mac'] for d in active_devices]
    Device.objects.exclude(mac_address__in=current_macs).update(is_active=False)

    # 6. Log the scan
    ScanLog.objects.create(devices_online=len(active_devices))

    # === NEW ML CODE ===
    brain = GhostBrain()
    is_anomaly = bool(brain.check_anomaly(len(active_devices)))
    
    status_msg = "Scan Complete"
    if is_anomaly:
        status_msg = "⚠️ ANOMALY DETECTED ⚠️"
        print(f"!!! GHOST HUNTER ALERT: {len(active_devices)} devices is unusual! !!!")

    # === Broadcast to WebSocket ===
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "dashboard_feed",
        {
            "type": "device_update",
            "message": {
                "status": status_msg,
                "is_anomaly": is_anomaly, # <--- Send the flag
                "count": len(active_devices),
                "devices": active_devices
            }
        }
    )

    return f"Scan Complete. Found {len(active_devices)} devices. Anomaly: {is_anomaly}"