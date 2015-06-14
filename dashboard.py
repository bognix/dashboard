import json
from flask import Flask, jsonify
from flask.templating import render_template
from jenkinsapi.custom_exceptions import NoBuildData

from jenkinsapi.jenkins import Jenkins
from requests.exceptions import ConnectionError


app = Flask(__name__)


def get_jenkins():
    return Jenkins(get_config()['sources']['jenkins']['url'])


def get_config():
    return json.load(open('config.json'))


@app.route('/')
def index():
    config_data = get_config()
    return render_template('index.html', config=config_data, json_config=json.dumps(config_data))


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
                    'name': current_build.name.split('\xbb')[1]
                })

    return_val = {
        'name': build_name,
        'status': last_build.get_status(),
        'date': last_build.get_timestamp(),
        'failed_runs': failed_runs,
        'has_failed_runs': (len(failed_runs) != 0),
        'child_runs_count': child_runs_count,
        'failure_percentage': len(failed_runs) * 100 / child_runs_count
    }

    try:
        last_success = build.get_last_stable_build().get_timestamp(),
    except NoBuildData:
        last_success = '???'

    return_val['last_success'] = last_success

    return jsonify(return_val)


if __name__ == '__main__':
    app.debug = True
    app.run()
