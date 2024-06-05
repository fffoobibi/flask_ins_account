from flask import Blueprint, request, jsonify
from utils import validate_token
from models.google_models import FlaskPlatformAccounts, ScrapySitesPlatformAccount
from models.account_model import TblScrapySite
from logger import logger

google_app = Blueprint("google_app", __name__)


@google_app.errorhandler(Exception)
def handler_error(error):
    logger.error('error', exc_info=True)
    return {"code": -1, "msg": str(error)}


@google_app.before_request
def check_token():
    token = request.headers.get("check-token")
    if token != "1C168F31197B4C4F":
        return jsonify({"error": "Invalid token"}), 401


@google_app.get("/account_list")
def account_list():
    # resp = (
    #     FlaskPlatformAccounts.select(
    #         FlaskPlatformAccounts, ScrapySitesPlatformAccount.scrapy_site_id.alias('site_id'), TblScrapySite.site_url, TblScrapySite.note.alias('site_note')
    #     )
    #     .join(
    #         ScrapySitesPlatformAccount,
    #         on=(
    #             FlaskPlatformAccounts.id
    #             == ScrapySitesPlatformAccount.platform_account_id
    #         ),
    #     )
    #     .join(
    #         TblScrapySite,
    #         on=(TblScrapySite.id == ScrapySitesPlatformAccount.scrapy_site_id),
    #         attr="sites",
    #     )
    #     .dicts().order_by(FlaskPlatformAccounts.id)
    # )
    
    resp = FlaskPlatformAccounts.select().dicts()
    rs = list(resp)
    
    # ret = []
    # keys = {}
    # for v in rs:
    #     if keys.get(v['id']):
    #         pass
    #     else:
    #         keys[v['id']] = v
    #         value = keys.setdefault(v['id'], v)
    
    #     sites = {}
    #     sites["site_id"] =value.pop('site_id')
    #     sites["site_note"] =value.pop('site_note')
    #     sites["site_url"] =value.pop('site_url')
        
    #     ret.append(v)
    
    for v in rs:
        TblScrapySite.select(FlaskPlatformAccounts).join(ScrapySitesPlatformAccount, on=(TblScrapySite.id==ScrapySitesPlatformAccount.scrapy_site_id))
    return {"code": 0, "data": rs}


@google_app.post("/add_accounts")
def add_platform_account():
    data = request.json.get("data")
    FlaskPlatformAccounts.insert_many(data).execute()
    return {"code": 0, "msg": "success"}


@google_app.post("/modify_account")
def modify_account():
    account_id = request.json.get("account_id")
    modify_data = request.json.get("modify_data")
    FlaskPlatformAccounts.update(modify_data).where(
        FlaskPlatformAccounts.id == account_id
    ).execute()
    return {"code": 0, "msg": "success"}
