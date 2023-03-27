import base64
import os

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.exc import IntegrityError
import hashlib
import random
import requests
import json
import uuid
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from database import Session
from Administrator import Administrator
from Verification_code import Verification_code
from User import User
from Notice import Notice

app = Flask(__name__)


# 登录接口
@app.route('/login', methods=['POST'])
def login():
    session = Session()
    token = request.headers.get('Authorization')
    data = request.json
    phone_number = data['phone_number']
    password = data['password']
    verification_code = data['verification_code']

    user = User.query.filter_by(phone_number=phone_number).first()

    if user is None:
        return jsonify({'error': 'User not found'})

    if verification_code:
        if user.verification_code != session.query().filter_by(phone_number=phone_number)[-1]:
            return jsonify({'error': 'Incorrect verification code'})

    else:
        if user.password_hash:
            return jsonify({'error': 'Incorrect password or phone_number'})

    return jsonify({'message': 'Login successful'})


# 注册接口
@app.route('/register', methods=['POST'])
def register():
    session = Session()
    token = request.headers.get('Authorization')
    data = request.json
    username = data['username']
    phone_number = data['phone_number']
    password = data['password']
    confirm_password = data['confirm_password']
    verification_code = data['verification_code']

    if verification_code == session.query(Verification_code).filter_by(phone_number=phone_number).first():
        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'})

        user = User(username, phone_number, password, token)

        # 因为电话号码唯一，所以电话要重复就不能插入到数据库
        try:
            session.add(user)
            session.commit()
        except IntegrityError:
            session.rollback()
            return jsonify({'error': 'User already exists'})

        return jsonify({'message': 'Registration successful'})
    else:
        return jsonify({'error': 'Verification_code do not match'})


# 发送短信认证的接口
@app.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    session = Session()
    data = request.json
    phone_number = data['phone_number']
    verification_code = Verification_code(phone_number=phone_number)
    code = verification_code.generate_verification_code()
    session.add(Verification_code(phone_number=phone_number, code=code))
    session.commit()

    # Replace the following with your own code to send a verification code to the user's phone number
    # using an SMS service like Alibaba Cloud
    # 我没有服务器，不能完成这个功能
    url = 'https://your_sms_service_api_endpoint'
    headers = {'Content-Type': 'application/json'}
    payload = {'phone_number': phone_number, 'verification_code': code}
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    return jsonify({'message': 'Verification code sent'})


# 添加公告接口
@app.route('/notice/<user_id>/add', methods=['post'])
def add_notice(user_id):
    session = Session()
    token = request.headers.get('Authorization')
    administrator = session.query(Administrator).filter_by(id=user_id, token=token).first()
    if administrator:
        title = request.json.get('title')
        content = request.json.get('content')
        notice = Notice(title=title, content=content)
        session.add(notice)
        session.commit()
        return jsonify({'status': 'success', 'message': 'successly add'})
    else:
        return jsonify({'status': 'success', 'message': 'You do not have permission to publish'})


# 获取全部公告接口
@app.route('/notice/<user_id>', methods=['get'])
def get_notice():
    session = Session()
    notices = session.query(Notice).order_by(Notice.create_time).desc()
    if notices:
        return jsonify({'status': 'success', 'notices': notices})
    return jsonify({'status': 'fail', 'message': 'No announcement'})


# 删除公告接口
@app.route('/notice/<user_id>/delete')
def delete_notice(user_id, title_id):
    session = Session()
    token = request.headers.get('Authorization')
    administrator = session.query(Administrator).filter_by(id=user_id, token=token).first()
    if administrator:
        session.delete(Notice.id == title_id)
        session.commit()
        return jsonify({'status': 'success', 'message': 'successly delete'})
    else:
        return jsonify({'status': 'fail', 'message': 'You do not have permission to delete'})


# 用户信息获取接口
@app.route('/user/<user_id>', methods=['GET', 'post'])
def get_user_info(user_id):
    token = request.headers.get('Authorization')
    session = Session()
    # 查询数据库中是否存在相应的用户信息
    user = session.query(User).filter(id=user_id, token=token).first()
    if user:
        return jsonify({'status': 'success',
                        'user_info': {'id': user.id, 'username': user.username, 'phone_number': user.phone_number}})
    return jsonify({'status': 'fail', 'message': '用户认证失败'})


# 注销用户
@app.route('/logoff/<user_id>', methods=['post'])
def logoff(user_id):
    token = request.headers.get('Authorization')
    session = Session()
    user = session.query(User).filter(id=user_id, token=token).first()
    if user:
        session.delete(user)
        session.commit()
        return jsonify({'status': 'success', 'user_id': user_id, 'token': user.token})
    return jsonify({'status': 'fail', 'message': '用户注销失败'})


if __name__ == '__main__':
    app.run(debug=True)
