from .utils import load_yaml
import yaml

CONFIG_FILE = '/etc/nbmessage-board/nbmessage-board-config.yaml'

class Config:
    def __init__(self):
        self._configs = load_yaml(CONFIG_FILE)
    
    def _save(self):
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(self._configs, f, default_flow_style=False)
    
    def update_config(self, kv: dict):
        self._configs.update(kv)
        self._save()
        