# import coverage
# cov = coverage.Coverage()
# cov.start()
from flask import Flask, render_template, redirect
from interface import interface
from variable import variable
from automation import automation
from performance import performance

app = Flask(__name__)
app.register_blueprint(interface, url_prefix='/interface')
app.register_blueprint(variable, url_prefix='/variable')
app.register_blueprint(automation, url_prefix='/automation')
app.register_blueprint(performance, url_prefix='/performance')


@app.route('/')
def rd():
    return redirect('index')


@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

#
# cov.stop()
# cov.save()
# cov.html_report()
