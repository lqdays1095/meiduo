from celery import Celery
# 路径需要设置从celery_tasks中查找
app = Celery('celery_tasks')  # 创建celery异步任务
app.config_from_object('celery_tasks.config')  # 加载配置文件
app.autodiscover_tasks(['celery_tasks.sms'])  # 让系统自动加载异步任务

