from ui.models import Datacenter, Hypervisor, Network
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin

class DatacenterAdmin(admin.ModelAdmin):
      fieldsets = [
           (None,                {'fields': ['name','address','city','state','zip','country']}),
      ]
      
      list_display = ('name', 'city', 'state','country')

class HypervisorAdmin(admin.ModelAdmin):
      list_display = ('ip_address','hostname','datacenter','arch','memory','cpucount','cpuspeed','public_net','private_net','state')

class NetworkAdmin(admin.ModelAdmin):
      fieldsets = [
          (None,		{'fields': ['hypervisor','name']}),
          ('Forwarding',	{'fields': ['forward_mode']}),
          ('DHCP Config',	{'fields': ['dhcp_ip','dhcp_mask','dhcp_start','dhcp_end']}),
          ('Advanced Bridging', {'fields': ['bridge','bridge_stp','bridge_delay'], 'classes': ['collapse']}),
          ('Advanced VLAN',	{'fields': ['vlan_tag'], 'classes': ['collapse']}),
          ('Advanced QOS', {'fields': ['inbound_avg','inbound_peak','inbound_burst',
					'outbound_avg','outbound_peak','outbound_burst'], 
					'classes': ['collapse']}),
      ]

      list_display = ('name','hypervisor','bridge', 'forward_mode','dhcp_start','dhcp_end','vlan_tag')


admin.site.register(Hypervisor,HypervisorAdmin)
admin.site.register(Datacenter,DatacenterAdmin)
admin.site.register(Network,NetworkAdmin)
