import libvirt, socket

def getHostname(ip_address):
	try:
		hostname = socket.gethostbyaddr(ip_address)
		return hostname[0]
	except:
		return None

def getHypervisorData(ip_address):
	try:
                conn = libvirt.open('qemu+tcp://'+ip_address+'/system')
		return conn.getInfo()
	except:
		return None
