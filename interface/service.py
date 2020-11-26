import requests
import re
from flask import jsonify, g
from interface.compare import Compare
from common import MyMongo, generate_id


class Service:

    def __init__(self):
        self.db = MyMongo('127.0.0.1', 27017)
        g.data = []

    @staticmethod
    def extract_value(data):
        # 单个case里的变量抽取，发起请求之后执行
        if data.get('extract'):
            extract_list = data['extract']
            for item in extract_list:
                name = item['extractValue']
                value = data['response']['data']
                try:
                    for part in item['extractExpr'].split('.'):
                        try:
                            value = value[str(part)]
                        except:
                            value = value[int(part)]
                except Exception as e:
                    return e
                g.data.append({'variable': name, 'value': value})

    def trigger(self, suite):
        # 触发套件
        suite_report = {}
        # 对套件列表进行循环
        for sid in suite['id_list']:
            suite_report[sid] = []
            # 获取单个套件里的所有case_id
            case_ids = self.db.search('interface', 'suites', {'_id': sid})[0]['case_ids']
            # 执行单个case
            for _id in case_ids:
                # 单个请求的所有参数封装为data，发起请求，response存入data中
                data = self.db.search('interface', 'cases', {'_id': _id})[0]
                self.debug(data)
                # 插入报告
                suite_report[sid].append(data)
        # 生成报告id
        total_report = {'_id': generate_id(), 'report': suite_report}
        # 保存报告
        return self.db.insert('interface', 'reports', total_report)

    def get_suites(self, data):
        filter_condition = {}
        if data.get('team'):
            filter_condition['team'] = data['team']
        if data.get('project'):
            filter_condition['project'] = data['project']
        data = self.db.search('interface', 'suites', filter_condition)
        case_ids_string = ''
        for suite in data:
            for case_id in suite['case_ids']:
                case_ids_string += case_id + ','
            suite['case_ids'] = case_ids_string[:-1]
        return data

    @staticmethod
    def assert_response(data):
        compare = Compare()
        response = data['response']
        # 对每个断言项进行断言
        for assert_item in data['assert']:
            assert_type = assert_item['assertType']
            expected = assert_item['assertValue']
            actual = response["data"]
            # 状态码只进行相等比较
            if assert_type == 'statusCode':
                actual = response['status_code']
                assert_item['result'] = str(actual) == expected
            else:
                try:
                    expr = re.match(r'\$\..+', assert_item['assertExpr']).group()
                except AttributeError as e:
                    print(e)
                else:
                    # $.data.cross_list.0.weight
                    for part in expr[2:].split('.'):
                        try:
                            actual = actual[str(part)]
                        except:
                            actual = actual[int(part)]
                assert_func = getattr(compare, assert_item['assertCondition'])
                assert_item.setdefault('result', assert_func(actual, expected))

    def debug(self, data):
        '''
        接口调试
        :param data: 传入带有所有接口参数的字典
        :return:
        '''
        # 参数校验
        if not data.get('url'):
            return jsonify({
                'status': 400,
                'message': 'invalid parameter "url".',
                'data': data
            })
        if not data.get('method'):
            return jsonify({
                'status': 400,
                'message': 'invalid parameter "method".',
                'data': data
            })
        # 解析变量
        # team = data['team']
        # project = data['project']
        self.replace_all_variables(data)
        self.replace_all_keywords(data)
        # 发起请求并断言
        self.send_request(data)
        self.assert_case(data)
        # 提取变量
        self.extract_value(data)
        # 生成返回给页面的响应文本
        return jsonify({
            'status_code': 200,
            'message': 'ok',
            'data': data
        })

    def assert_case(self, data):
        if 'assert' in data:
            self.assert_response(data)

    # def get_variables(self, case_data, team, project):
    def get_variables(self, case_data):
        # 获取数据库中的变量
        filter_condition = {'team': case_data['team'], 'project': case_data['project']}
        variables = self.db.search('variable', 'variables', filter_condition)
        # 提取变量
        variables.extend(g.data)
        # 返回总变量列表
        return variables

    def parse_variable(self, org_string, replace_variables):
        """
        将${变量名}解析成原始字符串
        :param org_string: 解析前的带{变量名}的字符串
        :return: parse_string：解析后的字符串
        """
        variable_to_replace = re.findall(r'\$\{\w+\}', org_string)
        if variable_to_replace:
            for var in variable_to_replace:
                try:
                    for variable in replace_variables:
                        if var[2:-1] == variable['variable']:
                            return org_string.replace(var, str(variable['value']))
                except Exception as e:
                    print(e)
        return org_string

    def parse_keyword(self, org_string):
        """
        将@{关键字}解析成关键字执行后的结果
        :param org_string: 解析前的带${关键字}的字符串
        :return: parse_string：解析后的字符串
        """
        keywords_to_replace = re.findall(r'\@\{\w+\}', org_string)
        if keywords_to_replace:
            for var in keywords_to_replace:
                try:
                    for keyword in self.db.search('variable', 'keywords', {}):
                        if var[2:-1] == keyword['name']:
                            exec(keyword['snippet'], keyword['mock'])
                            return org_string.replace(var, keyword['mock']['result'])
                except Exception as e:
                    print(e)
        return org_string

    def replace_all_variables(self, data):
        replace_variables = self.get_variables(data)
        if data.get('url'):
            data['url'] = self.parse_variable(data['url'], replace_variables)
        if data.get('description'):
            data['description'] = self.parse_variable(data['description'], replace_variables)
        if data.get('header'):
            for item in data['header'].keys():
                data['header'][item] = self.parse_variable(data['header'][item], replace_variables)
        if data.get('params'):
            for item in data['params'].keys():
                data['params'][item] = self.parse_variable(data['params'][item], replace_variables)

    def replace_all_keywords(self, data):
        if data.get('url'):
            data['url'] = self.parse_keyword(data['url'])
        if data.get('description'):
            data['description'] = self.parse_keyword(data['description'])
        if data.get('header'):
            for item in data['header'].keys():
                data['header'][item] = self.parse_keyword(data['header'][item])
        if data.get('params'):
            for item in data['params'].keys():
                data['params'][item] = self.parse_keyword(data['params'][item])

    @staticmethod
    def send_request(data):
        kwargs = {}
        # 对http的请求头做校验
        if data.get('header'):
            kwargs['headers'] = data['header']
        # 对http的请求参数做校验
        if data.get('params'):
            kwargs['params'] = data['params']
        # 解析变量
        response = requests.request(method=data['method'], url=data['url'], **kwargs)
        # 请求成功后，将请求结果追加到入参的字典中
        data['response'] = {
            'status_code': response.status_code,
            'message': 'ok',
            'data': response.json()
        }
        return response.json()

    def get_interface_info(self, data):
        return self.db.search('interface', 'cases', data)

    def get_interface_list(self, data):
        team = data.get('team')
        project = data.get('project')
        filter_condition = {}
        if team:
            filter_condition['team'] = team
        if project:
            filter_condition['project'] = project
        return self.db.search('interface', 'cases', filter_condition)

    def create_suite(self, data):
        # 先判断case id是否都存在
        for _id in data['case_ids']:
            result = self.db.search('interface', 'cases', {'_id': _id})
            if not result:
                return f'接口{_id}不存在！'
        data['_id'] = generate_id()
        return self.db.insert('interface', 'suites', data)

    def delete_interface(self, data):
        count = 0
        for _id in data['id_list']:
            count += self.db.delete('interface', 'cases', {'_id': _id})
        return count

    def delete_suite(self, data):
        count = 0
        for _id in data['id_list']:
            count += self.db.delete('interface', 'suites', {'_id': _id})
        return count


if __name__ == '__main__':
    service = Service()
    print(service.get_interface_list({'team': 'all'}))
    print()
    print(service.get_interface_list({'team': '质量管理部', 'project': 'all'}))
    print()
    print(service.get_interface_list({'team': '质量管理部', 'project': '深目测试组'}))
