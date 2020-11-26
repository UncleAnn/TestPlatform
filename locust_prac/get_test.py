import os
from locust import TaskSet, HttpUser, task, between


# 任务类-继承任务类
class MyGetTask(TaskSet):
    url = '/'
    # 具体任务，需要加装饰器
    @task
    def get_test(self):
        # 发起请求
        # 用上下文管理器with发起请求，并把请求复制给一个变量
        with self.client.get(self.url, name='get接口', timeout=10, catch_response=True) as response:
            # 获取响应
            resp_str = response.text
            print(f'响应数据：{resp_str}')
            if 'baidu' in resp_str:
                # 请求成功
                response.success()
            else:
                # 请求失败
                response.failure(resp_str)


class MyGetUser(HttpUser):
    # 通过这个字段去关联任务类和用户类
    tasks = [MyGetTask]
    # 一些常规测试参数
    host = 'https://www.baidu.com/'
    wait_time = between(2, 2)


if __name__ == '__main__':
    os.system('locust -f get_test.py')