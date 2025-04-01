"""
kanban manager

"""

import json
import re
from enum import Enum

class Pool(Enum):
    """
    预备池,就绪池,阻塞池,执行池,完成池,酱油池
    """
    预备池 ='预备池'
    就绪池 ='就绪池'
    阻塞池 ='阻塞池'
    执行池 ='执行池'
    完成池 ='完成池'
    酱油池 ='酱油池'


class KanbanManager():
    """
    
    """
    def __init__(self,kanban_path:str):
        """
        
        """
        self.kanban_path = kanban_path
        self.kanban_dict = {}

    def pull(self):
        """
        从文档拉取信息到
        """
        with open(self.kanban_path,'r') as f:
            text = f.read()
        self.kanban_dict = self._read(text)


    def push(self):
        """
        
        """
        text = self._write(self.kanban_dict)
        with open(self.kanban_path,'w') as f:
            f.write(text)


    def insert(self,text:str,pool:Pool):
        """
        将pool 中添加信息
        """
        self.kanban_dict[pool.value].append({'status': ' ', 'description': text, 'id':12, 'level': 2})


    def pop(self,inputs:str,by:str,pool:Pool):
        """
        将pool 中删除信息
        """
        def delete_by_description(data, description):
            """按描述删除数据列"""
            for i, item in enumerate(data):
                if item.get('description') == description:
                    del data[i]
                    return data
            print(f"未找到描述为 '{description}' 的数据列")
            return data

        def delete_by_id(data, target_id):
            """按ID删除数据列"""
            for i, item in enumerate(data):
                if item.get('id') == target_id:
                    del data[i]
                    return data
            print(f"未找到ID为 '{target_id}' 的数据列")
            return data

        data = self.kanban_dict[pool.value]
        if by == 'id':
            delete_by_id(data,inputs)
        elif by =='description':
            delete_by_description(data,inputs)
        

    def _read(self,text):
        # 提取池的名称和内容
        pool_pattern = re.compile(r'## ([\s\S]+?)(?=\n## |\n\n\n|\n\*\*\*)')
        pools = pool_pattern.findall(text)
        # 提取任务列表
        task_pattern = re.compile(r'- \[([x ])\]([\s\S]+?)(?=\n|$)')

        kanban_dict = {}

        for pool in pools:
            # 分割池的名称和内容
            try:
                pool_name, pool_content = pool.split('\n', 1)
                pool_name = pool_name.strip()
            except ValueError:
                pool_name = pool
                pool_content = ""
            
            # 提取任务列表
            tasks = task_pattern.findall(pool_content)
            
            # 将任务整理为字典格式
            task_list = []
            for task in tasks:
                status = task[0].strip()
                status = status or " "
                description = task[1].strip()
                task_list.append({
                    "status": status,
                    "description": description
                })
            
            kanban_dict[pool_name] = task_list
        return kanban_dict
    

    def _write(self,kanban_dict):
        """
        将字典格式的Kanban板转换为标准Markdown格式的文本。
        
        Args:
            kanban_dict (dict): 字典格式的Kanban板。
            
        Returns:
            str: 标准Markdown格式的文本。
        """
        markdown = ""
        
        for pool_name, tasks in kanban_dict.items():
            # 添加池的标题
            markdown += f"## {pool_name}\n\n"
            
            # 添加任务列表
            for task in tasks:
                status = task["status"]
                description = task["description"].strip()
                markdown += f"- [{status}] {description}\n"
            
            # 池之间添加空行
            markdown += "\n"
        head = """---

kanban-plugin: board

---
"""
        
        tail = """
        
%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[false,false,false,false,false,false],"link-date-to-daily-note":true,"tag-sort":[{"tag":""}],"move-tags":false,"lane-width":350,"tag-colors":[]}
```
%%
"""
        return head + markdown.strip() + tail


if __name__ == "__main__":
    kanban_path = "/Users/zhaoxuefeng/本地文稿/百度空间/cloud/Obsidian/知识体系尝试/工作/工程二开UseCase/ceshi.md"
    cm = KanbanManager(kanban_path)
    cm.pull()
    print(cm.kanban_dict,'canvs')
