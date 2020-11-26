import os
from locust import task, HttpUser, between


class WebServiceTest(HttpUser):
    host = 'http://localhost:8080'
    wait_time = between(2, 2)

    @task
    def xml_test(self):
        file_data = {'file': open('xml_locust_master.py', 'rb')}

        with self.client.post(url='/pinter/file/api/upload', files=file_data, name='file上传接口请求',
                              catch_response=True, timeout=10) as response:
            resp = response.text
            print(f'响应数据：{resp}')
            if resp == '上传成功':
                response.success()
            else:
                response.failure(resp)


if __name__ == '__main__':
    os.system('locust -f file_locust.py')
