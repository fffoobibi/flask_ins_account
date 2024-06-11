import datetime
import json

import redis
from flask import Flask, request, jsonify

from google_app import google_app, cache
from models.account_model import (
    TblMarketingTotalResource,
    TblPlatformAccount,
    TblScrapySite,
    TblScrapyVisits,
    TblCategory,
)
from utils import validate_token
from scheduler import init_schduler

app = Flask(__name__)
app.register_blueprint(google_app, url_prefix="/google")
cache.init_app(app)

redis_client = redis.StrictRedis(
    **{
        "host": "36.32.174.26",
        "password": "b=!@#--pfdnzzxsj2kdgjm",
        "port": 5003,
        "db": 0,
    }
)


# @app.before_request
# def bf():
#     database.connect()
#
#
# @app.teardown_request
# def teardown(exc):
#     if database.is_closed() is False:
#         database.close()


@app.get("/categories")
@validate_token
def get_categories():
    data = TblCategory.select().dicts()
    return {"data": list(data)}


@app.post("/modifty_category")
@validate_token
def modifty_category():
    data_id = request.json.get("id")
    category_id = request.json.get("category_id")
    TblMarketingTotalResource.update(
        category_id=category_id, store_method=4, database_type=2
    ).where(TblMarketingTotalResource.id == data_id).execute()
    return {"code": 0, "msg": "success"}


@app.get("/flat_categories")
@validate_token
def get_flat_categories():
    resp = list(TblCategory.select().dicts())
    keys = {}
    for v in resp:
        if v["pid"] == 0:
            value = keys.setdefault(
                v["id"],
                {
                    "name": v["name"],
                    "id": v["id"],
                    "subs": [],
                },
            )
        else:
            value = keys[v["pid"]]
            value["subs"].append(v)

    return {"data": list(keys.values())}


@app.post("/submit_influence")
@validate_token
def submit_influence():
    import json

    with redis_client.pipeline() as pipe:
        for v in request.json.get("data"):
            pipe.lpush(
                "influencer_nickname_list:start_urls", json.dumps(v, ensure_ascii=False)
            )
            pipe.execute()
    return {"code": 0, "msg": "success"}


@app.route("/")
@validate_token
def hello_world():  # put application's code here
    return "Hello World!"


@app.route("/add_account", methods=["POST"])
@validate_token
def add_account():
    username = request.form.get("username")
    password = request.form.get("password")
    bind_email = request.form.get("bind_email")
    bind_email_password = request.form.get("bind_email_password")
    can_use = request.form.get("can_use")
    account_type = request.form.get("account_type")
    comment = request.form.get("comment")
    create_time = request.form.get("create_time")
    modify_time = request.form.get("modify_time")
    proxy_ip = request.form.get("proxy_ip")
    account_info = {
        "username": username,
        "password": password,
        "bind_email": bind_email,
        "bind_email_password": bind_email_password,
        "can_use": can_use,
        "account_type": account_type,
        "comment": comment,
        "create_time": create_time,
        "modify_time": modify_time,
        "proxy_ip": proxy_ip,
    }
    try:
        TblPlatformAccount.insert(account_info).on_conflict_ignore().execute()
        return (
            jsonify({"code": 0, "msg": "成功"}),
            200,
            {"Content-Type": "application/json; charset=utf-8"},
        )
    except:
        return (
            jsonify({"code": 1, "msg": "失败"}),
            400,
            {"Content-Type": "application/json; charset=utf-8"},
        )


@app.route("/get_account")
@validate_token
def get_account():
    server_ip = request.args.get("server_ip", "54.209.179.134")
    item = TblPlatformAccount.get_or_none(
        TblPlatformAccount.can_use == 1, TblPlatformAccount.proxy_ip == server_ip
    )
    if item is not None:
        account = {
            "username": item.username,
            "password": item.password,
            "email": item.bind_email,
            "email_password": item.bind_email_password,
            "session": item.session,
            "proxy_ip": item.proxy_ip,
        }

        return json.dumps(account)
    else:
        return json.dumps({"username": None})


