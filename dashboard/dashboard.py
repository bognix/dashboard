import json
from flask import Flask, jsonify
from flask.templating import render_template
from flask.ext.cache import Cache

from jenkinsapi.jenkins import Jenkins
from requests.exceptions import ConnectionError


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@cache.cached(key_prefix='jenkins_instance')
def get_jenkins():
    return Jenkins(get_config()['sources']['jenkins']['url'])


@cache.cached(key_prefix='config')
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
