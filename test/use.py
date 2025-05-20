from kanbanz.manager import KanBanManager

kanban_path = "/Users/zhaoxuefeng/GitHub/obsidian/实验室/ceshi.md"


import importlib.resources

import yaml

def load_config():
    with open('config.yaml','r') as f:
        return yaml.safe_load(f)

x = load_config().get('WORK_CANVAS_PATH')

kb = KanBanManager(kanban_path=kanban_path,pathlib=x)

kb.sync_ready()

kb.sync_order()

kb.sync_run()

kb.sync_run2order()

kb.sync_run2over(task = '',
                canvas_path:str)