@app.route("/get_add_user_account")
@validate_token
def get_add_user_account():
    server_ip = request.args.get("server_ip", "18.210.200.217")
    item = TblPlatformAccount.get_or_none(
        TblPlatformAccount.can_use == 5, TblPlatformAccount.proxy_ip == server_ip
    )
    if item is not None:
        account = {
            "username": item.username,
            "password": item.password,
            "email": item.bind_email,
            "email_password": item.bind_email_password,
            "session": item.session,
            "proxy_ip": item.proxy_ip,
        }

        return json.dumps(account)
    else:
        return json.dumps({"username": None})


@app.route("/modify_account", methods=["POST"])
@validate_token
def modify_account():
    can_use = request.form.get("can_use")
    username = request.form.get("username")
    session = request.form.get("session")
    try:
        TblPlatformAccount.update(can_use=can_use, session=session).where(
            TblPlatformAccount.username == username
        ).execute()
        return (
            jsonify({"code": 0, "msg": "成功"}),
            200,
            {"Content-Type": "application/json; charset=utf-8"},
        )
    except:
        return (
            jsonify({"code": 1, "msg": "失败"}),
            400,
            {"Content-Type": "application/json; charset=utf-8"},
        )


@app.route("/update_session", methods=["POST"])
@validate_token
def update_session():
    session = request.form.get("session")
    username = request.form.get("username")
    try:
        TblPlatformAccount.update(session=session).where(
            TblPlatformAccount.username == username
        ).execute()
        return (
            jsonify({"code": 0, "msg": "成功"}),
            200,
            {"Content-Type": "application/json; charset=utf-8"},
        )
    except:
        return (
            jsonify({"code": 1, "msg": "失败"}),
            400,
            {"Content-Type": "application/json; charset=utf-8"},
        )


@app.route("/modify_can_use", methods=["POST"])
@validate_token
def modify_can_use():
    can_use = request.form.get("can_use")
    username = request.form.get("username")
    try:
        TblPlatformAccount.update(can_use=can_use).where(
            TblPlatformAccount.username == username
        ).execute()
        return (
            jsonify({"code": 0, "msg": "成功"}),
            200,
            {"Content-Type": "application/json; charset=utf-8"},
        )
    except:
        return (
            jsonify({"code": 1, "msg": "失败"}),
            400,
            {"Content-Type": "application/json; charset=utf-8"},
        )


@app.route("/get_all_account")
@validate_token
def get_all_account():
    flag = int(request.args.get("flag", 1))
    all_account = []
    if flag == 1:
        items = TblPlatformAccount.select(
            TblPlatformAccount.id,
            TblPlatformAccount.account_type,
            TblPlatformAccount.bind_email,
            TblPlatformAccount.bind_email_password,
            TblPlatformAccount.can_use,
            TblPlatformAccount.comment,
            TblPlatformAccount.password,
            TblPlatformAccount.username,
            TblPlatformAccount.proxy_ip,
            TblPlatformAccount.session,
            TblPlatformAccount.note,
        ).dicts()
        for item in items:
            all_account.append(item)
    else:
        items = TblPlatformAccount.select(
            TblPlatformAccount.id,
            TblPlatformAccount.account_type,
            TblPlatformAccount.bind_email,
            TblPlatformAccount.bind_email_password,
            TblPlatformAccount.can_use,
            TblPlatformAccount.comment,
            TblPlatformAccount.password,
            TblPlatformAccount.username,
            TblPlatformAccount.proxy_ip,
            TblPlatformAccount.note,
        ).dicts()
        for item in items:
            all_account.append(item)

    return jsonify(all_account)


@app.route("/modify_account_info", methods=["POST"])
@validate_token
def modify_account_info():
    data_list = request.json.get("data")
    fail_num = 0
    success_num = 0
    for item in data_list:
        try:
            account_id = item.pop("id")
            TblPlatformAccount.update(**item).where(
                TblPlatformAccount.id == account_id
            ).execute()
            success_num += 1
        except:
            fail_num += 1

    msg = "修改成功个数: %s, 修改失败个数： %s" % (success_num, fail_num)

    return jsonify({"code": 0, "msg": msg})


