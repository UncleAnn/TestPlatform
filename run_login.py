# import coverage
# cov = coverage.Coverage()
# cov.start()
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from login import get_user_info
from interface import interface
from variable import variable
from automation import automation
from performance import performance

app = Flask(__name__)
app.secret_key = 'Erased'
app.register_blueprint(interface, url_prefix='/interface')
app.register_blueprint(variable, url_prefix='/variable')
app.register_blueprint(automation, url_prefix='/automation')
app.register_blueprint(performance, url_prefix='/performance')

# 实例化登录管理对象，并初始化应用
login_manager = LoginManager()
login_manager.init_app(app)
# 设置用户登录视图函数，即验证失败时要跳转的页面
login_manager.login_view = 'login'


class User(UserMixin):
    pass


@app.route('/')
def rd():
    return redirect('index')


@app.route('/index')
def index():
    return render_template('index.html')
    # return render_template('index.html', curr_user=current_user.username)


@login_manager.user_loader
def user_loader(username):
    """根据 Session 信息加载登录用户，返回用户实例"""
    # 在每次请求过来后，Flask-Login都会从Session中寻找”user_id”的值
    # 如果找到的话，就会用这个”user_id”值来调用此回调函数，并构建一个用户类对象。
    curr_user_info = get_user_info(username)
    if not curr_user_info:
        return
    curr_user = User()
    curr_user.id = curr_user_info['_id']
    curr_user.username = curr_user_info['username']
    return curr_user


@login_manager.request_loader
def request_loader(request):
    # 如果Cookie被禁用了怎么办？
    # 只能通过请求参数将用户信息带过来，一般情况下会使用一个动态的Token来表示登录用户的信息。
    print('进入了request_loader')
    data = request.get_json()
    username = data.get('username')
    user_info = get_user_info(username)
    if not user_info:
        return
    curr_user = User()
    curr_user.id = user_info['_id']
    curr_user.is_authenticated = check_password_hash(user_info['password'], data['password'])
    return curr_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    # GET请求，渲染登录页面
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return render_template('login.html', curr_user=current_user)
        else:
            return redirect(request.values.get('next'))
    # POST请求，登录
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_info = get_user_info(username)
    # 校验密码
    is_login_success = check_password_hash(user_info.get('password'), password)
    # print('是否成功登录：', is_login_success)
    if is_login_success:
        # 密码正确，创建用户session。remember开启“记住我”
        # 创建用户实体
        user = User()
        user.id = user_info['_id']
        user.username = user_info['username']
        login_user(user, remember=True)
        print('登录后的认证状态：', user.is_authenticated)
        # 如果请求中有next参数，则重定向到其指定的地址，
        # 没有next参数，则重定向到"index"视图
        return jsonify({
            'status_code': 200,
            'message': '登录成功！',
            'data': user.username
        })
    else:
        # flash('用户名或密码错误！')
        return jsonify({
            'status_code': 400,
            'message': '用户名或密码错误！'
        })


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user', methods=['POST'])
# @login_required
def user():
    if current_user.is_authenticated:
        user_data = {'username': current_user.username}
        print(user_data)
        return jsonify(user_data)
    return jsonify({'username': '未登录'})


# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return redirect(url_for('login'))

# @app.route('/sign_up', methods=['POST'])
# def sign_up():
#     data = request.get_json()
#     if not data.get('username'):
#         return jsonify({
#             'status_code': 400,
#             'message': 'invalid parameter "username".'
#         })
#     if not data.get('password'):
#         return jsonify({
#             'status_code': 400,
#             'message': 'invalid parameter "password".'
#         })
#
#     return None


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

#
# cov.stop()
# cov.save()
# cov.html_report()
