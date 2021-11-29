import logging  # 引入logging模块
import os.path
import time
import sys
#print("sys.path[0] = ", sys.path[0])
def init_logger():
    # 第一步，创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Log等级总开关
    # 第二步，创建一个handler，用于写入日志文件
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    #log_path = os.path.dirname(os.getcwd()) + '/logs/'
    log_path = str(sys.path[0])+ '/logs/'
    log_name = log_path + rq + '.log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    # 第四步，将logger添加到handler里面
    logger.addHandler(fh)
    return logger
flask_logger = init_logger()
flask_out2user=[]
# 日志
'''
flask_logger.debug('this is a logger debug message')
flask_logger.info('this is a logger info message')
flask_logger.warning('this is a logger warning message')
flask_logger.error('this is a logger error message')
flask_logger.critical('this is a logger critical message')
'''