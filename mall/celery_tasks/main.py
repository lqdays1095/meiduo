from celery import Celery
# 创建celery异步任务的时候,先创建一个异步任务的文件夹
# main.py作为一部任务的启动文件
# 创建异步任务对象,然后加载配置文件

app = Celery('celery_tasks')
app.config_from_object('celery_tasks.config')
# 然后自动加载任务
app.autodiscover_tasks(['celery_tasks.sms'])

