import logging
from kubernetes.client.rest import ApiException

logger = logging.getLogger()

class Vpc(object):
	def __init__(self, obj_api, name, vni, cidr, dividers={}, networks={}):
		self.name = name
		self.vni = vni
		self.cidr = cidr
		self.dividers = dividers
		self.networks = networks
		self.obj_api = obj_api
		self.obj = None

	def get_obj_spec(self):
		self.obj = {
			"ip": self.cidr.ip,
			"prefix": self.cidr.prefixlen,
			"vni": self.vni,
			"dividers": len(self.dividers.keys()),
		}

		return self.obj

	def update_divider(self, droplet):
		logger.info("*Update dividers {}".format(droplet.name))
		if droplet.name in self.dividers:
			return True

		self.dividers[droplet.name] = droplet

		divider_name = self.name +'-divider-' + droplet.name

		try:

			api_response = self.obj_api.get_namespaced_custom_object(
				group="mizar.com",
				version="v1",
				namespace="default",
				plural="dividers",
				name=divider_name)
			logger.info("Exist {}".format(api_response))

		except ApiException as e:
			if e.status == 404:
				divider_obj = {
					"apiVersion": "mizar.com/v1",
					"kind": "Divider",
					"metadata": {
						"name": divider_name
					},
					"spec": {
						"ip": droplet.ip,
						"droplet": droplet.name,
						"vpc": self.name
					}
				}

				# create the divider resource
				self.obj_api.create_namespaced_custom_object(
					group="mizar.com",
					version="v1",
					namespace="default",
					plural="dividers",
					body=divider_obj,
				)
				return True
		finally:
			return False

		return False

	def delete_divider(self, droplet):
		pass

	def update_network(self, network):
		pass

	def delete_network(self, network):
		pass

	def update_bouncer(self, network, bouncer):
		pass

	def delete_bouncer(self, network, bouncer):
		pass

	def update_simple_endpoint(self):
		pass

	def delete_simple_endpoint(self):
		pass

	def update_host_endpoint(self):
		pass

	def delete_host_endpoint(self):
		pass

	def update_scaled_endpoint(self):
		pass

	def delete_scaled_endpoint(self):
		pass