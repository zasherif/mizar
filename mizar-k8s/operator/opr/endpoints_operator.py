from opr.droplet import DropletStore
import logging
logger = logging.getLogger()

class EndpointOperator(object):
	_instance = None

	def __new__(cls, **kwargs):
		if cls._instance is None:
			cls._instance = super(EndpointOperator, cls).__new__(cls)
			cls._init(cls, **kwargs)
		return cls._instance

	def _init(self, **kwargs):
		logger.info(kwargs)
		self.ds = DropletStore()

	def on_create(self, body, spec, **kwargs):
		logger.info("*create_endpoint {}".format(self.ds.store))

	def on_delete(self, body, spec, **kwargs):
		logger.info("*delete_endpoint {}".format(self.ds.store))

	def on_update(self, body, spec, **kwargs):
		logger.info("*update_endpoint {}".format(self.ds.store))

	def on_resume(self, spec, **kwargs):
		logger.info("*resume_endpoint {}".format(self.ds.store))
