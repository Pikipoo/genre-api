import yaml

with open('config.yaml', 'r') as config_file:
    CONFIG = yaml.safe_load(config_file)
