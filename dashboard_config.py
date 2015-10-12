import json

class DashboardConfig:
	
	CONFIG_LOCATION = 'config.json'
	
	def __init__(self, *args, **kwargs):
		self.config_json = json.load(open(self.CONFIG_LOCATION))

	def get_config(self):
		return self.config_json
