import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 转换格式
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('sx.log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)
