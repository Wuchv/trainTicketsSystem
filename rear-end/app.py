import os

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import Flask, make_response, request, redirect, url_for, abort, session, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import config
import datetime
import json

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
app.config.from_object(config)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
CORS(app, supports_credentials=True)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    tel = db.Column(db.Integer, nullable=False)
    rel_name = db.Column(db.String(30))
    sex = db.Column(db.String(10))
    type_of_certificate = db.Column(db.String(50))
    id_number = db.Column(db.String(50))
    permission = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30))


class Train(db.Model):
    __tablename__ = 'train'
    train_id = db.Column(db.String(30), primary_key=True)
    type = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30), nullable=False)


class Timetable(db.Model):
    __tablename__ = 'timetable'
    train_id = db.Column(db.String(30), db.ForeignKey('train'), primary_key=True)
    city = db.Column(db.String(30), nullable=False)
    station = db.Column(db.String(30), nullable=False)
    station_index = db.Column(db.Integer, nullable=False)
    arrive_time = db.Column(db.DateTime, nullable=False, primary_key=True)
    leave_time = db.Column(db.DateTime, nullable=False)

    train = db.relationship('Train', backref=db.backref('timetable'))


class Seat(db.Model):
    __tablename__ = 'seat'
    seat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.String(30), db.ForeignKey('train'), nullable=False)
    seat_type = db.Column(db.String(20), nullable=False)
    car = db.Column(db.String(15), nullable=False)
    seat_no = db.Column(db.String(20), nullable=False)

    train = db.relationship('Train', backref=db.backref('seat'))


class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user'), nullable=False)
    train_id = db.Column(db.String(30), db.ForeignKey('train'), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    start_station = db.Column(db.String(30), nullable=False)
    start_station_index = db.Column(db.Integer, nullable=False)
    end_station = db.Column(db.String(30), nullable=False)
    end_station_index = db.Column(db.Integer, nullable=False)
    money = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('order'))
    train = db.relationship('Train', backref=db.backref('order'))
    seat = db.relationship('Seat', backref=db.backref('order'))


class Price(db.Model):
    __tablename__ = 'price'
    city_1 = db.Column(db.String(30), primary_key=True, nullable=False)
    city_2 = db.Column(db.String(30), primary_key=True, nullable=False)
    seat_type = db.Column(db.String(20), primary_key=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)


db.create_all()


# # 增
# use1 = User(username='aaa', password='111', permission=0)
# db.session.add(use1)
# db.session.commit()

# # 查（res是列表）
# res = User.query.filter(User.id == 1).all()
# print(res[0].username)

# # 改
# user1 = User.query.filter(User.id == 1).first()
# user1.username = 'new aaa'
# db.session.commit()

# # 删
# user1 = User.query.filter(User.id == 1).first()
# db.session.delete(user1)
# db.session.commit()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        username = json_data.get("username")
        password = json_data.get("password")
        res = User.query.filter(User.username == username, User.password == password).first()
        if res:
            result = {
                "code": 0,
                "msg": "登陆成功",
                "data": {
                    "user_id": res.user_id,
                    "permission": res.permission
                }
            }
        else:
            result = {
                "code": 1,
                "msg": "登陆失败",
                "data": {}
            }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        username = json_data.get("username")
        password = json_data.get("password")
        tel = json_data.get("tel")
        radio = json_data.get("radio")
        res = User.query.filter(User.tel == tel or User.username == username).all()
        if res:
            result = {
                "code": 1,
                "msg": "注册失败",
                "data": {}
            }
        else:
            user = User(username=username, password=password, tel=tel, permission=radio)
            db.session.add(user)
            db.session.commit()
            res = User.query.filter(User.tel == tel).first()
            result = {
                "code": 0,
                "msg": "注册成功",
                "data": {
                    "user_id": res.user_id
                }   
            }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False


@app.route('/forget', methods=['GET', 'POST'])
def forget():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        username = json_data.get("username")
        tel = json_data.get("tel")
        res = User.query.filter(User.username == username, User.tel == tel).first()
        if res:
            result = {
                "code": 0,
                "msg": "找回密码成功",
                "data": {
                    "username": res.username,
                    "password": res.password
                }
            }
        else:
            result = {
                "code": 1,
                "msg": "找回密码失败，用户名或手机号不存在",
                "data": {}
            }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False


