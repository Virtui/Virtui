from django.db import models
import virt, choices, autofield

class Datacenter(models.Model):
    
    #### Field Definitions ####
    name = models.CharField(max_length=16,
                help_text="The name of the site: example Datacenter1")
    uuid = autofield.UUID(editable=False)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2,choices=choices.STATE_CHOICES)
    zip = models.BigIntegerField(max_length=10)
    country = models.CharField(max_length=100, choices=choices.COUNTRY_CHOICES)
    
    #### Define Object as A Field #####
    def __unicode__(self):
        return self.name

class Hypervisor(models.Model):
    
    #### Field Definitions ####
    datacenter = models.ForeignKey(Datacenter)    
    ip_address = models.IPAddressField(help_text='The IP Address of the hypervisor')
    hostname = models.CharField(max_length=100,editable=False,null=True)
    uuid = autofield.UUID(editable=False)
    public_net = models.CharField(max_length=16,
		help_text="The name of the adapter used for public networks: example eth0")
    private_net = models.CharField(max_length=16,
		help_text="The name of the adapter used for private networks: example eth1")
    arch = models.CharField(max_length=16,editable=False,null=True)
    memory = models.BigIntegerField(max_length=16,editable=False,null=True)
    cpucount = models.BigIntegerField(max_length=16,editable=False,null=True)
    cpuspeed = models.BigIntegerField(max_length=16,editable=False,null=True)
    state = models.BooleanField(editable=False)
     
    #### Define Object as A Field #####
    def __unicode__(self):
        return self.ip_address

    #### Trigger Certain Things On Save ####
    def save(self, *args, **kwargs):
	self.hostname = virt.getHostname(self.ip_address)
        hypervisorData = virt.getHypervisorData(self.ip_address)
	if hypervisorData:
		self.state = True
		self.arch = hypervisorData[0]
		self.memory = hypervisorData[1]
		self.cpucount = hypervisorData[2]
		self.cpuspeed = hypervisorData[3]
	else:
		self.state = False
        super(Hypervisor, self).save(*args, **kwargs) # Call the "real" save() method.

class Network(models.Model):
    
    #### Field Definitions ####
    hypervisor = models.ForeignKey(Hypervisor)     
    name = models.CharField(max_length=16,
		help_text="The name of the network")
    uuid = autofield.UUID(editable=False)
    bridge = models.CharField(max_length=16,null=True,blank=True,
		help_text="The name of the bridge to create.  Leave blank for no bridge")
    bridge_stp = models.BooleanField(default=1,
		help_text='Whether spanning tree is enabled on the bridge: default True')
    bridge_delay = models.BigIntegerField(default=0,
		help_text='Bridge forward delay in seconds: default 0')
    bridge_mac = autofield.MAC(editable=False) 
    forward_mode = models.CharField(max_length=16, choices=choices.FORWARD_CHOICES,default="nat",
		help_text="Forwarding mode, for no forwarding select 'isolated': default 'nat'")
    inbound_avg = models.BigIntegerField(null=True,blank=True,
		help_text='Average inbound bit rate on interface being shaped: example 1000')
    inbound_peak = models.BigIntegerField(null=True,blank=True,
		help_text='Maximum inbound bit rate at which bridge can send data: example 5000')
    inbound_burst = models.BigIntegerField(null=True,blank=True,
		help_text='Maximum inbound bytes that can be burst at peak speed: example 5120')
    outbound_avg = models.BigIntegerField(null=True,blank=True,
		help_text='Average outbound bit rate on interface being shaped: example 128')
    outbound_peak = models.BigIntegerField(null=True,blank=True,
		help_text='Maximum outbound bit rate at which bridge can send data: example 256')
    outbound_burst = models.BigIntegerField(null=True,blank=True,
		help_text='Maximum outbound bytes that can be burst at peak speed: example 256')
    dhcp_ip = models.IPAddressField(help_text="The IP Address to assign to the DHCP Server: example 192.168.0.1")
    dhcp_mask = models.IPAddressField(help_text="The subnet mask of the DHCP Server: example 255.255.255.0")
    dhcp_start = models.IPAddressField(help_text="The range start boundary of the DHCP pool: example 192.168.0.100")
    dhcp_end = models.IPAddressField(help_text="The range end boundary of the DHCP pool: example 192.168.0.200")
    vlan_tag = models.BigIntegerField(null=True,blank=True,help_text="The VLAN tag to assign to this network: default 0 (none)")

    #### Define Object as A Field #####
    def __unicode__(self):
        return self.name
