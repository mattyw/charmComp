import copy
import json
import subprocess
import toml

CONFIG_PATH = "/opt/influxdb/shared/config.toml"


def read_config():
    with open(CONFIG_PATH) as fh:
        data = fh.read()
    return toml.loads(data)


def write_config(seeds=None):
    existing_config = read_config()
    config = copy.deepcopy(existing_config)

    svc_config = json.loads(
        subprocess.check_output(['config-get', '--format=json']))
    if svc_config['log-level'] in ('debug', 'info', 'warn', 'error'):
        config['logging']['level'] = svc_config['log-level']

    if seeds is not None:
        config['cluster']['seed-servers'] = seeds

    if config == existing_config:
        return False

    with open(CONFIG_PATH, 'w') as fh:
        toml.dump(config, fh)
    subprocess.check_output(['service', 'influxdb', 'restart'])
    return True