@app.route('/admin/getUserInfo', methods=['GET', 'POST'])
def getUserInfo():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        user_id = json_data.get("user_id")
        res = User.query.filter(User.user_id == user_id).first()
        if res:
            result = {
                "code": 0,
                "msg": "成功",
                "data": {
                    "username": res.username,
                    "tel": res.tel,
                    "rel_name": res.rel_name,
                    "sex": res.sex,
                    "type_of_certificate": res.type_of_certificate,
                    "id_number": res.id_number,
                    "password": res.password
                }
            }
        else:
            result = {
                "code": 1,
                "msg": "请检查网络连接",
                "data": {}
            }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False


# user1 = User.query.filter(User.id == 1).first()
# user1.username = 'new aaa'
# db.session.commit()
@app.route('/admin/updateUserInfo', methods=['GET', 'POST'])
def updateUserInfo():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        user_id = json_data.get("user_id")
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            user.username = json_data.get("userInfo")["username"]
            user.rel_name = json_data.get("userInfo")["rel_name"]
            user.tel = json_data.get("userInfo")["tel"]
            user.password = json_data.get("userInfo")["password"]
            user.type_of_certificate = json_data.get("userInfo")["type_of_certificate"]
            user.id_number = json_data.get("userInfo")["id_number"]
            user.sex = json_data.get("userInfo")["sex"]
            db.session.commit()
            result = {
                "code": 0,
                "msg": "修改成功",
                "data": {}
            }
        else:
            result = {
                "code": 1,
                "msg": "请检查网络连接",
                "data": {}
            }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False


# dict转obj
def obj_dic(d):
    top = type('new', (object,), d)
    seqs = tuple, list, set, frozenset
    for i, j in d.items():
        if isinstance(j, dict):
            setattr(top, i, obj_dic(j))
        elif isinstance(j, seqs):
            setattr(top, i,
                    type(j)(obj_dic(sj) if isinstance(sj, dict) else sj for sj in j))
        else:
            setattr(top, i, j)
    return top


# 对查询的座位进行修饰
def decorativeSeats(arg):
    seats = [(), (), ()]
    if len(arg) != 0:
        for item in arg:
            if item.seat_type == "二等座":
                seats[0] = item
            elif item.seat_type == "一等座":
                seats[1] = item
            elif item.seat_type == "商务座":
                seats[2] = item
        for inx, key in enumerate(seats):
            if key:
                print(key)
            else:
                if inx == 0:
                    seats[0] = {"seat_type": "二等座",
                                "amount": 0}
                elif inx == 1:
                    seats[1] = {"seat_type": "一等座",
                                "amount": 0}
                elif inx == 2:
                    seats[2] = {"seat_type": "商务座",
                                "amount": 0}

    else:
        seats = [{"seat_type": "二等座",
                  "amount": 0}, {"seat_type": "一等座",
                                 "amount": 0}, {"seat_type": "商务座",
                                                "amount": 0}]
    return seats


