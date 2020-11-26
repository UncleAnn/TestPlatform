from flask import render_template, request, jsonify, Blueprint
from automation.service import Service

automation = Blueprint('automation', __name__, static_folder='automation_static',
                       template_folder='automation_templates')


@automation.route('/create')
def create():
    return render_template('automation_create.html')


@automation.route('/api/v1/run', methods=['POST'])
def api_v1_run():
    service = Service()
    data = request.get_json()
    result = service.run_ui_test(data)
    return jsonify({
        'status_code': 200,
        'message': 'ok',
        'data': result
    })
