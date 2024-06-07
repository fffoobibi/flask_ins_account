import random

from setting import CACHE_REDIS_SETTINGS
from flask import Blueprint, request, jsonify
from flask_caching import Cache

from logger import logger
from models.account_model import TblScrapySite
from models.google_models import FlaskPlatformAccounts, ScrapySitesPlatformAccount
from utils import format_datetime_fields


def make_cache_key(*args, **kwargs):
    site_id = request.json.get("site_id")
    account_type = request.json.get("account_type", 2)
    return f"site_id_{site_id}_account_type_{account_type}"


google_app = Blueprint("google_app", __name__)
config = CACHE_REDIS_SETTINGS.copy()
cache = Cache(config=config)


@google_app.errorhandler(Exception)
def handler_error(error):
    logger.error("error", exc_info=True)
    return {"code": -1, "msg": str(error)}


@google_app.before_request
def check_token():
    token = request.headers.get("check-token")
    if token != "1C168F31197B4C4F":
        return jsonify({"error": "Invalid token"}), 401


@google_app.get("/simple_account_list")
def simple_account_list():
    rs = list(
        FlaskPlatformAccounts.select()
        .where(FlaskPlatformAccounts.is_delete == 0)
        .dicts()
        .order_by(FlaskPlatformAccounts.account_type)
    )
    return {"code": 0, "msg": "success", "data": rs}


@google_app.get("/account_list")
def account_list():
    resp = FlaskPlatformAccounts.select().dicts()
    rs = list(resp)
    for v in rs:
        v["sites"] = list(
            TblScrapySite.select(
                TblScrapySite.id, TblScrapySite.site_url, TblScrapySite.note
            )
            .join(
                ScrapySitesPlatformAccount,
                on=(TblScrapySite.id == ScrapySitesPlatformAccount.scrapy_site_id),
            )
            .where(ScrapySitesPlatformAccount.platform_account_id == v["id"])
            .dicts()
        )
    return {"code": 0, "data": rs}


@google_app.post("/add_accounts")
def add_platform_account():
    data = request.json.get("data")
    success = 0
    total = len(data)
    for value in data:
        try:
            FlaskPlatformAccounts.insert(value).execute()
            success += 1
        except:
            pass
    return {"code": 0, "msg": f"已添加{success}个账号, 共{total}个账号"}


@google_app.post("/modify_account")
def modify_account():
    account_id = request.json.get("account_id")
    modify_data = request.json.get("modify_data")
    FlaskPlatformAccounts.update(modify_data).where(
        FlaskPlatformAccounts.id == account_id
    ).execute()
    return {"code": 0, "msg": "success"}


@google_app.post("/get_account")
@cache.cached(make_cache_key=make_cache_key, timeout=3600 * 24 * 14)
def get_account():
    site_id = request.json.get("site_id")
    account_type = request.json.get("account_type", 2)
    flask_accounts = (
        FlaskPlatformAccounts.select()
        .join(
            ScrapySitesPlatformAccount,
            on=(
                FlaskPlatformAccounts.id
                == ScrapySitesPlatformAccount.platform_account_id
            ),
        )
        .join(
            TblScrapySite,
            on=(TblScrapySite.id == ScrapySitesPlatformAccount.scrapy_site_id),
        )
        .where(
            FlaskPlatformAccounts.is_delete == 0,
            FlaskPlatformAccounts.account_type == account_type,
            FlaskPlatformAccounts.can_use == 1,
            ScrapySitesPlatformAccount.can_use == 1,
            TblScrapySite.id == site_id,
        )
        .dicts()
    )
    rs = list(flask_accounts)
    if rs:
        return {"code": 0, "data": random.choice(rs), "msg": "success"}
    else:
        return {"code": 0, "data": None, "msg": "无可用账号"}


@google_app.get("/sites_list")
def sites_list():
    sites = TblScrapySite.select(
        TblScrapySite.id,
        TblScrapySite.site_url,
        TblScrapySite.site_account,
        TblScrapySite.site_passwd,
        TblScrapySite.note,
        TblScrapySite.create_time,
    ).dicts()
    rs = list(sites)
    for v in rs:
        v["accounts"] = list(
            FlaskPlatformAccounts.select()
            .join(
                ScrapySitesPlatformAccount,
                on=(
                    FlaskPlatformAccounts.id
                    == ScrapySitesPlatformAccount.platform_account_id
                ),
            )
            .where(ScrapySitesPlatformAccount.scrapy_site_id == v["id"])
            .order_by(FlaskPlatformAccounts.account_type)
            .dicts()
        )

    return {
        "code": 0,
        "data": format_datetime_fields(rs, ["create_time"]),
        "msg": "success",
    }


@google_app.post("/bind_site_account")
def bind_site_account():
    site_id = request.json.get("site_id")
    account_ids = request.json.get("account_ids")

    rsp = list(
        FlaskPlatformAccounts.select(
            FlaskPlatformAccounts.id, FlaskPlatformAccounts.account_type
        )
        .where(FlaskPlatformAccounts.id.in_(account_ids))
        .dicts()
    )
    ScrapySitesPlatformAccount.delete().where(ScrapySitesPlatformAccount.scrapy_site_id==site_id).execute()
    for v in rsp:
        account_type = v["account_type"]
        account_id = v["id"]
        cache.delete(f"site_id_{site_id}_account_type_{account_type}")
        ScrapySitesPlatformAccount.insert(
            {
                ScrapySitesPlatformAccount.scrapy_site_id: site_id,
                ScrapySitesPlatformAccount.platform_account_id: account_id,
            }
        ).execute()
    return {"code": 0, "msg": "success"}


@google_app.post("/modify_site_account")
def modify_site_account():
    site_id = request.json.get("site_id")
    account_id = request.json.get("account_id")
    can_use = request.json.get("can_use")
    data = request.json.get("data", None)
    account_type = FlaskPlatformAccounts.get(account_id).account_type
    cache.delete(f"site_id_{site_id}_account_type_{account_type}")
    ScrapySitesPlatformAccount.update(can_use=can_use).where(
        ScrapySitesPlatformAccount.scrapy_site_id == site_id,
        ScrapySitesPlatformAccount.platform_account_id == account_id,
    ).execute()
    if data is not None:
        FlaskPlatformAccounts.update({FlaskPlatformAccounts.data: data}).where(
            FlaskPlatformAccounts.id == account_id
        ).execute()
    return {"code": 0, "msg": "success"}
