import datetime
import time
import psutil
import socket
from common.mongo import MyMongo


class Agent:
    def __init__(self):
        self.mongo = MyMongo('127.0.0.1', '27017')

    @staticmethod
    def get_ip():
        # 通过socket库可以获取机器名，通过机器名可以获取ip地址
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)

    @staticmethod
    def get_cpu():
        # interval获取cpu数据的时间间隔，percpu为True时返回机器多核数据
        # data的值是[9.2, 6.2, 25.0, 9.4, 10.9, 0.0, 1.6, 1.6, 1.6, 7.8, 3.1, 3.1]
        result = {}
        data = psutil.cpu_percent(interval=1, percpu=True)
        # cpu的总数据
        result['data'] = data
        print(f'data的值是{data}')
        # CPU平均负载：cpu的总数据/cpu的核数
        result['avg'] = sum(data) / psutil.cpu_count()
        # cpu的总空闲值
        result['idle'] = 100 - result['avg']
        print(result)

    @staticmethod
    def get_memory():
        result = {}
        # 获取系统内存的使用情况，symem对象
        # svmem(total=8457662464, available=3598602240, percent=57.5, used=4859060224, free=3598602240)
        data = psutil.virtual_memory()
        print(f'当前已使用内存：{data}')
        # 内存总量
        result['total'] = data.total
        # 已使用内存
        result['used'] = data.used
        # 可用内存
        result['available'] = data.available
        # 使用百分比
        result['percent'] = data.percent
        return result

    @staticmethod
    def get_disk():
        result = {
            'total': 0,
            'used': 0,
            'available': 0,
            'percent': 0
        }
        # 先获取硬盘分区，再跟进分区获取硬盘信息，Mac这里直接用/代替disk_partitions()
        partitions = psutil.disk_partitions()
        # 计算每一个分区的数据，然后汇总成硬盘使用总量
        for partition in partitions:
            # 分区信息总览
            print('partition：', partition)
            # 磁盘使用情况
            data = psutil.disk_usage(partition.device)
            print('disk_usage：', data)
            # 磁盘使用情况-单项
            result['total'] += data.total
            result['used'] += data.used
            result['available'] += data.free
        # 磁盘总使用率
        result['percent'] = 100 * result['used'] / result['total']
        print(result)
        return result

    @staticmethod
    def get_network():
        # 获取网卡接受与发送的bytes和packet数据。
        # snetio(bytes_sent=3398615, bytes_recv=14170744,
        # packets_sent=28431, packets_recv=25604, errin=0, errout=255, dropin=0, dropout=0)
        result = {
            'bytes': {},
            'packets': {}
        }
        # 网络概况
        data = psutil.net_io_counters()
        print(data)
        # 收发字节数和收发包数
        result['bytes']['sent'] = data.bytes_sent
        result['bytes']['receive'] = data.bytes_recv
        result['packets']['sent'] = data.packets_sent
        result['packets']['receive'] = data.packets_recv

        return result

    # 入口函数
    def monitor(self, interval=10):
        collection = self.get_ip()
        while True:
            result = {
                'time': datetime.datetime.now(),
                'cpu': self.get_cpu(),
                'memory': self.get_memory(),
                'disk': self.get_disk(),
                'network': self.get_network(),
            }
            # if result['cpu']['avg'] > 20:
            #    send_email("3512937625@qq.com", "<h1>CPU使用率大于20%，实际是{0}</h1>".format(result['cpu']['avg']))
            print("将机器{0}数据写入数据库\n{1}".format(collection, result))
            # self.mongo.insert("monitor", collection, result)
            time.sleep(interval)


if __name__ == '__main__':
    agent = Agent()
    # agent.monitor()
    # agent.get_ip()
    # agent.get_cpu()
    # agent.get_disk()
    # agent.get_memory()
    agent.get_network()
