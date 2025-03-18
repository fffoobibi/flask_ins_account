import datetime
from peewee import *
from playhouse.mysql_ext import JSONField
from models import database, md_database


class UnknownField(JSONField):
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


class TblMarketingTotalResource(BaseModel):
    account_creation_date = IntegerField(null=True)
    adverts_mode = CharField(index=True, null=True)
    age_spread = UnknownField(null=True)  # json
    avatar = CharField(null=True)
    blackout_cause = CharField(null=True)
    category_id = IntegerField()
    category_notes = CharField(index=True, null=True)
    channel_analysis = TextField(null=True)
    channel_avg_likes = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    channel_avg_watchs = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    channel_avg_comments = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    channel_id = CharField(index=True, null=True)
    channel_interact_rate = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    channel_level = IntegerField(null=True)
    channel_name = CharField(index=True, null=True)
    channel_subscription = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    channel_url = CharField()
    channel_url_md5 = CharField(index=True, null=True)
    contact = CharField(null=True)
    content_direction = CharField()
    country = CharField(null=True)
    country_code = IntegerField()
    real_country_code = IntegerField(null=True)
    crawl_category_name = CharField(null=True)
    crawler_mode = IntegerField(null=True)
    create_time = IntegerField(index=True)
    creator = CharField()
    day_avg_uv = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    description = CharField(null=True)
    good_at_categories = UnknownField(null=True)  # json
    id = BigAutoField()
    is_blacklist = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_delete = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    last_crawler_time = IntegerField(null=True)
    last_update_time = IntegerField(null=True)
    note = CharField(null=True)
    offer = CharField(constraints=[SQL("DEFAULT '0.00'")], null=True)
    operate_time = IntegerField(null=True)
    operator = CharField(null=True)
    other_contact = CharField(null=True)
    platform = IntegerField()
    platform_type = IntegerField()
    resource_attr = IntegerField(null=True)
    resource_class = IntegerField(null=True)
    sex_spread = UnknownField(null=True)  # json
    store_method = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    user_id = IntegerField(null=True)
    user_spread = UnknownField(null=True)  # json
    videos = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    views = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    classified = IntegerField(constraints=[SQL("DEFAULT 0")])
    by_kol = IntegerField(constraints=[SQL("DEFAULT 0")])
    which_server = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    lang_code = CharField(null=True)
    database_type = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)

    class Meta:
        table_name = "tbl_marketing_total_resource"
        database = md_database


class TblInfluencerExtension(BaseModel):
    channel_id = CharField(index=True)
    channel_name = CharField()
    url = CharField(unique=True)
    country = CharField(null=True)
    fans = IntegerField(null=True)
    influencer_categories = CharField(index=True)
    keywords = CharField(index=True, null=True)
    tag = JSONField(null=True)
    create_time = DateTimeField(default=datetime.datetime.now, index=True)