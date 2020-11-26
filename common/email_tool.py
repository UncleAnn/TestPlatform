from email.header import Header
from email.mime.text import MIMEText
import smtplib

common_email = '13145899433@163.com'
password = 'EEEEHDPZVQQFKGYW'


def smtp_service(receiver, message):
    # 具体创建的smpt的服务及发送邮件的封装
    try:
        smpt = smtplib.SMTP()
        smpt.connect('smtp.163.com')
        # 登录邮箱
        smpt.login(common_email, password)
        smpt.sendmail(common_email, receiver, message.as_string())
        print(f'send email to {receiver} success.')
    except Exception as e:
        print(e)
        print(f'send email to {receiver} failed.')


def send_email(receiver, template, title='测试平台邮件推送'):
    # 供外界调用的接口
    message = MIMEText(template, 'html', 'utf-8')
    message['From'] = common_email
    message['To'] = receiver
    message['Subject'] = Header(title, 'utf-8')
    smtp_service(receiver, message)

