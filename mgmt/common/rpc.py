import json

class TrnRpc:
	def __init__(self, ip, mac, itf='eth0', benchmark = False):
		self.ip = droplet.ip
		self.mac = droplet.mac
		self.itf = droplet.itf

		# transitd cli commands
		self.trn_cli = f'''/trn_bin/transit -s {self.ip} '''
		self.trn_cli_load_transit_xdp = f'''{self.trn_cli} load-transit-xdp -i {self.phy_itf} -j'''
		self.trn_cli_unload_transit_xdp = f'''{self.trn_cli} unload-transit-xdp -i {self.phy_itf} -j'''
		self.trn_cli_update_vpc = f'''{self.trn_cli} update-vpc -i {self.phy_itf} -j'''
		self.trn_cli_get_vpc = f'''{self.trn_cli} get-vpc -i {self.phy_itf} -j'''
		self.trn_cli_delete_vpc = f'''{self.trn_cli} delete-vpc -i {self.phy_itf} -j'''
		self.trn_cli_update_net = f'''{self.trn_cli} update-net -i {self.phy_itf} -j'''
		self.trn_cli_get_net = f'''{self.trn_cli} get-net -i {self.phy_itf} -j'''
		self.trn_cli_delete_net = f'''{self.trn_cli} delete-net -i {self.phy_itf} -j'''
		self.trn_cli_update_ep = f'''{self.trn_cli} update-ep -i {self.phy_itf} -j'''
		self.trn_cli_get_ep = f'''{self.trn_cli} get-ep -i {self.phy_itf} -j'''
		self.trn_cli_delete_ep = f'''{self.trn_cli} delete-ep -i {self.phy_itf} -j'''
		self.trn_cli_load_pipeline_stage = f'''{self.trn_cli} load-pipeline-stage -i {self.phy_itf} -j'''

		self.trn_cli_load_transit_agent_xdp = f'''{self.trn_cli} load-agent-xdp'''
		self.trn_cli_unload_transit_agent_xdp = f'''{self.trn_cli} unload-agent-xdp'''
		self.trn_cli_update_agent_metadata = f'''{self.trn_cli} update-agent-metadata'''
		self.trn_cli_get_agent_metadata = f'''{self.trn_cli} get-agent-metadata'''
		self.trn_cli_delete_agent_metadata = f'''{self.trn_cli} delete-agent-metadata'''
		self.trn_cli_update_agent_ep = f'''{self.trn_cli} update-agent-ep'''
		self.trn_cli_get_agent_ep = f'''{self.trn_cli} get-agent-ep'''
		self.trn_cli_delete_agent_ep = f'''{self.trn_cli} delete-agent-ep'''

		if benchmark:
			self.xdp_path = "/trn_xdp/trn_transit_xdp_ebpf.o"
			self.agent_xdp_path = "/trn_xdp/trn_agent_xdp_ebpf.o"
		else:
			self.xdp_path = "/trn_xdp/trn_transit_xdp_ebpf_debug.o"
			self.agent_xdp_path = "/trn_xdp/trn_agent_xdp_ebpf_debug.o"

	def get_substrate_ep_json(self, droplet):
		jsonconf = {
			"tunnel_id": "0",
			"ip": droplet.ip,
			"eptype": "0",
			"mac": droplet.mac,
			"veth": "",
			"remote_ips": [""],
			"hosted_iface": ""
		}
		jsonconf = json.dumps(jsonconf)
		return jsonconf

	def update_substrate_ep(self, droplet):
		jsonconf = self.get_substrate_ep_json(droplet)
		cmd = f'''{self.trn_cli_update_ep} \'{jsonconf}\''''
		logger.info("update_substrate_ep: {}".format(cmd))
		returncode, text = run_cmd(cmd)
		logger.info("returns {} {}".format(returncode, text))

	def update_agent_substrate_ep(self, ep, droplet):
		itf = ep.get_veth_peer()
		jsonconf = self.get_substrate_ep_json(droplet)
		cmd = f'''{self.trn_cli_update_agent_ep} -i \'{itf}\' -j \'{jsonconf}\''''
		logger.info("update_agent_substrate_ep: {}".format(cmd))
		returncode, text = run_cmd(cmd)
		logger.info("update_agent_substrate_ep returns {} {}".format(returncode, text))

	def update_ep(self, ep, droplet):
		peer = ""

		# Only detail veth info if the droplet is also a host
		if (droplet and self.ip == droplet.ip):
			peer = ep.get_veth_peer()

		jsonconf = {
			"tunnel_id": ep.get_tunnel_id(),
			"ip": ep.get_ip(),
			"eptype": ep.get_eptype(),
			"mac": ep.get_mac(),
			"veth": ep.get_veth_name(),
			"remote_ips": ep.get_remote_ips(),
			"hosted_iface": peer
		}

		jsonconf = json.dumps(jsonconf)
		jsonkey = {
			"tunnel_id": ep.get_tunnel_id(),
			"ip": ep.get_ip(),
		}
		key = ("ep " + self.phy_itf, json.dumps(jsonkey))
		cmd = f'''{self.trn_cli_update_ep} \'{jsonconf}\''''
		logger.info("update_ep: {}".format(cmd))
		returncode, text = run_cmd(cmd)
		logger.info("returns {} {}".format(returncode, text))

	def update_agent_metadata(self, ep, net):
		itf = ep.get_veth_peer()
		jsonconf = {
			"ep": {
				"tunnel_id": ep.get_tunnel_id(),
				"ip": ep.get_ip(),
				"eptype": ep.get_eptype(),
				"mac": ep.get_mac(),
				"veth": ep.get_veth_name(),
				"remote_ips": ep.get_remote_ips(),
				"hosted_iface": self.phy_itf
			},
			"net": {
				"tunnel_id": net.get_tunnel_id(),
				"nip": net.get_nip(),
				"prefixlen": net.get_prefixlen(),
				"switches_ips": net.get_bouncers_ips()
			},
			"eth": {
				"ip": self.ip,
				"mac": self.mac,
				"iface": self.phy_itf
			}
		}
		jsonconf = json.dumps(jsonconf)
		cmd = f'''{self.trn_cli_update_agent_metadata} -i \'{itf}\' -j \'{jsonconf}\''''
		logger.info("update_agent_metadata: {}".format(cmd))
		returncode, text = run_cmd(cmd)
		logger.info("update_agent_metadata returns {} {}".format(returncode, text))

	def load_transit_agent_xdp(self, ep):
		itf = ep.veth_peer
		agent_pcap_file = itf + '.pcap'
		jsonconf = {
			"xdp_path": self.agent_xdp_path,
			"pcapfile": agent_pcap_file
		}
		jsonconf = json.dumps(jsonconf)
		cmd = f'''{self.trn_cli_load_transit_agent_xdp} -i \'{itf}\' -j \'{jsonconf}\' '''
		logger.info("load_transit_agent_xdp: {}".format(cmd))
		returncode, text = run_cmd(cmd)
		logger.info("load_transit_agent_xdp returns {} {}".format(returncode, text))