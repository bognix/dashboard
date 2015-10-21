import os
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.custom_exceptions import NoBuildData
from jenkinsapi.artifact import Artifact
from requests.exceptions import ConnectionError


class JenkinsWrapper:

	JENKINS_INSTANCE = None

	def __init__(self, jenkins_name, config, *args, **kwargs):
		jenkins_config = config['sources'][jenkins_name]
		if jenkins_config.has_key('secured') and jenkins_config['secured']:
			self.JENKINS_INSTANCE = Jenkins(
			jenkins_config['url'],
				username=os.environ['JENKINS_USER'],
				password=os.environ['JENKINS_PASS'])
		else:
			self.JENKINS_INSTANCE = Jenkins(jenkins_config['url'])

		if self.JENKINS_INSTANCE is None:
			raise ConnectionError("Connection with Jenkins failed")

	def get_jenkins_intance(self):
		return self.JENKINS_INSTANCE

	def get_build(self, build_name):
		return self.JENKINS_INSTANCE[build_name]

	def get_build_results(self, build_name, build_config):
		build = self.JENKINS_INSTANCE[build_name]
		last_build = build.get_last_build()
		last_build_number = build.get_last_buildnumber()
		child_runs = last_build.get_matrix_runs()
		child_runs_count = 0
		failed_runs = []
		return_val = {
			'name': build_name,
			'status': last_build.get_status(),    
			'hours_ago': get_time_ago(last_build.get_timestamp()),
		}

		if item_config.has_key('artifact'):
			output = Artifact('output', item_config['artifact'], last_build).get_data()
			return_val['artifact_output'] = output
		else:
			has_next = True
			while has_next:
				try:
					current_build = child_runs.next()
				except StopIteration:
					has_next = False

			if has_next:
				child_runs_count += 1
				if current_build.get_number() == last_build_number and current_build.get_status() == 'FAILURE':
					failed_runs.append({
						'name': current_build.name.split('\xbb')[1].split(',')[0]
				})

		return_val['failed_runs'] = failed_runs
		return_val['has_failed_runs'] = (len(failed_runs) != 0)
		return_val['child_runs_count'] = child_runs_count
		return_val['failure_percentage'] = len(failed_runs) * 100 / child_runs_count if (child_runs_count != 0) else 100

		try:
			last_success = get_time_ago(build.get_last_stable_build().get_timestamp()),
		except NoBuildData:
			last_success = '???'

		return_val['last_success'] = last_success

		return return_val

		def get_time_ago(run_date):
			return int((datetime.datetime.utcnow().replace(tzinfo=None)
				- run_date.replace(tzinfo=None)).total_seconds() / 3600)