# 查询直达车票
def getDirectTickets(start_city, end_city, date):
    sql_getTrainId = "select  a.train_id, a.station as start_station, a.station_index as start_index, a.leave_time as start_time," \
                     " b.station as end_station, b.station_index as end_index, b.arrive_time as end_time," \
                     " (unix_timestamp(b.arrive_time) - unix_timestamp(a.leave_time)) as running_time" \
                     " from timetable as a,timetable as b,train as c " \
                     " where a.city = '{}' and b.city = '{}' and substring(a.arrive_time,1,10) = '{}' " \
                     " and a.station_index < b.station_index  and a.train_id = b.train_id " \
                     " and c.train_id = a.train_id and c.status = '运行中'".format(start_city, end_city, date)
    train = db.session.execute(sql_getTrainId).fetchall()
    tickets = []
    print(train)
    for item in train:
        sql_getSeat = "select t.train_id, s.seat_type, count(s.seat_type) as amount" \
                      " from train as t, seat as s" \
                      " where t.train_id = '{}' and t.train_id = s.train_id and s.seat_id not in (" \
                      " select seat_id" \
                      " from train_ticket_system.order" \
                      " where train_id = '{}' and substring(start_time,1,10) = '{}' and ((start_station_index >= {}" \
                      " and start_station_index <= '{}') or (end_station_index >= {} and end_station_index <='{}')))" \
                      " group by s.seat_type, t.train_id".format(item.train_id, item.train_id, date,
                                                                 item.start_index, item.end_index, item.start_index,
                                                                 item.end_index)
        seats = decorativeSeats(db.session.execute(sql_getSeat).fetchall())
        tem = {
            "isDirect": True,
            "train_id": item.train_id,
            "start_station": item.start_station,
            "start_index": item.start_index,
            "start_time": item.start_time.strftime('%H:%M'),
            "end_station": item.end_station,
            "end_index": item.end_index,
            "end_time": item.end_time.strftime('%H:%M'),
            "running_time": str('%.2f' % (item.running_time / 3600)) + "h",
            "seat_1": {
                "seat_type": seats[0]["seat_type"],
                "price": getPrice(start_city, end_city, seats[0]["seat_type"]),
                "residual_ticket": seats[0]["amount"]
            }, "seat_2": {
                "seat_type": seats[1]["seat_type"],
                "price": getPrice(start_city, end_city, seats[1]["seat_type"]),
                "residual_ticket": seats[1]["amount"]
            }, "seat_3": {
                "seat_type": seats[2]["seat_type"],
                "price": getPrice(start_city, end_city, seats[2]["seat_type"]),
                "residual_ticket": seats[2]["amount"]
            }
        }
        tickets.append(tem)
    return tickets


def getPrice(city_1, city_2, seat_type):
    sql_getPrice = "select price from price" \
                   " where ((city_1 = '{}' and city_2 = '{}') or (city_1 = '{}' and city_2 = '{}'))" \
                   " and seat_type = '{}'".format(city_1, city_2, city_2, city_1, seat_type)
    price = db.session.execute(sql_getPrice).fetchall()
    return price[0].price


