# -*- coding: utf-8 -*-
from flask import Flask, request
import os
import sqlite3
from threading import Thread
from uuid import uuid4
import requests
import time
from pyquery import PyQuery
import re
import json

app = Flask(__name__)


# 服务
def dg():
    print('打工线程启动')
    while True:
        sql = sqlite3.connect('database.db')
        info = sql.execute("SELECT name,cookie,id FROM user").fetchall()
        sql.close()
        for i in info:
            url = 'https://www.tsdm39.com/plugin.php?id=np_cliworkdz:work'
            headers = {
                'Cookie': i[1],
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9.0; SAMSUNG SM-F900U Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36 Edg/111.0.1661.62'
            }

            for _ in [1, 2, 3, 4, 5, 6, 7]:
                while True:
                    try:
                        requests.post(url=url, headers=headers, data={'act': 'clickad'})
                        break
                    except:
                        print(i[0], ' 出现异常,正在重试')
                        sql = sqlite3.connect('database.db')
                        sql.execute("INSERT INTO task (type, time, info) VALUES (?, ?, ?)",
                                    ('dg', str(time.time_ns()), i[0] + ' 出现异常,正在重试',))
                        sql.commit()
                        sql.close()
                        time.sleep(60)
                time.sleep(2)

            while True:
                try:
                    ttt = requests.post(url=url, headers=headers, data={'act': 'getcre'}).text
                    break
                except:
                    sql = sqlite3.connect('database.db')
                    sql.execute("INSERT INTO task (type, time, info) VALUES (?, ?, ?)",
                                ('dg', str(time.time_ns()), i[0] + ' 出现异常,正在重试',))
                    sql.commit()
                    sql.close()
                    print(i[0], ' 出现异常,正在重试')
                    time.sleep(60)

            if '不要作弊哦，重新进行游戏吧' in ttt:
                print(i[0], ' 出现作弊')
                sql = sqlite3.connect('database.db')
                sql.execute("INSERT INTO task (type, time, info) VALUES (?, ?, ?)", ('dg', str(time.time_ns()), i[0] + '出现作弊',))
                sql.commit()
                sql.close()
                info.append(i)
                time.sleep(60)
                continue
            if '必须与上一次间隔6小时0分钟0秒才可再次进行' in ttt:
                print(i[0], ' 时间未到')
                sql = sqlite3.connect('database.db')
                sql.execute("INSERT INTO task (type, time, info) VALUES (?, ?, ?)", ('dg', str(time.time_ns()), i[0] + '时间未到',))
                sql.commit()
                sql.close()
                continue

            print(i[0], ' 打工完成')
            sql = sqlite3.connect('database.db')
            sql.execute("INSERT INTO task (type, time, info) VALUES (?, ?, ?)",
                        ('dg', str(time.time_ns()), i[0] + ' 打工完成',))
            sql.commit()
            sql.close()
            time.sleep(5)

        sql = sqlite3.connect('database.db')
        sql.execute("INSERT INTO status (type, time, info) VALUES (?, ?, ?)", ('dg', str(time.time_ns()), '打工完成',))
        sql.commit()
        sql.close()
        Thread(target=cx, daemon=True).start()
        time.sleep(21600)