@app.route("/get_account_by_type")
@validate_token
def get_account_by_type():
    utype = request.args.get("type", "1")
    flag = request.args.get("flag", "2")
    utype = utype.split(",")
    type_list = []
    for item in utype:
        type_list.append(int(item))
    account_list = []
    if flag == "1":
        items = (
            TblPlatformAccount.select(
                TblPlatformAccount.id,
                TblPlatformAccount.account_type,
                TblPlatformAccount.bind_email,
                TblPlatformAccount.bind_email_password,
                TblPlatformAccount.can_use,
                TblPlatformAccount.comment,
                TblPlatformAccount.password,
                TblPlatformAccount.username,
                TblPlatformAccount.proxy_ip,
                TblPlatformAccount.session,
                TblPlatformAccount.note,
            )
            .where(TblPlatformAccount.can_use.in_(type_list))
            .dicts()
        )
    else:
        items = (
            TblPlatformAccount.select(
                TblPlatformAccount.id,
                TblPlatformAccount.account_type,
                TblPlatformAccount.bind_email,
                TblPlatformAccount.bind_email_password,
                TblPlatformAccount.can_use,
                TblPlatformAccount.comment,
                TblPlatformAccount.password,
                TblPlatformAccount.username,
                TblPlatformAccount.proxy_ip,
                TblPlatformAccount.note,
            )
            .where(TblPlatformAccount.can_use.in_(type_list))
            .dicts()
        )
    for item in items:
        account_list.append(item)

    return jsonify(account_list)


@app.route("/get_tool_account")
@validate_token
def get_tool_account():
    username = "admin"
    password = "Aa123456"
    return {
        "code": 0,
        "msg": "success",
        "data": {"username": username, "password": password},
    }


@app.get("/get_scrapy_sites")
@validate_token
def get_scrapy_sites():
    data = []
    for value in TblScrapySite.select().dicts().iterator():
        value["create_time"] = value["create_time"].strftime("%Y-%m-%d %H:%M:%S")

        data.append(value)
    return {"code": 0, "msg": "success", "data": data}


@app.post("/add_scrapy_sites")
@validate_token
def add_scrapy_site():
    site_url = request.json.get("site_url")
    site_account = request.json.get("site_account")
    site_passwd = request.json.get("site_passwd")
    note = request.json.get("note") or ""
    project = request.json.get("project")
    count = TblScrapySite.select().where(TblScrapySite.site_url == site_url).count()
    if count != 0:
        return {"code": 1, "msg": "账号已存在"}
    else:
        TblScrapySite.create(
            site_url=site_url,
            site_account=site_account,
            site_passwd=site_passwd,
            note=note,
            project=project,
        )
        return {"code": 0, "msg": "站点已添加"}


@app.post("/modify_scrapy_sites")
@validate_token
def modify_scrapy_site():
    site_id = request.json.get("site_id")
    data = request.json.get("data") or {}
    TblScrapySite.update(**data).where(TblScrapySite.id == site_id).execute()
    return {"code": 0, "msg": "站点数据已修改"}


@app.post("/modify_scrapy_sites_by_url")
@validate_token
def modify_scrapy_sites_by_address():
    site_url = request.json.get("url")
    data = request.json.get("data") or {}
    TblScrapySite.update(**data).where(TblScrapySite.site_url == site_url).execute()
    return {"code": 0, "msg": "站点数据已修改"}


@app.post("/delete_scrapy_site")
@validate_token
def delete_scrapy_site():
    site_id = request.json.get("site_id")
    TblScrapySite.delete().where(TblScrapySite.id == site_id).execute()
    return {"code": 0, "msg": "站点数据已删除"}


@app.post("/check_server_id")
@validate_token
def check_server_id():
    server_ip = request.form.get("server_ip")
    try:
        server_id = TblScrapySite.get_or_none(
            TblScrapySite.site_url.contains(server_ip)
        ).id
        return {"code": 0, "msg": "success", "data": server_id}
    except:
        return {"code": -1, "msg": "未查到"}


