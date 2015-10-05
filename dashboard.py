import json
import datetime
from flask import Flask, jsonify
from flask.templating import render_template
from jenkinsapi.custom_exceptions import NoBuildData
import os
import argparse

from jenkinsapi.jenkins import Jenkins
from requests.exceptions import ConnectionError


app = Flask(__name__)


def get_jenkins():
    return Jenkins(get_config()['sources']['jenkins']['url'])

def get_jenkins_api():
    return Jenkins(get_config()['sources']['jenkins-api']['url'], username=os.environ['JENKINS_USER'], password=os.environ['JENKINS_PASS'])

def get_config():
    return json.load(open('config.json'))


@app.route('/')
def index():
    config_data = get_config()
    screens_count = len(config_data['screens'])
    orientation = app.screen_orientation
    return render_template(
        'index.html', config=config_data, json_config=json.dumps(config_data), screens_count=screens_count, orientation=orientation)


@app.route('/jenkins_results/<build_name>', methods=['GET'])
def get_build_data(build_name):
    jenkins_instance = get_jenkins()
    if jenkins_instance is not None:
        build = jenkins_instance[build_name]
    else:
        raise ConnectionError("Connection with Jenkins failed")

    last_build = build.get_last_build()
    last_build_number = build.get_last_buildnumber()
    child_runs = last_build.get_matrix_runs()
    child_runs_count = 0
    failed_runs = []

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

    return_val = {
        'name': build_name,
        'status': last_build.get_status(),
        'hours_ago': get_time_ago(last_build.get_timestamp()),
        'failed_runs': failed_runs,
        'has_failed_runs': (len(failed_runs) != 0),
        'child_runs_count': child_runs_count,
        'failure_percentage': len(failed_runs) * 100 / child_runs_count if (child_runs_count != 0) else 100
    }

    try:
        last_success = get_time_ago(build.get_last_stable_build().get_timestamp()),
    except NoBuildData:
        last_success = '???'

    return_val['last_success'] = last_success

    return jsonify(return_val)

@app.route('/jenkins_api_results/<build_name>', methods=['GET'])
def get_build_data_api(build_name):
    jenkins_instance = get_jenkins_api()
    if jenkins_instance is not None:
        build = jenkins_instance[build_name]
    else:
        raise ConnectionError("Connection with Jenkins failed")

    last_build = build.get_last_build()
    last_build_number = build.get_last_buildnumber()
    child_runs = last_build.get_matrix_runs()
    child_runs_count = 0
    failed_runs = []

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

    return_val = {
        'name': build_name,
        'status': last_build.get_status(),
        'hours_ago': get_time_ago(last_build.get_timestamp()),
        'failed_runs': failed_runs,
        'has_failed_runs': (len(failed_runs) != 0),
        'child_runs_count': child_runs_count,
        'failure_percentage': len(failed_runs) * 100 / child_runs_count if (len(failed_runs) != 0) else 0
    }

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
    parser = argparse.ArgumentParser(description='Screen orientation.')
    parser.add_argument('--orientation', metavar='O', type=str, required=False, default='horizontal',
                   help='Screen Orientation - possible values: horizontal, vertical')
    app.debug = True
    app.screen_orientation = parser.parse_args().orientation
    app.run()
