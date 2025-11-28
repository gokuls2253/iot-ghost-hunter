from django.db import models

# Create your models here.

class Device(models.Model):
    """
    Represents a physical device on the network.
    Identified uniquely by MAC address.
    """
    mac_address = models.CharField(max_length=17, unique=True, help_text="Physical MAC Address (e.g., 00:1A:2B:3C:4D:5E)")
    ip_address = models.GenericIPAddressField(help_text="Current IP Address")
    host_name = models.CharField(max_length=100, blank=True, null=True, help_text="Resolved Hostname")
    vendor = models.CharField(max_length=100, blank=True, null=True, help_text="Hardware Manufacturer (e.g., Apple, Espressif)")
    
    # Status fields
    is_active = models.BooleanField(default=True, help_text="Is the device currently reachable?")
    last_seen = models.DateTimeField(auto_now=True, help_text="Timestamp of last successful ping")
    
    # User customization
    alias = models.CharField(max_length=50, blank=True, null=True, help_text="User-friendly name (e.g., 'Dad's iPhone')")
    is_trusted = models.BooleanField(default=False, help_text="If True, anomalies from this device are ignored")

    def __str__(self):
        return self.alias or self.host_name or self.mac_address

class ScanLog(models.Model):
    """
    Historical record of a network scan.
    Used for generating time-series graphs on the dashboard.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    devices_online = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Scan at {self.timestamp}: {self.devices_online} devices"