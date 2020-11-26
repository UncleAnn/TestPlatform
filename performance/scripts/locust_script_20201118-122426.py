from locust import HttpUser, task, between


class MyTest(HttpUser):
    host = 'https://www.baidu.com'
    wait_time = between(2, 2)

    @task
    def kv_test(self):
        # post请求参数，表单传给data，json字符串传给json
        with self.client.get(url='/', name='get请求', timeout=10, catch_response=True) as response:
            # text获取响应文本，json获取json类型的响应，content获取二进制的响应内容
            resp = response.text
            if 'success' in resp:
                response.success()
            else:
                response.failure('测试失败')