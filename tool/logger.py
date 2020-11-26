import logging.handlers


class GetLogger:
    logger = None
    @classmethod
    def get_logger(cls):
        # 单例
        if not cls.logger:
            # 获取日志(自己写日志的名字，不写root)
            cls.logger = logging.getLogger()
            # 给日志设置一个默认级别  日志级别是大写的
            cls.logger.setLevel(logging.INFO)
            # 格式器，定义输出格式
            fmt = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d] - %(message)s"
            # 定义格式器,并把具体的格式放到格式器中进行实例化
            fm = logging.Formatter(fmt)
            # 处理器
            tf = logging.handlers.TimedRotatingFileHandler(filename="../logger/test.log",
                                                  when='midnight',
                                                  interval=1,
                                                  backupCount= 3, # 始终保留三个文件,最新的会把最老的覆盖掉
                                                  encoding='utf-8')
            # 在处理器中添加格式器
            tf.setFormatter(fm)
            # 在日志器中添加处理器
            cls.logger.addHandler(tf)
        # 最终返回一个日志对象
        return cls.logger


if __name__ == '__main__':
    # 调试
    logger = GetLogger().get_logger()
    logger.debug('我要开始打印了')
    try:
        logger.info('准备一下9999')
        print('99999999999')
        logger.info('打印完毕')
    except Exception as e:
        logger.error('打印出错了，报错信息是{}'.format(e))

