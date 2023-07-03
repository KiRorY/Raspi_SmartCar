import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
import random


def send_email(sender='',password='',receiver=''):
    # 发件人信息
    sender = ''
    password = '' # 这里填QQ邮箱授权码

    # 收件人信息
    receiver = ''

    # 邮件内容

    message = MIMEMultipart()
    message['Subject'] = 'Test Email with Image'
    message['From'] = sender
    message['To'] = receiver
    text = MIMEText('树莓派智能车邮件发送测试', 'plain', 'utf-8')
    message.attach(text)

    # 添加图片

    img_dir = 'output'
    # 附件
    for filename in os.listdir(img_dir):
        with open(os.path.join(img_dir, filename),'rb') as f:
            image = MIMEImage(f.read(),'jpeg')
            image.add_header('Content-Disposition',f'attachment; filename={filename}')
            message.attach(image)

    image_files = [filename
    for filename in os.listdir(img_dir)]
    if image_files:
        # 随机预览一张图片
        preview_img = random.choice(image_files)
        with open(os.path.join(img_dir,preview_img),'rb') as f:
            image = MIMEImage(f.read(),'jpeg')
            image.add_header('Content-ID','<preview>')
            message.attach(image)

    # 直接预览图片
    html = """
    <html>
        <body>
            <p>树莓派智能车</p>
    """
    if image_files:
        html += '<p><img src=cid:preview></p>'

    html += """
        </body>
    </html>
    """

    text = MIMEText(html, 'html', 'utf-8')
    message.attach(text)

    # 连接到QQ邮箱SMTP服务器并发送邮件
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login(sender, password)
    server.sendmail(sender, receiver, message.as_string())
    server.quit()
