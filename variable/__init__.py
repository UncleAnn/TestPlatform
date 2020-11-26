import json
import re
from flask import Blueprint, jsonify, request, render_template
from variable.service import Service

variable = Blueprint('variable', __name__, static_folder='variable_static', template_folder='variable_templates')
service = Service()


@variable.route('/')
def index():
    return render_template('variable.html')


@variable.route('/keyword')
def keyword():
    return render_template('keyword.html')


@variable.route('/api/v1/debug', methods=['POST'])
def api_v1_debug():
    data = request.get_json()
    service = Service()
    return service.keyword_debug(data)


@variable.route('/api/v1/save', methods=['POST'])
def api_v1_save():
    data = request.get_json()
    service = Service()
    return service.keyword_save(data)


@variable.route('/api/v1/search', methods=['POST'])
def api_v1_search():
    data = request.values.to_dict()
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': service.search(data)
    })


@variable.route('/api/v1/insert', methods=['POST'])
def api_v1_insert():
    data = request.get_json()
    if not data.get('team'):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter {team}'
        })
    if not data.get('project'):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter {project}'
        })
    print(data)
    return jsonify({
        'status': 0,
        'message': '新增成功',
        'data': service.insert(data)
    })


@variable.route('/api/v1/update', methods=['POST'])
def api_v1_update():
    data = request.get_json()
    if not data.get('team'):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter {team}'
        })
    if not data.get('project'):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter {project}'
        })
    if not data.get('variable'):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter {variable}'
        })
    if not data.get('value'):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter {value}'
        })
    return jsonify({
        'status': 0,
        'message': '修改成功',
        'data': service.update(data)
    })


@variable.route('/api/v1/delete', methods=['POST'])
def api_v1_delete():
    data = request.get_json()
    print(data)
    del_count = 0
    fail_count = 0
    for _id in data['id_list']:
        if service.delete({'_id': _id}):
            del_count += 1
        else:
            fail_count += 1
    if fail_count:
        return jsonify({
            'status': 0,
            'message': f'删除{del_count}个变量成功，删除{fail_count}个变量失败。',
            'data': data
        })
    else:
        return jsonify({
            'status': 0,
            'message': f'成功删除{del_count}个变量',
            'data': data
        })


@variable.route('/api/v1/searchProject', methods=['POST'])
def api_v1_search_project():
    data = request.get_json()
    if not data.get('type'):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter {type}',
            'data': data
        })
    if not data.get('team'):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter {team}',
            'data': data
        })
    try:
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': service.search_project(data)
        })
    except Exception as e:
        return jsonify({
            'status': 400,
            'message': str(e),
            'data': data
        })


@variable.route('/api/v1/aggregate', methods=['POST'])
def api_v1_aggregate():
    data = request.get_json()
    if not data.get('type'):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter {type}',
            'data': data
        })
    if not data.get('key'):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter {key}',
            'data': data
        })

    # 聚合逻辑处理
    try:
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': service.aggregate(data)
        })
    except Exception as e:
        return jsonify({
            'status': 400,
            'message': str(e),
            'data': data
        })
