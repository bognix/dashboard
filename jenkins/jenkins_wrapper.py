class JenkinsFactory:
	@staticmethod
	def get_jenkins_instance(jenkin_name, config):
		jenkins_config = config.sources[jenkins_name]
		return JenkinsWrapper(jenkins_config)

class JenkinsWrapper:
	def __init__(config):
		