def getTransferTickets(start_city, end_city, date):
    sql_getTrainId = "select a.train_id as fTrain, a.station_index as fStart_index,a.station as fStart_station, a.leave_time as fStart_time, a.city as fCity_1," \
                     "  b.station_index as fEnd_index, b.station as fEnd_station, b.arrive_time as fEnd_time, b.city as fCity_2," \
                     "  c.station_index as sStart_index, c.station as sStart_station, c.leave_time as sStart_time, c.city as sCity_1," \
                     "  d.train_id as sTrain, d.station_index as sEnd_index, d.station as sEnd_station, d.arrive_time as sEnd_time, d.city as sCity_2," \
                     " (unix_timestamp(b.arrive_time) - unix_timestamp(a.leave_time)) as fRunning_time," \
                     " (unix_timestamp(d.arrive_time) - unix_timestamp(c.leave_time)) as sRunning_time," \
                     " (unix_timestamp(d.arrive_time) - unix_timestamp(a.leave_time)) as running_time" \
                     " from timetable as a, timetable as b, timetable as c, timetable as d, train as e, train as f" \
                     " where a.city = '{}' and d.city = '{}' and substring(a.leave_time,1,10) = '{}'" \
                     " and substring(d.arrive_time,1,10) = '{}' and a.train_id = b.train_id and b.station = c.station" \
                     " and c.train_id = d.train_id and b.train_id <> c.train_id and a.station_index < b.station_index" \
                     " and b.arrive_time < c.leave_time and c.station_index < d.station_index and a.train_id = e.train_id" \
                     " and e.status = '运行中' and c.train_id = f.train_id and f.status = '运行中'".format(start_city,
                                                                                                     end_city, date,
                                                                                                     date)
    train = db.session.execute(sql_getTrainId)
    tickets = []
    for item in train:
        sql_getFirstSeat = "select t.train_id, s.seat_type, count(s.seat_type) as amount" \
                           " from train as t, seat as s" \
                           " where t.train_id = '{}' and t.train_id = s.train_id and s.seat_id not in (" \
                           " select seat_id" \
                           " from train_ticket_system.order" \
                           " where train_id = '{}' and substring(start_time,1,10) = '{}' and ((start_station_index >= {}" \
                           " and start_station_index <= '{}') or (end_station_index >= {} and end_station_index <='{}')))" \
                           " group by s.seat_type, t.train_id".format(item.fTrain, item.fTrain, date,
                                                                      item.fStart_index, item.fEnd_index,
                                                                      item.fStart_index, item.fEnd_index)
        sql_getSecondSeat = "select t.train_id, s.seat_type, count(s.seat_type) as amount" \
                            " from train as t, seat as s" \
                            " where t.train_id = '{}' and t.train_id = s.train_id and s.seat_id not in (" \
                            " select seat_id" \
                            " from train_ticket_system.order" \
                            " where train_id = '{}' and substring(start_time,1,10) = '{}' and ((start_station_index >= {}" \
                            " and start_station_index <= '{}') or (end_station_index >= {} and end_station_index <='{}')))" \
                            " group by s.seat_type, t.train_id".format(item.sTrain, item.sTrain, date,
                                                                       item.sStart_index, item.sEnd_index,
                                                                       item.sStart_index, item.sEnd_index)
        fSeats = decorativeSeats(db.session.execute(sql_getFirstSeat).fetchall())
        sSeats = decorativeSeats(db.session.execute(sql_getSecondSeat).fetchall())
        tem = {
            "isDirect": False,
            "train_id": item.fTrain + "/" + item.sTrain,
            "start_station": item.fStart_station,
            "start_time": item.fStart_time.strftime('%H:%M'),
            "end_station": item.sEnd_station,
            "end_time": item.sEnd_time.strftime('%H:%M'),
            "running_time": str('%.2f' % (item.running_time / 3600)) + "h",
            "children": [{
                "isDirect": False,
                "index": 0,
                "train_id": item.fTrain,
                "start_station": item.fStart_station,
                "start_index": item.fStart_index,
                "start_time": item.fStart_time.strftime('%H:%M'),
                "end_station": item.fEnd_station,
                "end_index": item.fEnd_index,
                "end_time": item.fEnd_time.strftime('%H:%M'),
                "running_time": str('%.2f' % (item.fRunning_time / 3600)) + "h",
                "seat_1": {
                    "seat_type": fSeats[0]["seat_type"],
                    "price": getPrice(item.fCity_1, item.fCity_2, fSeats[0]["seat_type"]),
                    "residual_ticket": fSeats[0]["amount"]
                }, "seat_2": {
                    "seat_type": fSeats[1]["seat_type"],
                    "price": getPrice(item.fCity_1, item.fCity_2, fSeats[1]["seat_type"]),
                    "residual_ticket": fSeats[1]["amount"]
                }, "seat_3": {
                    "seat_type": fSeats[2]["seat_type"],
                    "price": getPrice(item.fCity_1, item.fCity_2, fSeats[2]["seat_type"]),
                    "residual_ticket": fSeats[2]["amount"]
                }
            }, {
                "isDirect": False,
                "index": 1,
                "train_id": item.sTrain,
                "start_station": item.sStart_station,
                "start_index": item.sStart_index,
                "start_time": item.sStart_time.strftime('%H:%M'),
                "end_station": item.sEnd_station,
                "end_index": item.fEnd_index,
                "end_time": item.sEnd_time.strftime('%H:%M'),
                "running_time": str('%.2f' % (item.sRunning_time / 3600)) + "h",
                "seat_1": {
                    "seat_type": sSeats[0]["seat_type"],
                    "price": getPrice(item.sCity_1, item.sCity_2, sSeats[0]["seat_type"]),
                    "residual_ticket": sSeats[0]["amount"]
                },
                "seat_2": {
                    "seat_type": sSeats[1]["seat_type"],
                    "price": getPrice(item.sCity_1, item.sCity_2, sSeats[1]["seat_type"]),
                    "residual_ticket": sSeats[1]["amount"]
                }, "seat_3": {
                    "seat_type": sSeats[2]["seat_type"],
                    "price": getPrice(item.sCity_1, item.sCity_2, sSeats[2]["seat_type"]),
                    "residual_ticket": sSeats[2]["amount"]
                }
            }]
        }
        tickets.append(tem)
    return tickets


@app.route('/admin/getTickets', methods=['GET', 'POST'])
def getTickets():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        start_city = json_data.get("start_city")
        end_city = json_data.get("end_city")
        date = json_data.get("date")
        print(start_city, end_city, date)
        getPrice(start_city, end_city, "二等座")
        directTickets = getDirectTickets(start_city, end_city, date)
        transferTickets = getTransferTickets(start_city, end_city, date)
        result = {
            "code": 0,
            "msg": "获取成功",
            "data": directTickets + transferTickets
        }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False


