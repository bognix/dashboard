import json
import datetime
from flask import Flask, jsonify
from flask.templating import render_template

from dashboard_config import DashboardConfig
from jenkins_wrapper import JenkinsWrapper
from werkzeug.contrib.cache import SimpleCache


app = Flask(__name__)
cache = SimpleCache()


def get_jenkins_instance(jenkins_name):
    jenkins_instance = cache.get('%s-jenkins' % jenkins_name)
    if jenkins_instance is None:
        jenkins_instance = JenkinsWrapper(jenkins_name, get_dashboard_config())
        cache.set('%s-jenkins' % jenkins_name, jenkins_instance, timeout=1440 * 60)
    return jenkins_instance

def get_dashboard_config():
    dashboard_config = cache.get('dashboard_config')
    if dashboard_config is None:
        dashboard_config = DashboardConfig().get_config()
        cache.set('dashboard_config', dashboard_config, timeout=1440 * 60)
    return dashboard_config


def get_item_config(build_name):
    config = get_dashboard_config()
    if config.has_key('items') and config['items'].has_key(build_name):
        return config['items'][build_name]
    return {}

@app.route('/')
def index():
    config_data = get_dashboard_config()
    screens_count = len(config_data['screens'])
    return render_template(
        'index.html', config=config_data, json_config=json.dumps(config_data), screens_count=screens_count)


@app.route('/jenkins_results/<jenkins_name>/<build_name>', methods=['GET'])
def get_build_data(jenkins_name, build_name):
    item_config = get_item_config(build_name)

    return jsonify(get_jenkins_instance(jenkins_name).get_build_results(build_name, item_config))


if __name__ == '__main__':
    app.debug = True
    app.run()
