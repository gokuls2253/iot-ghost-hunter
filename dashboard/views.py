from django.shortcuts import render
from network.models import Device, ScanLog
import json

def index(request):
    # 1. Device Inventory
    devices = Device.objects.all().order_by('-last_seen')
    active_devices = devices.filter(is_active=True).count()
    
    # 2. Historical Data for Graph (Last 10 Scans)
    # We reverse the order so the oldest is on the left, newest on right
    logs = ScanLog.objects.order_by('-timestamp')[:10]
    logs = reversed(logs) 
    
    # Prepare data arrays for Chart.js
    labels = []
    data_points = []
    
    for log in logs:
        # Format time as HH:MM
        labels.append(log.timestamp.strftime("%H:%M"))
        data_points.append(log.devices_online)

    context = {
        'devices': devices,
        'active_devices': active_devices,
        'total_devices': devices.count(),
        # Pass data as JSON strings so JS can read them safely
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data_points),
    }
    
    return render(request, 'dashboard/index.html', context)