def qd():
    print('签到线程启动')
    while True:
        if time.strftime('%H', time.localtime()) != '18':
            time.sleep(300)
            continue
        # 获取用户信息
        sql = sqlite3.connect('database.db')
        info = sql.execute("SELECT name,cookie,id FROM user").fetchall()
        sql.close()
        for i in info:
            # 获取formhash值
            url = 'https://www.tsdm39.com/forum.php?mobile=yes'
            headers = {
                'Cookie': i[1],
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9.0; SAMSUNG SM-F900U Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36 Edg/111.0.1661.62'
            }
            text = ''
            while True:
                try:
                    text = requests.get(url=url, headers=headers).text
                    break
                except:
                    sql = sqlite3.connect('database.db')
                    sql.execute("INSERT INTO task (type, time, info) VALUES (?, ?, ?)",
                                ('qd', str(time.time_ns()), i[0] + ' 出现异常,正在重试',))
                    sql.commit()
                    sql.close()
                    print(i[0], ' 出现异常,正在重试')
                    time.sleep(60)
            text = text.replace('<?xml version="1.0" encoding="utf-8"?>', '')
            doc = PyQuery(text)
            t = doc('body > div.wp > div.pd2 > a:nth-child(11)').attr('href')
            if t == '':
                print(i[0], ' Cookie过期')
                sql = sqlite3.connect('database.db')
                sql.execute("INSERT INTO task (type, time, info) VALUES (?, ?, ?)",
                            ('qd', str(time.time_ns()), i[0] + 'Cookie过期',))
                sql.commit()
                sql.close()
                continue
            formhash = re.search('(?<=(formhash=)).*?(?=(&mobile=yes))', t)[0]

            time.sleep(2)

            # 进行签到
            url = 'https://www.tsdm39.com/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=0&inajax=0&mobile=yes'
            headers = {
                'Cookie': i[1],
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9.0; SAMSUNG SM-F900U Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36 Edg/111.0.1661.62'
            }
            data = {
                'formhash': str(formhash),
                'qdxq': 'kx',
                'qdmode': '3',
                'todaysay': '',
                'fastreply': '1'
            }
            text = ''
            con = 0
            while True:
                try:
                    text = requests.post(url=url, headers=headers, data=data).text
                    if '您今日已经签到' in text:
                        sql = sqlite3.connect('database.db')
                        sql.execute("INSERT INTO task (type, time, info) VALUES (?, ?, ?)",
                                    ('qd', str(time.time_ns()), i[0] + '已经签到',))
                        sql.commit()
                        sql.close()
                        break
                    if '恭喜你签到成功!获得随机奖励' not in text:
                        print(i[0], ' 出现未知问题', con)
                        sql = sqlite3.connect('database.db')
                        sql.execute("INSERT INTO task (type, time, info) VALUES (?, ?, ?)",
                                    ('qd', str(time.time_ns()), i[0] + '出现未知问题，重试：' + str(con),))
                        sql.commit()
                        sql.close()
                        con = con + 1
                        time.sleep(10)
                        if con == 3:
                            sql = sqlite3.connect('database.db')
                            sql.execute("INSERT INTO task (type, time, info) VALUES (?, ?, ?)",
                                        ('qd', str(time.time_ns()), i[0] + '取消重试',))
                            sql.commit()
                            sql.close()
                            con = 0
                            break
                        continue
                    break
                except:
                    sql = sqlite3.connect('database.db')
                    sql.execute("INSERT INTO task (type, time, info) VALUES (?, ?, ?)",
                                ('qd', str(time.time_ns()), i[0] + ' 出现异常,正在重试',))
                    sql.commit()
                    sql.close()
                    print(i[0], ' 出现异常,正在重试')
                    time.sleep(60)

            text = text.replace('<?xml version="1.0" encoding="utf-8"?>', '')
            doc = PyQuery(text)
            sql = sqlite3.connect('database.db')
            sql.execute("INSERT INTO task (type, time, info) VALUES (?, ?, ?)",
                        ('qd', str(time.time_ns()), i[0] + '获得天使币：' + doc('#messagetext > p:nth-child(1)').text().replace('恭喜你签到成功!获得随机奖励 天使币 ', ''),))
            sql.commit()
            sql.close()
            print(i[0] + '获得天使币：' + doc('#messagetext > p:nth-child(1)').text().replace('恭喜你签到成功!获得随机奖励 天使币 ', ''))
            time.sleep(5)
        sql = sqlite3.connect('database.db')
        sql.execute("INSERT INTO status (type, time, info) VALUES (?, ?, ?)",
                    ('qd', str(time.time_ns()), '签到完成',))
        sql.commit()
        sql.close()
        Thread(target=cx, daemon=True).start()
        time.sleep(3600)


def cx():
    print('查询线程启动')
    while True:
        sql = sqlite3.connect('database.db')
        info = sql.execute("SELECT name,cookie,id FROM user").fetchall()
        sql.close()
        for i in info:
            url = 'https://www.tsdm39.com/home.php?mod=space&uid=' + i[2] + '&do=profile&mobile=yes'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9.0; SAMSUNG SM-F900U Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36 Edg/111.0.1661.62'
            }
            text = ''
            while True:
                try:
                    text = requests.get(url=url, headers=headers).text
                    break
                except:
                    print(i[0], ' 出现异常,正在重试')
                    time.sleep(60)
            text = text.replace('<?xml version="1.0" encoding="utf-8"?>', '')
            doc = PyQuery(text)
            sql = sqlite3.connect('database.db')
            sql.execute("UPDATE user SET tsb = ? WHERE id = ?",
                        (str(int(re.search('(?<=(天使币)).*?(?=( ))', doc('body > div.wp > div.bm > div.bm > div > div').text())[0])),i[2],))
            sql.commit()
            sql.close()
            time.sleep(2)
        time.sleep(43200)

