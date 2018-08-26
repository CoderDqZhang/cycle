import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def person_id_validator(value):
    """
    对用户身份证进行自定义验证
    :param value:验证的字段值
    :return:身份格式不正确
    """
    ID_compile = re.compile(r'([A-Za-z](\d{6})\(\d\))|(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9]|X|x)$')
    if not ID_compile.match(value):
        raise ValidationError(u"身份证格式不正确")


def zip_code_validator(value):
    """
    对邮政编码进行自定义验证
    :param value: 验证的字段值
    :return:邮政编码格式不正确
    """
    zip_code = re.compile('^[0-9]\\d{5}$')
    if not zip_code.match(value):
        raise ValidationError(u"邮政编码格式不正确")


def password_validator(value):
    """
    对密码进行自定义验证
    :param value: 验证的字段值
    :return:以字母开头，长度在6~18之间，只能包含字符、数字和下划线
    """
    password = re.compile('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z_]{8,16}$')
    if not password.match(value):
        raise ValidationError(u'以字母开头，长度在6~18之间，只能包含字符、数字和下划线')


# person.py
#  from utils.model_field_validators import  person_id_validator
#    password = models.CharField(validators=[password_validator],max_length=100, verbose_name=u'密码', null=True, blank=True)
#   zip_code = models.CharField(validators=[zip_code_validator],max_length=50, verbose_name=u'邮政编码', null=True, blank=True)