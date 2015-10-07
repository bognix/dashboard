class DashboardConfig:
	config_location = 'config.json'

	def __init__(*args, **kwargs):
		config_json = json.load(open(self.config_location))

	def get_config():
		return config_json
