from django.template.loader import render_to_string

def createNetworkXML(dictObj):
	return render_to_string('libvirt/network.xml',dictObj)
