import os
from copy import deepcopy
from time import strftime, sleep
from common import send_email


class Service:
    def execute(self, data):
        """
        1、压测
        2、读取locust_stats.csv文件里的 请求总数、平均响应时间、最小响应时间、最大响应时间
        3、将以上字段提取，发送邮件
        :param data:
        :return:
        """
        code = data.get('code')
        # 存储文件的时间
        test_time = strftime('%Y%m%d-%H%M%S')
        CMD = "locust --headless -u {user} -r {rate} -t {time} --csv={stat_file_name} -f {locust_file}"
        # 拼接脚本和报告路径
        path = os.path.dirname(os.path.abspath(__file__))
        locust_file = os.sep.join([path, 'scripts', f'locust_script_{test_time}.py'])
        stat_file_path = os.sep.join([path, 'reports', test_time])
        os.mkdir(stat_file_path)
        stat_file_name = os.sep.join([stat_file_path, 'locust'])
        # 将code值存到文件中
        with open(locust_file, 'w', encoding='utf-8') as f:
            f.write(code)
        # 深拷贝一份data，用以格式化拼接
        fmt_data = deepcopy(data)
        fmt_data['stat_file_name'] = stat_file_name
        fmt_data['locust_file'] = locust_file
        cmd = CMD.format(**fmt_data)
        os.system(cmd)
        # 延时等待测试结束及报告生成
        sleep(int(fmt_data['time']) + 1)
        # 读取报告里的内容
        email_content = ""
        with open(os.sep.join([stat_file_path, 'locust_stats.csv']), 'r') as f:
            report_lines = f.readlines()
            print(report_lines)
            for line in report_lines[1:-2]:
                if line != '\n':
                    line = line.split(',')
                    email_content += f'''<h3>{line[1]}</h3>
                    <div>
                        <label>请求总数：{line[2]}</label>
                        <label>平均响应：{line[5]}</label>
                        <label>最小响应：{line[6]}</label>
                        <label>最大响应：{line[7]}</label>
                    </div><p>'''
        send_email('19865877121@163.com', email_content)
