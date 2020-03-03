import logging
from common.constants import *
from common.common import *

logger = logging.getLogger()

class Endpoint:
	def __init__(self, name, obj_api, opr_store, spec=None):
		self.name = name
		self.obj_api = obj_api
		self.store = opr_store
		# Initial values all none
		self.vpc = ""
		self.net = ""
		self.vni = ""
		self.status = ""
		self.gw = ""
		self.ip = ""
		self.prefix = ""
		self.mac = ""
		self.type = ""
		self.droplet = ""
		self.droplet_ip = ""
		self.droplet_mac = ""
		self.veth_peer = ""
		self.veth_name = ""
		self.netns = ""
		self.container_id = ""
		self.local_id = ""
		self.veth_index = ""
		self.veth_peer_index = ""
		self.mac = ""
		self.veth_peer_mac = ""
		self.bouncers = set()
		if spec is not None:
			self.set_obj_spec(spec)

		# Misc obj
		# self.droplet_obj = None

	def get_obj_spec(self):
		self.obj = {
				"type": self.type,
				"status": self.status,
				"vpc": self.vpc,
				"net": self.net,
				"ip": self.ip,
				"gw": self.gw,
				"mac": self.mac,
				"vni": self.vni,
				"droplet": self.droplet,
				"prefix": self.prefix,
				"itf": self.veth_name,
				"veth": self.veth_peer,
				"netns": self.netns,
				"hostip": self.droplet_ip,
				"hostmac": self.droplet_mac
		}

		return self.obj

	def set_obj_spec(self, spec):
		self.type = get_spec_val('type', spec)
		self.status = get_spec_val('status', spec)
		self.vpc = get_spec_val('vpc', spec)
		self.net = get_spec_val('net', spec)
		self.ip = get_spec_val('ip', spec)
		self.gw = get_spec_val('gw', spec)
		self.mac = get_spec_val('mac', spec)
		self.vni = get_spec_val('vni', spec)
		self.droplet = get_spec_val('droplet', spec)
		self.prefix = get_spec_val('prefix', spec)
		self.veth_name = get_spec_val('itf', spec)
		self.veth_peer = get_spec_val('veth', spec)
		self.netns = get_spec_val('netns', spec)
		self.droplet_ip = get_spec_val('hostip', spec)
		self.droplet_mac = get_spec_val('hostip', spec)

	def get_name(self):
		return self.name

	def get_plural(self):
		return "endpoints"

	def get_kind(self):
		return "Endpoint"

	def store_update_obj(self):
		if self.store is None:
			return
		self.store.update_ep(self)

	def store_delete_obj(self):
		if self.store is None:
			return
		self.store.delete_ep(self.name)

	# K8s APIs
	def create_obj(self):
		return kube_create_obj(self)

	def update_obj(self):
		return kube_update_obj(self)

	def delete_obj(self):
		return kube_delete_obj(self)

	def watch_obj(self, watch_callback):
		return kube_watch_obj(self, watch_callback)

	# Setters
	def set_vpc(self, vpc):
		self.vpc = vpc

	def set_net(self, net):
		self.net = net

	def set_vni(self, vni):
		self.vni = vni

	def set_status(self, status):
		self.status = status

	def set_gw(self, gw):
		self.gw = gw

	def set_ip(self, ip):
		self.ip = ip

	def set_prefix(self, prefix):
		self.prefix = prefix

	def set_mac(self, mac):
		self.mac = mac

	def set_type(self, eptype):
		self.type = eptype

	def set_droplet(self, droplet):
		self.droplet = droplet

	def set_droplet_ip(self, droplet_ip):
		self.droplet_ip = droplet_ip

	def set_droplet_mac(self, droplet_mac):
		self.droplet_mac = droplet_mac

	def set_droplet_obj(self, droplet_obj):
		self.droplet_obj = droplet_obj

	def set_veth_peer(self, veth_peer):
		self.veth_peer = veth_peer

	def set_veth_name(self, veth_name):
		self.veth_name = veth_name

	def set_netns(self, netns):
		self.netns = netns

	def set_container_id(self, container_id):
		self.container_id = container_id

	def set_local_id(self, local_id):
		self.local_id = local_id

	def set_veth_index(self, veth_index):
		self.veth_index = veth_index

	def set_veth_peer_index(self, veth_peer_index):
		self.veth_peer_index = veth_peer_index

	def set_veth_peer_mac(self, veth_peer_mac):
		self.veth_peer_mac = veth_peer_mac

	def add_bouncer(self, b):
		self.bouncers.add(b)

	def update_md(self):
		pass

############
	def update_object(self):
		body = self.obj_api.get_namespaced_custom_object(
			group="mizar.com",
			version="v1",
			namespace="default",
			plural="endpoints",
			name=self.name)
		body['spec'] = self.get_obj_spec()
		logger.info("updating Endpont {}".format(self.name))
		self.obj_api.patch_namespaced_custom_object(
			group="mizar.com",
			version="v1",
			namespace="default",
			plural="endpoints",
			name=self.name,
			body=body,
		)
		logger.info("updated endpint {}".format(self.name))


	def get_veth_peer(self):
		return self.veth_peer

	def get_veth_name(self):
		return self.veth_name

	def get_tunnel_id(self):
		return str(self.vni)

	def get_ip(self):
		return str(self.ip)

	def get_eptype(self):
		if self.type == ep_type_simple:
			return str(CONSTANTS.TRAN_SIMPLE_EP)

	def get_mac(self):
		return str(self.mac)

	def get_remote_ips(self):
		remote_ips = []
		remote_ips = self.droplet_obj and [str(self.droplet_obj.ip)]
		return remote_ips