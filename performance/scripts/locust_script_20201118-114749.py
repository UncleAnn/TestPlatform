from locust import HttpUser, task, between


class MyTest(HttpUser):
    host = 'http://localhost:8080/pinter'
    wait_time = between(2, 2)

    @task
    def kv_test(self):
        post_data = {
            'userName': 'admin',
            'password': '1234'
        }
        # post请求参数，表单传给data，json字符串传给json
        with self.client.post(url='/com/login', data=post_data, name='参数为k-v的post接口', timeout=10,
                              catch_response=True) as response:
            # text获取响应文本，json获取json类型的响应，content获取二进制的响应内容
            resp = response.json()
            print(f'参数k-v响应数据为：{resp}')
            if resp['message'] == 'success':
                response.success()
            else:
                response.failure('测试失败')