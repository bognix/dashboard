import json
import datetime
from flask import Flask, jsonify
from flask.templating import render_template
from jenkinsapi.custom_exceptions import NoBuildData
import os

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.artifact import Artifact
from requests.exceptions import ConnectionError


app = Flask(__name__)


def get_jenkins(jenkins_name):
    jenkins_config = get_config()['sources'][jenkins_name]

    if jenkins_config.has_key('secured') and jenkins_config['secured']:
        return Jenkins(jenkins_config['url'], username=os.environ['JENKINS_USER'], password=os.environ['JENKINS_PASS'])

    return Jenkins(jenkins_config['url'])

def get_config():
    return json.load(open('config.json'))

def get_item_config(build_name):
    config = get_config()
    if config.has_key('items') and config['items'].has_key(build_name):
        return config['items'][build_name]
    return {}

@app.route('/')
def index():
    config_data = get_config()
    screens_count = len(config_data['screens'])
    return render_template(
        'index.html', config=config_data, json_config=json.dumps(config_data), screens_count=screens_count)


@app.route('/jenkins_results/<jenkins_name>/<build_name>', methods=['GET'])
def get_build_data(jenkins_name, build_name):
    jenkins_instance = get_jenkins(jenkins_name)
    item_config = get_item_config(build_name)
    if jenkins_instance is not None:
        build = jenkins_instance[build_name]
    else:
        raise ConnectionError("Connection with Jenkins failed")

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

    print return_val['status']
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
                if current_build.get_number() == last_build_number and current_build.get_status() == 'FAILURE' or current_build.get_status() == 'UNSTABLE':
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

    return jsonify(return_val)

def get_time_ago(run_date):
    return int((datetime.datetime.utcnow().replace(tzinfo=None)
         - run_date.replace(tzinfo=None)).total_seconds() / 3600)

if __name__ == '__main__':
    app.debug = True
    app.run()
