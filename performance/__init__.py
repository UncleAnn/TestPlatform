from flask import Blueprint, render_template, request, jsonify
from performance.service import Service

performance = Blueprint('performance', __name__, static_folder='performance_static',
                        template_folder='performance_templates')


@performance.route('/')
def index():
    return render_template('performance.html')


@performance.route('/api/v1/execute', methods=['POST'])
def api_v1_execute():
    data = request.get_json()
    code = data.get('code')
    if not code:
        return jsonify({
            'status_code': 400,
            'message': 'locust代码有误，请检查！',
            'data': data
        })
    # host = data.get('host')
    # if not host:
    #     return jsonify({
    #         'status_code': 400,
    #         'message': 'invalid parameter "host".',
    #         'data': data
    #     })
    Service().execute(data)
    return jsonify({
        'status_code': 200,
        'message': 'ok',
        'data': data
    })


