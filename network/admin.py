from django.contrib import admin
from .models import Device, ScanLog

# Register your models here.
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('mac_address', 'ip_address', 'vendor', 'alias', 'is_active', 'last_seen')
    search_fields = ('mac_address', 'ip_address', 'alias', 'vendor')
    list_filter = ('is_active', 'is_trusted', 'vendor')

@admin.register(ScanLog)
class ScanLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'devices_online')
    readonly_fields = ('timestamp',)