import os
from locust import task, HttpUser, between


class DownloadTest(HttpUser):
    host = 'http://localhost:8080'
    wait_time = between(2, 2)

    @task
    def xml_test(self):
        download_param = {'id': 1}

        with self.client.get(url='/pinter/file/api/download', params=download_param, name='下载接口请求',
                             catch_response=True, timeout=10) as response:
            resp_bytes = response.content
            print(f'响应数据：{resp_bytes}')
            # if resp == '上传成功':
            #     response.success()
            # else:
            #     response.failure(resp)


if __name__ == '__main__':
    os.system('locust -f download_locust.py')
