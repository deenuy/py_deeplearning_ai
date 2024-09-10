# config_loader.py

import yaml

class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path
        self._add_custom_constructors()

    def _add_custom_constructors(self):
        # Define the custom constructor for !join
        def join_constructor(loader, node):
            seq = loader.construct_sequence(node)
            return ''.join(seq)

        # Add the custom constructor to the PyYAML loader
        yaml.add_constructor('!join', join_constructor)

    def load_config(self):
        with open(self.config_path, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        return config
