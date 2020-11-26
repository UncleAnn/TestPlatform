import os
from locust import task, HttpUser, between


# http://ws.webxml.com.cn/WebServices/MobileCodeWS.asmx
class WebServiceTest(HttpUser):
    host = 'http://ws.webxml.com.cn'
    wait_time = between(2, 2)

    @task
    def xml_test(self):
        # webservice无法自动识别content-type，需要手动添加
        xml_header = {'Content-type': 'text/xml'}
        phone_num = '13145899433'

        xml_data = f'''<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                <getMobileCodeInfo xmlns="http://WebXml.com.cn/">
                <mobileCode>{phone_num}</mobileCode>
                <userID></userID>
                </getMobileCodeInfo>
                </soap:Body>
                </soap:Envelope>'''
        with self.client.post(url='/WebServices/MobileCodeWS.asmx', data=xml_data, headers=xml_header,
                              name='webservice接口请求', catch_response=True, timeout=10) as response:
            resp = response.text
            # print(f'响应数据：{resp}')
            if phone_num in resp:
                response.success()
            else:
                response.failure('测试不通过')


if __name__ == '__main__':
    os.system('locust -f xml_locust_master.py --master')
