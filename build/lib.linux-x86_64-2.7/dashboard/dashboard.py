import json
from flask import Flask, jsonify
from flask.templating import render_template

from jenkinsapi.jenkins import Jenkins
from requests.exceptions import ConnectionError
from flask import g


def get_jenkins():
    print 'aaa'
    if jenkins is None:
        print 'bbb'
        try:
            jenkins = Jenkins(get_config()['sources']['jenkins']['url'])
        except ConnectionError:
            jenkins = None

    return jenkins


app = Flask(__name__)
jenkins = get_jenkins()



def get_config():
    config = getattr(g, '_config', None)
    if config is None:
        config = g._config = json.load(open('config.json'))

    return config


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
    child_runs_results = []

    has_next = True
    while has_next:
        try:
            current_build = child_runs.next()
            if current_build.get_number() == last_build_number:
                child_runs_results.append({
                    'name': current_build.name.split('\xbb')[1],
                    'status': current_build.get_status()
                })
        except StopIteration:
            has_next = False

    return jsonify({
        'name': build_name,
        'status': last_build.get_status(),
        'date': last_build.get_timestamp(),
        'last_success': build.get_last_stable_build().get_timestamp(),
        'child_runs': child_runs_results,
        'has_child_runs': (len(child_runs_results) != 0),
        'number': last_build_number
    })


if __name__ == '__main__':
    app.debug = True
    app.run()
