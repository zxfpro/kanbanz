"""
更加偏重系统级别

"""

from .manager import KanbanManager,Pool

class KanbanSystem():
    """
    
    """
    def __init__(self,kanban_path:str):
        self.km = KanbanManager(kanban_path)
        self.km.pull()

    def input_ready_pool(self,text):
        """
        写入预备池
        """
        self.km.insert(text=text,pool=Pool.预备池)

    def ready_pool_2_order_pool(self,text):
        """
        预备池->就绪池
        """
        self.km.pop(inputs=text,by='description',pool=Pool.预备池)
        self.km.insert(text=text,pool=Pool.就绪池)

    def order_pool_2_execution_pool(self):
        """
        就绪池转移到执行池
        """
        self.km.pop(inputs=text,by='description',pool=Pool.就绪池)
        self.km.insert(text=text,pool=Pool.执行池)

    def order_pool_2_soy_pool(self):
        """
        就绪池->酱油池
        """
        self.km.pop(inputs=text,by='description',pool=Pool.就绪池)
        self.km.insert(text=text,pool=Pool.酱油池)

    def execution_pool_2_finishing_pool(self):
        """
        执行池->完成池
        """
        self.km.pop(inputs=text,by='description',pool=Pool.执行池)
        self.km.insert(text=text,pool=Pool.完成池)

    def execution_pool_2_choke_pool(self):
        """
        执行池->阻塞池
        """
        self.km.pop(inputs=text,by='description',pool=Pool.执行池)
        self.km.insert(text=text,pool=Pool.阻塞池)

    def choke_pool_2_order_pool(self):
        """
        阻塞池->就绪池
        """
        self.km.pop(inputs=text,by='description',pool=Pool.阻塞池)
        self.km.insert(text=text,pool=Pool.就绪池)

    def soy_pool_2_memorandum(self):
        """
        酱油池->备忘录
        """
        pass

    def execution_pool_2_calendar(self):
        """
        执行池->日历
        """
        pass

    def finishing_pool_2_ARCHIVIST(self):
        """
        完成池->归档
        """
        pass





    