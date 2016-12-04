import time


log_config = {}


def set_path():
    """
    设置 日志文件
    """
    fmt = '%H%M%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    log_config['file'] = 'logs/log.only.{}.txt'.format(dt)


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    fmt = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    if 'file' not in log_config:
        set_path()
    path = log_config.get('file')
    with open(path, 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)
