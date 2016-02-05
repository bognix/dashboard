import os
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.custom_exceptions import NoBuildData, JenkinsAPIException
from jenkinsapi.artifact import Artifact
from requests.exceptions import ConnectionError
import datetime


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

    def get_build_results(self, build_name, build_config={}):
        if build_config.has_key('type') and build_config['type'] == 'single':
            return self.get_single_build_results(build_name, build_config=build_config)
        else:
            return self.get_grouped_build_results(build_name, build_config=build_config)

    def get_grouped_build_results(self, build_name, build_config={}):
        build = self.JENKINS_INSTANCE[build_name]
        last_build = build.get_last_build()
        last_build_number = build.get_last_buildnumber()
        child_runs = last_build.get_matrix_runs()
        child_runs_count = 0
        failed_runs = []
        return_val = {
            'name': build_name,
            'status': last_build.get_status(),
            'hours_ago': self.get_time_ago(last_build.get_timestamp()),
        }

        if build_config.has_key('artifact'):
            try:
                output = Artifact('output', build_config['artifact'], last_build).get_data()
                return_val['artifact_output'] = output
            except JenkinsAPIException:
                return_val['image'] = 'happy'
        elif build_config.has_key('simple'):
            if last_build.get_status() == 'SUCCESS':
                return_val['image'] = 'happy'
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
            last_success = self.get_time_ago(build.get_last_stable_build().get_timestamp()),
        except NoBuildData:
            last_success = '???'

        return_val['last_success'] = last_success

        return return_val

    def get_single_build_results(self, build_name, build_config={}):
        return_val = {
            'name': build_name
        }
        failed_runs = []
        aborted_runs = []
        succeded_runs = []
        build = self.JENKINS_INSTANCE[build_name]

        if build_config.has_key('target_env'):
            last_build = self.get_last_build_matching_env(build, build_config['target_env'])
        else:
            last_build = build.get_last_build()

        if last_build is not None:
            last_build_number = last_build.get_number()

            last_build_status = last_build.get_status()
            return_val['status'] = last_build_status
            child_runs_count = 0

            child_runs = last_build.get_matrix_runs()

            has_next = True
            while has_next:
                try:
                    current_build = child_runs.next()
                except StopIteration:
                    has_next = False

                if has_next:
                    child_runs_count += 1
                    if current_build.get_number() is last_build_number:
                        if current_build.get_status() == 'FAILURE' or current_build.get_status() == 'UNSTABLE':
                            failed_runs.append({
                                'name': current_build.name.split('\xbb')[1].split(',')[0]
                            })
                        elif current_build.get_status() == 'ABORTED':
                            aborted_runs.append({
                                'name': current_build.name.split('\xbb')[1].split(',')[0]
                            })
                        elif current_build.get_status() == 'SUCCESS':
                            succeded_runs.append({
                                'name': current_build.name.split('\xbb')[1].split(',')[0]
                            })

            return_val['failed_runs'] = failed_runs
            return_val['aborted_runs'] = aborted_runs
            return_val['success_count'] = len(succeded_runs)
            return_val['total_count'] = child_runs_count
            return_val['hours_ago'] = self.get_time_ago(last_build.get_timestamp())
            return_val['is_running'] = last_build.is_running()
            return_val['has_failed_runs'] = (len(failed_runs) != 0)
            return_val['has_aborted_runs'] = (len(aborted_runs) != 0)
            return_val['failed_count'] = len(failed_runs)
            return_val['aborted_count'] = len(aborted_runs)

            if len(aborted_runs) != 0:
                return_val['status'] = 'ABORTED'
            elif last_build.is_running():
                return_val['status'] = None

            if build_config.has_key('target_env') is not None:
                return_val['environment'] = build_config['target_env']

        return return_val

    def get_time_ago(self, run_date):
        return int((datetime.datetime.utcnow().replace(tzinfo=None)
            - run_date.replace(tzinfo=None)).total_seconds() / 3600)

    def get_last_build_matching_env(self, build, env):
        not_found = True
        last_build = build.get_last_build()
        last_build_number = last_build.get_number()
        counter = 0

        while not_found and (counter < 10) and (last_build_number > 0):
            if self.extract_env_from_params(last_build.get_actions()['parameters']) == env:
                return last_build
            last_build = build.get_build((last_build_number - 1))
            last_build_number = last_build.get_number()
            counter = counter + 1

        return None

    def extract_env_from_params(self, params):
        for d in params:
            if 'env' in d.values():
                return d['value']

