from users.models import EmailVerifyRecord
from django.core.mail import send_mail
import random
import string

#生成8位的随机字符串
def random_str(randomlength=8):
    chars = string.ascii_letters + string.digits #生成a-z 0-9的字符串
    strcode = ''.join(random.sample(chars, randomlength))  #生成8位的随机字符串
    return strcode

def send_register_mail(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        title = '博客注册激活链接'
        body = '请点击一下链接激活账号: htto://127.0.0.1:8000/users/active/{0}'.format(code)

        send_status = send_mail(title,body,'309415794@qq.com',[email])
        if send_status:
            pass