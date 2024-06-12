from peewee import *
from playhouse.mysql_ext import JSONField
from models import md_hub_database


class UnknownField(JSONField):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = md_hub_database


class TblKolVideo(BaseModel):
    channel_id = CharField(null=True)
    crawl_time = IntegerField(null=True)
    digg_count = IntegerField(null=True)
    follower_count = IntegerField(null=True)
    following_count = IntegerField(null=True)
    heart = IntegerField(null=True)
    heart_count = IntegerField(null=True)
    id = BigAutoField()
    is_dh = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    kol_id = BigIntegerField(index=True)
    thumbnail_local = CharField(null=True)
    video_category = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    video_comment_count = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    video_count = IntegerField(null=True)
    video_description = TextField(null=True)
    video_dislike_count = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    video_id = CharField(index=True, null=True)
    video_like_count = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    video_publish_date = IntegerField(index=True, null=True)
    video_tags = TextField(null=True)
    video_thumbnail = CharField(null=True)
    video_title = CharField(index=True, null=True)
    video_url = CharField(null=True)
    video_view_count = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = "tbl_kol_video"
