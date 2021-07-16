"""
created by dyx on 2021/7/16.
"""

import logging

# 默认的warning级别，只输出warning以上的
# 使用basicConfig()来指定日志级别和相关信息

logging.basicConfig(level=logging.DEBUG,
                    filename="demo.log",  # log日志输出的文件位置和文件名
                    filemode="w",  # 文件写入格式，w为重新写入，默认是追加
                    format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s",
                    # 日志输出的格式 # -8表示占位符，让输出左对齐，输出长度都为8位
                    datefmt="%Y-%m-%d %H:%M:%S"  # 时间输出格式
                    )

logging.debug("this is DEBUG !!!")
logging.info("this is INFO !!")
logging.warning("this is WARNING !!!")
logging.critical("this is CRITICAL !!")

# 在实际项目中，捕获异常的时候，如果使用logging.error(e),只提示logging信息，不会出现为什么会错的信息，所以要使用logging.exception(e)去记录

try:
    4 / 0
except Exception as e:
    logging.exception(e)

"""
logging 编程方式代码demo
"""
import logging

# 编程的方式记录日志

# 记录器
logger1 = logging.getLogger("logger1")
logger1.setLevel(logging.DEBUG)

logger2 = logging.getLogger("logger2")
logger2.setLevel(logging.INFO)

# 处理器
# 1.标准输出
sh1 = logging.StreamHandler()
sh1.setLevel(logging.WARNING)
sh2 = logging.StreamHandler()

# 2.文件输出
# 没有设置输出级别，将logger1的输出级别
fh1 = logging.FileHandler(filename="fh.log", mode='w')

fh2 = logging.FileHandler(filename='fh.log', mode='a')
fh2.setLevel(logging.WARNING)

# 格式器
fmt1 = logging.Formatter(fmt="%(asctime)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s")

fmt2 = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s"
                         , datefmt="%Y/%m/%d %H:%M:%S")

# 给处理器设置格式
sh1.setFormatter(fmt1)
fh1.setFormatter(fmt2)
sh2.setFormatter(fmt2)
fh2.setFormatter(fmt1)

# 记录器设置处理器
logger1.addHandler(sh1)
logger1.addHandler(fh1)
logger2.addHandler(sh2)
logger2.addHandler(fh2)

# 打印日志代码
logger1.debug("This is  DEBUG of logger1 !!")
logger1.info("This is  INFO of logger1 !!")
logger1.warning("This is  WARNING of logger1 !!")
logger1.error("This is  ERROR of logger1 !!")
logger1.critical("This is  CRITICAL of logger1 !!")

logger2.debug("This is  DEBUG of logger2 !!")
logger2.info("This is  INFO of logger2 !!")
logger2.warning("This is  WARNING of logger2 !!")
logger2.error("This is  ERROR of logger2 !!")
logger2.critical("This is  CRITICAL of logger2 !!")