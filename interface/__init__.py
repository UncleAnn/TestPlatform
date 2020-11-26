from flask import Blueprint, render_template, jsonify, request, g
from interface.service import Service
from common.mongo import MyMongo
from common import generate_id

interface = Blueprint('interface', __name__, static_folder='interface_static', template_folder='interface_templates')
mongo = MyMongo(host='127.0.0.1', port=27017)


@interface.route('/create')
def interface_create():
    return render_template('interface_create.html')


@interface.route('/edit/<id>')
def interface_edit(id):
    return render_template('interface_edit.html')


@interface.route('/suite')
def interface_suite():
    return render_template('interface_suite.html')


@interface.route('/api/v1/createSuite', methods=['POST'])
def interface_api_v1_create_suite():
    data = request.get_json()
    if not data.get('case_ids'):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter {case_ids}',
            'data': data
        })
    service = Service()
    result = service.create_suite(data)
    if '不存在' in result:
        return jsonify({
            'status': 400,
            'message': result,
            'data': data
        })
    return jsonify({
        'status': 200,
        'message': '创建成功',
        'data': data
    })


@interface.route('/api/v1/suite', methods=['POST'])
def interface_api_v1_suite():
    data = request.values.to_dict()
    service = Service()
    data = service.get_suites(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data
    })


@interface.route('/api/v1/deleteSuite', methods=['POST'])
def interface_api_v1_delete_suite():
    data = request.get_json()
    service = Service()
    if not data.get('id_list'):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter {id_list}',
            'data': data
        })
    result = service.delete_suite(data)
    if result == len(data['id_list']):
        return jsonify({
            'status': 200,
            'message': '删除成功',
            'data': data
        })
    else:
        return jsonify({
            'status': 200,
            'message': f'删除成功{result}个，失败{len(data["id_list"]) - result}个',
            'data': data
        })


@interface.route('/api/v1/runSuite', methods=['POST'])
def interface_api_v1_run_suite():
    data = request.get_json()
    # 为了能让flask的g对象进入，service对象生成必须在视图函数里而不是全局声明
    service = Service()
    if not data.get('id_list'):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter {id_list}',
            'data': data
        })
    report_id = service.trigger(data)
    if report_id:
        return jsonify({
            'status': 200,
            'message': '执行套件成功',
            'data': f'报告ID：{report_id}'
        })
    else:
        return jsonify({
            'status': 400,
            'message': '执行套件失败',
            'data': data
        })


@interface.route('/api/v1/search', methods=['POST'])
def interface_api_v1_search():
    data = request.get_json()
    service = Service()
    if not data.get('_id'):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter {_id}',
            'data': data
        })
    return jsonify({
        'status': 200,
        'message': 'ok',
        'data': service.get_interface_info(data)
    })


@interface.route('/list')
def interface_list():
    return render_template('interface_list.html')


@interface.route('/api/v1/delete', methods=['POST'])
def interface_api_v1_delete():
    data = request.get_json()
    service = Service()
    service.delete_interface(data)
    return jsonify({
        'status': 0,
        'message': '删除成功',
        'data': data['id_list']
    })


@interface.route('/api/v1/list', methods=['POST'])
def interface_api_v1_list():
    data = request.values.to_dict()
    service = Service()
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': service.get_interface_list(data)
    })


@interface.route('/api/v1/debug', methods=['POST'])
def interface_api_v1_debug():
    service = Service()
    data = request.get_json()
    return service.debug(data)


@interface.route('/api/v1/save', methods=['POST'])
def interface_api_v1_save():
    data = request.get_json()
    # 参数校验
    url = data.get('url')
    if not url:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter "url".',
            'data': data
        })
    method = data.get('method')
    if not method:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter "method".',
            'data': data
        })
    # 判断是新增还是修改后保存
    if data.get('_id'):
        mongo.update(database='interface', collection='cases', filter_condition={'_id': data['_id']}, document=data)
    else:
        # 生成唯一id
        data['_id'] = generate_id()
        print(data)
        # 存储数据
        mongo.insert(database='interface', collection='cases', document=data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data
    })


@interface.route('/report')
def interface_report():
    return render_template('interfaceReport.html')
