
import requests
from datetime import datetime
from grapherz.canvas.core import Canvas,Color
from kanban.core import Pool,Kanban
from contextlib import contextmanager
from ..scripts.aifunc import give_a_task_time,generate_schedule
from reallife import KANBAN_PATH,WORK_CANVAS_PATH,Date
from .status import status
from ..scripts.applescript import Calulate,Notes,Reminder
from .utils import parse_execution_jiangyou_pool,parse_execution_pool, read_file
from .utils import git_pull, git_push
import asyncio

date_c = Date()
date = date_c.date

@contextmanager
def controlKanban(kanban:Kanban):
    kanban.pull()
    yield kanban
    kanban.push()

@contextmanager
def sync_obsidian_github(commit:str):
    git_pull("obsidian")
    yield
    git_push('obsidian',commit=commit)


class KanBanManager():
    def __init__(self,kanban_path,pathlib):
        self.kanban_path = kanban_path
        self.pathlib = pathlib
        self.kanban = Kanban(self.kanban_path)
        self.main_path = "/Users/zhaoxuefeng/GitHub/obsidian/工作"

    @status(task="同步预备池",date=date,run_only=True)
    def sync_ready(self):
        def encode(i,project_name):
            return project_name+'-'+i
        
        def save_in_pauses(i,pauses):
            for pause in pauses:
                if i.get('text') in pause:
                    return True
            return False
        with sync_obsidian_github("同步预备池"):
            for path in self.pathlib:
                canvas_path=self.main_path+path
                try:
                    canvas = Canvas(file_path=canvas_path)
                except FileNotFoundError as e:
                    print(e)
                    continue
                with controlKanban(self.kanban) as kb:
                    project_name = canvas_path.rsplit('/',2)[-2] 
                    pauses = kb.get_tasks_in(pool=Pool.阻塞池)
                    readys = kb.get_tasks_in(pool=Pool.预备池)

                    nodes = [i.get('text') or '' for i in canvas.select_by_color(Color.yellow,type='node') if not save_in_pauses(i,pauses=pauses)]
                    for i in nodes:
                        if i not in readys:
                            kb.insert(text=encode(i,project_name),pool=Pool.预备池)
        return 'success'

    @status(task="同步就绪池",date=date,run_only=True)
    def sync_order(self):
        with sync_obsidian_github("调整优先级"):
            with controlKanban(self.kanban) as kb:
                tasks = kb.get_tasks_in(Pool.预备池)
                order_tasks = kb.get_tasks_in(Pool.就绪池)
                orders = ' '.join(order_tasks)
                for task in tasks:
                    kb.pop(text = task,pool = Pool.预备池)
                    if task not in orders:
                        task_ = give_a_task_time(task)
                        kb.insert(text=task_,pool=Pool.就绪池)
        return 'success'

    @status(task="同步执行池",date=date,run_only=True)
    def sync_run(self)->str:
        with sync_obsidian_github("同步到执行池"):
            with controlKanban(self.kanban) as kb:
                tasks = kb.get_tasks_in(Pool.就绪池)
                all_task_time = 0
                for task in tasks:
                    if task.split(' ')[0][-1].lower() != 'p':
                        continue
                    task_time = int(task.split(' ')[0][:-1])

                    if all_task_time + task_time <=14:
                        all_task_time += task_time
                        kb.pop(text=task,pool=Pool.就绪池)
                        kb.insert(text=task,pool=Pool.执行池)

                    elif all_task_time < 8:
                        pass
        return 'success'
    
    @status(task="回收未完成的任务",date=date,run_only=True)
    def sync_run2order(self):
        with controlKanban(self.kanban) as kb:
            tasks = kb.get_tasks_in(Pool.执行池)
            if tasks:
                for task in tasks:
                    kb.pop(text=task,pool=Pool.执行池)
                    kb.insert(text=task,pool=Pool.就绪池)
            
        return 'success'

    @status(task="任务完成的任务",date=date,run_only=True)
    def sync_run2over(self,task:str,
                      canvas_path:str):

        """从执行池添加到完成池
        # multi_line_input = "备案-新域名做域名备案$/工程系统级设计/项目级别/数字人生/模拟资质认证/模拟资质认证.canvas\n"

        1 将task从执行池添加到完成池
        2 将canvas 中的颜色变绿
        Args:
            kanban_path (str): 看板路径

        Returns:
            None: None
        """
        
        canvas_path = canvas_path.replace('\n','')
        canvas_path =self.main_path+canvas_path


        with controlKanban(self.kanban) as kb:
            task = task.split('-',1)[-1]
            if len(kb.get_task_by_word(task,pool=Pool.执行池)) == 0:
                kb.insert(text=task,pool=Pool.完成池)
                kb.push()
                return 'failed'

            task_ = kb.get_task_by_word(task,pool=Pool.执行池)[0]
            kb.pop(text=task_,pool=Pool.执行池)
            kb.insert(text=task_,pool=Pool.完成池)

            # and
            canvas = Canvas(file_path=canvas_path)
            tasks = canvas.select_nodes_by_text(task)
            try:
                tasks[0].color = Color.green.value
            except IndexError as e:
                return f'error: {e}'
            canvas.to_file(canvas_path)

        return 'success'

    @status(task="同步记录",date=date,run_only=False)
    def add_tips(self,task:str):
        """从执行池添加到完成池
        1 将task从执行池添加到完成池
        2 将canvas 中的颜色变绿
        Args:
            kanban_path (str): 看板路径

        Returns:
            None: None
        """
        with controlKanban(self.kanban) as kb:
            kb.insert(text=task,pool=Pool.预备池)
        return 'success'

    @status(task="同步体重",date=date,run_only=True)
    def sync_weight(self)->str:
        """
        同步体重
        """

        url = f"http://101.201.244.227:8000/weight/{date}"
        response = requests.get(url)
        result = response.json().get('weight')
        x = f"""---
番茄: 14
体重: {result}
---
"""

        with open(self.main_path + f'/日记/{date}.md','a') as f:
            f.write(x)
        return 'success'