@app.get("/get_scrapy_visits")
@validate_token
def get_scrapy_visits():
    # 获取当前日期
    current_date = datetime.date.today()

    crawler_name = request.args.get("crawler_name", "1")
    check_time = request.args.get("check_time", current_date)
    start_time = request.args.get("start_time", None)
    end_time = request.args.get("end_time", None)
    if isinstance(check_time, datetime.date):
        pass
    else:
        check_time = datetime.datetime.strptime(check_time, "%Y-%m-%d")
    data_list = []
    if (start_time or end_time) is None:
        if crawler_name == "1":
            items = (
                TblScrapyVisits.select()
                .where(TblScrapyVisits.create_time == check_time)
                .dicts()
                .iterator()
            )
        else:
            crawler_name = crawler_name.split(",")
            name_list = []
            for item in crawler_name:
                name_list.append(item)
            items = (
                TblScrapyVisits.select()
                .where(
                    TblScrapyVisits.create_time == check_time,
                    TblScrapyVisits.crawler_name.in_(name_list),
                )
                .dicts()
                .iterator()
            )
    else:
        if crawler_name == "1":
            items = (
                TblScrapyVisits.select()
                .where(
                    TblScrapyVisits.create_time >= start_time,
                    TblScrapyVisits.create_time <= end_time,
                )
                .dicts()
                .iterator()
            )
        else:
            crawler_name = crawler_name.split(",")
            name_list = []
            for item in crawler_name:
                name_list.append(item)
            items = (
                TblScrapyVisits.select()
                .where(
                    TblScrapyVisits.create_time >= start_time,
                    TblScrapyVisits.create_time <= end_time,
                    TblScrapyVisits.crawler_name.in_(name_list),
                )
                .dicts()
                .iterator()
            )
    for item in items:
        server_id = item["which_server"]
        server = TblScrapySite.get_or_none(TblScrapySite.id == server_id)
        if server is not None:
            server_name = server.note
        else:
            server_name = None
        item["server_name"] = server_name
        data_list.append(item)

    return jsonify(data_list)


@app.post("/add_scrapy_visits")
@validate_token
def add_scrapy_visits():
    # 获取当前日期
    current_date = datetime.date.today()
    modify_time = datetime.datetime.now()
    if "X-Forwarded-For" in request.headers:
        # 获取 IP 地址列表（可能经过多个代理）
        ip_list = request.headers.getlist("X-Forwarded-For")
        # 取最后一个 IP 地址即为真实的客户端 IP
        server_ip = ip_list[-1]
    else:
        # 如果没有 X-Forwarded-For 头部，则使用 remote_addr
        server_ip = request.remote_addr

    if server_ip == "127.0.0.1":
        server_ip = "54.209.179.134"
    # server_ip = '54.209.179.134'
    try:
        which_server = TblScrapySite.get_or_none(
            TblScrapySite.site_url.contains(server_ip)
        ).id
    except:
        which_server = 0

    crawler_name = request.form.get("crawler_name", None)
    visits_num = request.form.get("visits_num", 1)
    if crawler_name is None:
        return {"code": 0, "msg": "没有指定爬虫项目"}
    query = TblScrapyVisits.get_or_none(
        TblScrapyVisits.crawler_name == crawler_name,
        TblScrapyVisits.create_time == current_date,
        TblScrapyVisits.which_server == which_server,
    )

    if query is not None:
        add_num = query.crawler_visits + int(visits_num)
        data = {"crawler_name": query.crawler_name, "add_num": add_num}
        TblScrapyVisits.update(crawler_visits=add_num, modify_time=modify_time).where(
            TblScrapyVisits.crawler_name == crawler_name,
            TblScrapyVisits.create_time == current_date,
            TblScrapyVisits.which_server == which_server,
        ).execute()
    else:
        data = {
            "crawler_name": crawler_name,
            "which_server": which_server,
            "crawler_visits": int(visits_num),
            "create_time": current_date,
        }
        TblScrapyVisits.insert(data).execute()

    return {"code": 0, "msg": "success", "data": data}


@app.post("/modify_scrapy_visits_info")
@validate_token
def modify_scrapy_visits_info():
    data_list = request.json.get("data")
    fail_num = 0
    success_num = 0
    for item in data_list:
        try:
            data_id = item.pop("id")
            TblScrapyVisits.update(**item).where(
                TblScrapyVisits.id == data_id
            ).execute()
            success_num += 1
        except:
            fail_num += 1

    msg = "修改成功个数: %s, 修改失败个数： %s" % (success_num, fail_num)

    return jsonify({"code": 0, "msg": msg})


init_schduler()

if __name__ == "__main__":
    app.run(debug=True)
