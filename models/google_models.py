from peewee import *

from models import database


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = database


class FlaskPlatformAccounts(BaseModel):
    account = CharField()
    account_type = IntegerField(null=True)
    can_use = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    create_time = DateTimeField(null=True)
    data = UnknownField(null=True)  # json
    day_use_count = IntegerField(null=True)
    email = CharField(null=True)
    key = CharField(null=True)
    note = CharField(null=True)
    passwd = CharField()
    is_delete = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = "flask_platform_accounts"


class ScrapySitesPlatformAccount(BaseModel):
    can_use = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    platform_account_id = IntegerField(null=True)
    scrapy_site_id = IntegerField(null=True)
    note = CharField(null=True)

    class Meta:
        table_name = "scrapy_sites_platform_account"
