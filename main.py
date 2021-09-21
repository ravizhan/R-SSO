import hmac
import json
import random
import string
import time
import yaml

import pymysql
import redis
from fastapi import FastAPI, Response, Form
from fastapi.middleware.cors import CORSMiddleware

with open("config_test.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET,POST"],
    allow_headers=["*"],
)
db = pymysql.connect(host=config["mysql"]["host"], port=config["mysql"]["port"], user=config["mysql"]["user"],
                     passwd=config["mysql"]["passwd"], database=config["mysql"]["database"],
                     autocommit=True)
cursor = db.cursor()
pool = redis.ConnectionPool(host=config["redis"]["host"], port=config["redis"]["port"], decode_responses=True,
                            db=config["redis"]["db"], password=config["redis"]["password"])
r = redis.Redis(connection_pool=pool)


def user_exist(user):
    sql = "SELECT * FROM user WHERE name='" + user + "'"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        if len(results) == 0:
            return False
        else:
            return True
    except Exception as e:
        print(e)


@app.post("/api/login")
def login(user: str = Form(None), password: str = Form(None)):
    sql = "SELECT password FROM user WHERE name='" + user + "'"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            return {"status": "403", "message": "登陆失败"}
        if results[0][0] == password:
            text = str(round(time.time())) + user + ''.join(random.sample(string.ascii_letters + string.digits, 8))
            code = hmac.new(text.encode(), digestmod="sha256").hexdigest()
            r.set(code, user, ex=30)
            return {"status": "200", "message": "登陆成功", "code": code}
        else:
            return {"status": "403", "message": "登陆失败"}
    except Exception as e:
        print(e)
        return Response(status_code=500, media_type="application/json",
                        content=json.dumps({"status": "500", "message": "未知错误，请联系网站管理员"}, ensure_ascii=False))


@app.post("/api/register")
def register(user: str = Form(None), password: str = Form(None), email: str = Form(None)):
    sql = "INSERT INTO user VALUES(NULL,'%s','%s','%s')" % (user, password, email)
    if not user_exist(user):
        try:
            cursor.execute(sql)
            return {"status": "200", "message": "注册成功"}
        except Exception as e:
            print(e)
            return Response(status_code=500, media_type="application/json",
                            content=json.dumps({"status": "500", "message": "未知错误，请联系网站管理员"}, ensure_ascii=False))
    else:
        return Response(status_code=403, media_type="application/json",
                        content=json.dumps({"status": "403", "message": "用户名已存在"}, ensure_ascii=False))


@app.get("/api/profile")
def auth(code: str):
    user = r.get(code)
    if user is not None:
        sql = "SELECT * FROM user WHERE name='" + user + "'"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()[0]
            data = {
                "id": results[0],
                "user": results[1],
                "email": results[3]
            }
            r.delete(code)
            return data
        except Exception as e:
            print(e)
            return Response(status_code=500, media_type="application/json",
                            content=json.dumps({"status": "500", "message": "未知错误，请联系网站管理员"}, ensure_ascii=False))
    else:
        return Response(status_code=403, media_type="application/json",
                        content=json.dumps({"status": "403", "message": "code不存在"}, ensure_ascii=False))


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", reload=True)