# 获取座位id
def getSeatId(train_id, seat_type):
    sql_getSeatId = "select seat_id from seat where train_id = '{}' and seat_type = '{}'".format(train_id, seat_type)
    seats = db.session.execute(sql_getSeatId).fetchall()
    return seats[0].seat_id


@app.route('/admin/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        data = json_data.get("order")
        if data["isDirect"]:
            print("isDirect")
            item = Order(user_id=data["user_id"], train_id=data["detail"]["train_id"],
                         seat_id=getSeatId(data["detail"]["train_id"], data["seat"]["seat_type"]),
                         start_time=data["date"] + " " + data["detail"]["start_time"],
                         end_time=data["date"] + " " + data["detail"]["end_time"],
                         start_station=data["detail"]["start_station"],
                         start_station_index=data["detail"]["start_index"],
                         end_station=data["detail"]["end_station"],
                         end_station_index=data["detail"]["end_index"],
                         money=data["seat"]["price"])
            db.session.add(item)
            db.session.commit()
        else:
            fOder = Order(user_id=data["user_id"], train_id=data["fOrder"]["train_id"],
                          seat_id=getSeatId(data["fOrder"]["train_id"], data["fOrder"]["seat"]["seat_type"]),
                          start_time=data["date"] + " " + data["fOrder"]["start_time"],
                          end_time=data["date"] + " " + data["fOrder"]["end_time"],
                          start_station=data["fOrder"]["start_station"],
                          start_station_index=data["fOrder"]["start_index"],
                          end_station=data["fOrder"]["end_station"],
                          end_station_index=data["fOrder"]["end_index"],
                          money=data["fOrder"]["seat"]["price"])
            sOder = Order(user_id=data["user_id"], train_id=data["sOrder"]["train_id"],
                          seat_id=getSeatId(data["sOrder"]["train_id"], data["sOrder"]["seat"]["seat_type"]),
                          start_time=data["date"] + " " + data["sOrder"]["start_time"],
                          end_time=data["date"] + " " + data["sOrder"]["end_time"],
                          start_station=data["sOrder"]["start_station"],
                          start_station_index=data["sOrder"]["start_index"],
                          end_station=data["sOrder"]["end_station"],
                          end_station_index=data["sOrder"]["end_index"],
                          money=data["sOrder"]["seat"]["price"])
            db.session.add(fOder)
            db.session.add(sOder)
            db.session.commit()
        result = {
            "code": 0,
            "msg": "下单成功",
            "data": ""
        }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False


def getUserOrders(user_id):
    sql_getOrders = "select * " \
                    "from train_ticket_system.order " \
                    "where user_id = '{}' " \
                    "order by start_time".format(user_id)
    ordersInSql = db.session.execute(sql_getOrders).fetchall()
    orders = []
    for item in ordersInSql:
        sql_getSeat = "select * from seat where seat_id = '{}'".format(item.seat_id)
        seat = db.session.execute(sql_getSeat).fetchall()[0]
        tem = {
            "order_id": item["order_id"],
            "train_id": item["train_id"],
            "seat_car": seat["car"],
            "seat_no": seat["seat_no"],
            "seat_type": seat["seat_type"],
            "start_time": item["start_time"],
            "start_station": item["start_station"],
            "start_station_index": item["start_station_index"],
            "end_time": item["end_time"],
            "end_station": item["end_station"],
            "end_station_index": item["end_station_index"],
            "running_time": (item["end_time"] - item["start_time"]).seconds,
            "money": item["money"],
            "isFinished": False}
        if tem["start_time"] < datetime.datetime.now():
            tem["isFinished"] = True
        orders.append(tem)
    return orders


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


@app.route('/admin/getOrders', methods=['GET', 'POST'])
def getOrders():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        user_id = json_data.get("user_id")
        orders = getUserOrders(user_id)
        result = {
            "code": 0,
            "msg": "获取成功",
            "data": {"orders": orders}
        }
        response = make_response(json.dumps(result, cls=DateEncoder))
        response.mimetype = 'application/json'
        return response
    return False


@app.route('/admin/returnTicket', methods=['GET', 'POST'])
def returnTicket():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        order_id = json_data.get("order_id")
        tem = Order.query.filter(Order.order_id == order_id).first()
        db.session.delete(tem)
        db.session.commit()
        result = {
            "code": 0,
            "msg": "退票成功",
            "data": ""
        }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False


@app.route('/admin/getUsers', methods=['GET', 'POST'])
def getUsers():
    if request.method == 'GET':
        sql_getUsers = "select * from user where permission <> 1"
        ls = db.session.execute(sql_getUsers).fetchall()
        users = []
        for i in ls:
            tem = {
                "user_id": i.user_id,
                "username": i.username,
                "rel_name": i.rel_name,
                "tel": i.tel,
                "id_number": i.id_number,
                "status": i.status
            }
            users.append(tem)
        result = {
            "code": 0,
            "msg": "退票成功",
            "data": {"users": users}
        }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False


@app.route('/admin/changeUserStatus', methods=['GET', 'POST'])
def changeUserStatus():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        user_id = json_data.get("user_id")
        status = json_data.get("status")
        _status = "禁乘" if status == "正常" else "正常"
        user = User.query.filter(User.user_id == user_id).first()
        user.status = _status
        db.session.commit()
        result = {
            "code": 0,
            "msg": "修改成功",
            "data": ""
        }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False


@app.route('/admin/getTrains', methods=['GET', 'POST'])
def getTrains():
    if request.method == 'GET':
        sql_getTrains = "select * from train"
        ls = db.session.execute(sql_getTrains).fetchall()
        trains = []
        for i in ls:
            tem = {
                "train_id": i.train_id,
                "type": i.type,
                "status": i.status
            }
            trains.append(tem)
        result = {
            "code": 0,
            "msg": "退票成功",
            "data": {"trains": trains}
        }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False


@app.route('/admin/changeTrainStatus', methods=['GET', 'POST'])
def changeTrainStatus():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        train_id = json_data.get("train_id")
        status = json_data.get("status")
        _status = "停运" if status == "运行中" else "运行中"
        train = Train.query.filter(Train.train_id == train_id).first()
        train.status = _status
        db.session.commit()
        result = {
            "code": 0,
            "msg": "修改成功",
            "data": ""
        }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False


@app.route('/admin/deleteUser', methods=['GET', 'POST'])
def deleteUser():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        user_id = json_data.get("user_id")
        user = User.query.filter(User.user_id == user_id).first()
        db.session.delete(user)
        db.session.commit()
        result = {
            "code": 0,
            "msg": "删除成功",
            "data": ""
        }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False


@app.route('/admin/deleteTrain', methods=['GET', 'POST'])
def deleteTrain():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        train_id = json_data.get("train_id")
        train = Train.query.filter(Train.train_id == train_id).first()
        db.session.delete(train)
        db.session.commit()
        result = {
            "code": 0,
            "msg": "删除成功",
            "data": ""
        }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False


@app.route('/admin/getTimetable', methods=['GET', 'POST'])
def getTimetable():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        date = json_data.get("date")
        sql_getTimetable = "select * from timetable where substring(arrive_time,1,10) = '{}'".format(date)
        ls = db.session.execute(sql_getTimetable).fetchall()
        timetable = []
        for i in ls:
            tem = {
                "train_id": i.train_id,
                "city": i.city,
                "station": i.station,
                "arrive_time": i.arrive_time,
                "leave_time": i.leave_time
            }
            timetable.append(tem)
        result = {
            "code": 0,
            "msg": "查询成功",
            "data": {"timetable": timetable}
        }
        response = make_response(json.dumps(result, cls=DateEncoder))
        response.mimetype = 'application/json'
        return response
    return False


@app.route('/admin/deleteTimetable', methods=['GET', 'POST'])
def deleteTimetable():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        train_id = json_data.get("train_id")
        city = json_data.get("city")
        station = json_data.get("station")
        arrive_time = json_data.get("arrive_time")
        record = Timetable.query.filter(Timetable.train_id == train_id, Timetable.city == city,
                                        Timetable.station == station, Timetable.arrive_time == arrive_time).first()
        db.session.delete(record)
        db.session.commit()
        result = {
            "code": 0,
            "msg": "删除成功",
            "data": ""
        }
        response = make_response(json.dumps(result))
        response.mimetype = 'application/json'
        return response
    return False



