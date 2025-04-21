
# 1 看板的拉取和推送
```python
from kanban import Kanban,Pool
kanban_path = "/Users/zhaoxuefeng/GitHub/obsidian/工作/实验室/ceshi.md"
kb = Kanban(kanban_path)
kb.pull()
# TODO

kb.push()
```

## 在某池中插入任务

```python

kb.insert('任务1',Pool.预备池)

```

## 在某池中推出任务

```python

kb.pop('任务1',Pool.预备池)

```


## 查询某池中的所有任务

```python
kb.get_tasks_in(Pool.预备池)
```

## 查询某池中的任务,根据关键字查询
```python
kb.get_task_by_word(word='合理',Pool.预备池)
```