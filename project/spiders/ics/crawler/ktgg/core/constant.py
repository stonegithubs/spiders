# coding=utf-8
"""
用于保存开庭公告爬虫中的一些常量，枚举等
"""


class TASK_STATUS(object):
    """
    任务状态枚举类
    """
    DISPATCH = 100              # 调度中
    PREPARE = 101               # 准备阶段，未启动
    # START_FAILED = 102           # 启动失败(下发到队列失败)
    RUNNING = 103               # 运行中
    # RUNNING_TIME_OUT = 104      # 运行超时(运行时间超过某一个很长的时间阀值，都没有达到抓取完成的条件)
    SUCCESS = 105               # 运行成功
    FAILED = 106                 # 运行失败
    NO_RECORD = 107
    # INCOMPLETE = 108


# TODD 这些配置，是否迁移到default_setting.py中去
DATA_TABLE = 'tbl_ktgg_data'
STATUS_TABLE = 'tbl_ktgg_status'
RAW_TABLE = 'tbl_ktgg_raw'
KTGG_MANAGER_TABLE = 'tbl_ktgg_manager'
KTGG_STATUS_TABLE = 'tbl_ktgg_status'
KTGG_TASK_QUEUE = 'ktgg_queue'


if __name__ == '__main__':
    import datetime
    print datetime.datetime.now().strftime('%Y-%m-%d')


