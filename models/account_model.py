import datetime
from peewee import *
from playhouse.mysql_ext import JSONField
from models import database


class UnknownField(object):
    pass


class BaseModel(Model):
    # pass
    class Meta:
        database = database


class TblPlatformAccount(BaseModel):
    account_type = IntegerField()
    bind_email = CharField(null=True)
    bind_email_password = CharField(null=True)
    can_use = IntegerField()
    comment = CharField(null=True)
    create_time = IntegerField(null=True)
    modify_time = IntegerField(null=True)
    password = CharField()
    username = CharField()
    proxy_ip = CharField()
    session = JSONField()
    note = TextField()

    class Meta:
        table_name = "tbl_platform_account"


class TblScrapySite(BaseModel):
    site_url = CharField(max_length=120, unique=True)
    site_account = CharField(max_length=50)
    site_passwd = CharField(max_length=255)
    note = CharField(max_length=255)
    create_time = DateTimeField(default=datetime.datetime.now)
    project = CharField(max_length=50)
    proxy = CharField(max_length=50)

    class Meta:
        table_name = "tbl_scrapy_sites"


class TblScrapyVisits(BaseModel):
    which_server = IntegerField()
    crawler_name = CharField(max_length=255)
    crawler_visits = BigIntegerField()
    create_time = DateTimeField(default=datetime.datetime.now, index=True)
    modify_time = DateTimeField()
    comment = CharField(max_length=255)

    class Meta:
        table_name = "tbl_scrapy_visits_statistics"
    


class TblCategory(BaseModel):
    like_keywords = TextField(null=True)
    name = CharField(null=True)
    pid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "tbl_category"
