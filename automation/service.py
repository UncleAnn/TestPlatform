import os
from common.mongo import MyMongo
from automation.keywordFunc import Keyword


class Service:

    def __init__(self):
        self.db = MyMongo('127.0.0.1', 27017)
        self.kw = Keyword()

    def run_ui_test(self, data):
        """
        执行单个UI测试脚本
        :param data: 列表嵌套字典
        :return:
        """
        os.system('taskkill /F /IM chromedriver.exe')
        script_result = True
        op_result_list = []
        for op in data:
            try:
                el = (op['by'], op['locator'])
                func = getattr(self.kw, op['type'])
                func(el, op['data'])
                op_result_list.append(True)
            except:
                script_result = False
                op_result_list.append(False)
                break
        return {
            'result_list': op_result_list,
            'test_result': script_result
        }