# 首次启动检查
if os.path.exists('database.db') is False:
    open('database.db', 'w').close()
    sql = sqlite3.connect('database.db')
    sql.execute("create table user (cookie text not null,id text not null,name text not null,tsb text default '0' not null)")
    sql.execute("create table task (uuid INTEGER constraint task_pk primary key autoincrement,type text not null,time text not null,info text not null)")
    sql.execute("create table status (uuid INTEGER constraint task_pk primary key autoincrement,type text not null,time text not null,info text not null)")
    sql.commit()
    sql.close()
    print('没有数据库，已自动创建')

# 创建服务
Thread(target=dg, daemon=True).start()
Thread(target=qd, daemon=True).start()

pwd = 'L$5V$9eszfv$AX4*&(shajvmtZ&qJQVMT^LNq1lmzwlA%p1CVia3IYO%BV(vCrop'


# 路由
@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/index.css')
def indexCSS():
    return app.send_static_file('index.css')


@app.route('/index.js')
def indexJS():
    return app.send_static_file('index.js')


@app.route('/jquery-3.7.0.js')
def indexJquery():
    return app.send_static_file('jquery-3.7.0.js')


@app.route('/login')
def login():
    return app.send_static_file('login.html')


@app.route('/api/log/dg', methods=['POST'])
def apiLogDG():
    if request.form.get('pwd') != pwd:
        return {'code': '0001', 'info': '密码错误'}

    sql = sqlite3.connect('database.db')
    info = sql.execute("SELECT time,info FROM task WHERE type='dg' ORDER BY uuid DESC LIMIT 0,10").fetchall()
    sql.close()
    return info


@app.route('/api/log/qd', methods=['POST'])
def apiLogQD():
    if request.form.get('pwd') != pwd:
        return {'code': '0001', 'info': '密码错误'}

    sql = sqlite3.connect('database.db')
    info = sql.execute("SELECT time,info FROM task WHERE type='qd' ORDER BY uuid DESC LIMIT 0,10").fetchall()
    sql.close()
    return info


@app.route('/api/user/add', methods=['POST'])
def apiUserAdd():
    if request.form.get('pwd') != pwd:
        return {'code': '0001', 'info': '密码错误'}

    cookie = request.form.get('cookie')
    id = request.form.get('id')
    name = request.form.get('name')

    if cookie == '' or id == '' or name == '':
        return {'code': '0102', 'info': '不能为空'}

    sql = sqlite3.connect('database.db')

    u = sql.execute("SELECT id FROM user WHERE id=?", (id,)).fetchone()
    if u is not None:
        return {'code': '0101', 'info': '账户重复'}

    sql.execute("INSERT INTO user (cookie, id, name) VALUES (?, ?, ?)", (cookie, id, name,))
    sql.commit()
    sql.close()

    return {'code': '0000', 'info': '添加成功'}


@app.route('/api/user/del', methods=['POST'])
def apiUserDel():
    if request.form.get('pwd') != pwd:
        return {'code': '0001', 'info': '密码错误'}

    id = request.form.get('id')
    sql = sqlite3.connect('database.db')
    sql.execute("DELETE FROM user WHERE id = ?", (str(id),))
    sql.commit()
    sql.close()
    return {'code': '0000', 'info': '删除成功'}


@app.route('/api/user/all', methods=['POST'])
def apiUserAll():
    if request.form.get('pwd') != pwd:
        return {'code': '0001', 'info': '密码错误'}

    sql = sqlite3.connect('database.db')
    info = sql.execute("SELECT id,name,cookie FROM user").fetchall()
    if info is None:
        return []
    sql.close()
    return info


@app.route('/api/tsb', methods=['POST'])
def apiTSB():
    if request.form.get('pwd') != pwd:
        return {'code': '0001', 'info': '密码错误'}

    sql = sqlite3.connect('database.db')
    info = sql.execute("SELECT tsb FROM user").fetchall()
    if info is None:
        return '0'
    sql.close()
    all = 0
    for i in info:
        all = all + int(i[0])
    return str(all)


@app.route('/api/status', methods=['POST'])
def apiStatus():
    if request.form.get('pwd') != pwd:
        return {'code': '0001', 'info': '密码错误'}

    sql = sqlite3.connect('database.db')
    try:
        dgv = sql.execute("SELECT time FROM status WHERE type='dg' ORDER BY uuid DESC LIMIT 0,1").fetchone()[0]
    except:
        dgv = '0'
    try:
        qdv = sql.execute("SELECT time FROM status WHERE type='qd' ORDER BY uuid DESC LIMIT 0,1").fetchone()[0]
    except:
        qdv = '0'
    sql.close()
    return {'code': '0000', 'info': '查询成功', 'msg': {'dg': dgv, 'qd': qdv}}


if __name__ == '__main__':
    app.run(port=os.getenv("PORT", default=5000), host='0.0.0.0')
