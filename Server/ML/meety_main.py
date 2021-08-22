# Импорт модулей
import random, requests, json, time, datetime, io, re, hashlib

from flask import request, jsonify, send_file
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request

import meety_utils as utils
import meety_orm as orm
from meety_gen import gen_min
from meety_config import app, cors, db, jwt

# Добавляем заголовки для CORS
@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Origin, Content-Type, X-Auth-Token, Authorization"
    return response

# Авторизация
@app.route("/auth",  methods=['POST'])
def auth():
    # username = request.json.get("username", None)
    # password = request.json.get("password", None)
    # Дергаем базу
    # user_login = orm.User.query.filter(orm.User.email == username, orm.User.password_hash == password).first_or_404()
    # Генерим токен
    # access_token = create_access_token(identity=user_login.user_id)
    # Авторизацию отключили для MVP
    access_token = create_access_token(identity=1)
    return jsonify(access_token = access_token), 200

# Создание встречи (тут должна быть интеграция с почтовым сервисом)
@app.route("/create_meeting",  methods=['POST', 'GET'])
def create_meeting():
    meeting_body = request.json
    # Готовим запись для помещения в БД
    new_meeting = orm.Meeting(external_id         = hashlib.md5(meeting_body['id'].encode()).hexdigest(),
                              meeting_subject     = meeting_body['meeting_subject'],
                              meeting_datetime_ts = meeting_body['meeting_datetime_ts'],
                              meeting_duration    = meeting_body['meeting_duration'],
                              meeting_place       = meeting_body['meeting_place'],
                              # owner_id            = utils.get_user_by_email(meeting_body['owner']),
                              owner_id            = 1,
                              visible             = 1)
    db.session.add(new_meeting)
    # Крепим к встрече участников
    [new_meeting.participant.append(orm.Meeting_Participant(
        description = x['description'],
        user_id = utils.get_user_by_email(x['description']),
        status = 0,
        email = re.search(r'[\w\.-]+@[\w\.-]+', x['description']).group())) for x in meeting_body['meeting_participants']]
    # Комитим
    db.session.commit()
    return jsonify(result=new_meeting.serialize)

# Получить JSON со списком встреч
@app.route("/get_meetings",  methods=['GET'])
# @jwt_required()
def get_meetings():
    # meetings = [x.serialize for x in orm.Meeting.query.filter(orm.Meeting.owner_id == get_jwt_identity(),
    meetings = [x.serialize for x in orm.Meeting.query.filter(orm.Meeting.owner_id == 1,
                                                              orm.Meeting.visible > 0).all()]
    return jsonify(result=meetings)

# Получить транскрипцию звуковых дорожек (текст встречи/стенограмму)
@app.route("/get_transcript",  methods=['GET'])
# @jwt_required()
def get_transcript():
    # Проверка на права
    # meeting = orm.Meeting.query.filter(orm.Meeting.owner_id == get_jwt_identity(),
    meeting = orm.Meeting.query.filter(orm.Meeting.owner_id == 1,
                                       orm.Meeting.visible > 0,
                                       orm.Meeting.meeting_id == request.json.get("meeting_id", None)).first()
    if meeting is None:
        return jsonify(status='error', error_text='no such meeting or access denied')
    # Отдаем текст встречи в списке в JSON
    trans = [x.serialize 
             for x 
             in orm.Record.query.filter(orm.Record.meeting_id == meeting.meeting_id).all()]
    if trans is None:
        return jsonify(status='error', error_text='no such meeting or access denied')
    else:
        return jsonify(result=trans)

# Получить минутки встречи
@app.route("/get_minutes_file",  methods=['GET'])
# @jwt_required()
def get_minutes_file():
    # Проверка на права
    # meeting = orm.Meeting.query.filter(orm.Meeting.owner_id == get_jwt_identity(),
    meeting = orm.Meeting.query.filter(orm.Meeting.owner_id == 1,
                                       orm.Meeting.visible > 0,
                                       orm.Meeting.meeting_id == request.json.get("meeting_id", None)).first()
    if meeting is None:
        return jsonify(status='error', error_text='no such meeting or access denied')
    # Отдаем текст встречи файлом
    file_str = ''
    file_str += 'Протокол встречи\n\n'
    file_str += '\n'.join(filter(None, meeting.serialize_minutes))
    return send_file(io.BytesIO(file_str.encode()),
                     as_attachment=True,
                     attachment_filename=str(request.json.get('filename') + '.txt'),
                     mimetype='text/csv')
                     
# Получить минутки встречи
@app.route("/get_minutes",  methods=['GET'])
# @jwt_required()
def get_minutes():
    # Проверка на права
    # meeting = orm.Meeting.query.filter(orm.Meeting.owner_id == get_jwt_identity(),
    meeting = orm.Meeting.query.filter(orm.Meeting.owner_id == 1,
                                       orm.Meeting.visible > 0,
                                       orm.Meeting.meeting_id == request.json.get("meeting_id", None)).first()
    if meeting is None:
        return jsonify(status='error', error_text='no such meeting or access denied')
    # Отдаем минутки в JSON
    minute = [x.serialize 
              for x 
              in orm.Minute.query.filter(orm.Minute.meeting_id == meeting.meeting_id).all()]
    if minute is None:
        return jsonify(status='error', error_text='no such meeting or access denied')
    else:
        return jsonify(result=minute)

# Распознание дорожек (распознаны на клиенте, но можно это сделать и на стороне сервера)
@app.route("/recognize", methods=['POST'])
# @jwt_required()
def recognize():
    if request.method == "POST":
        external_id = request.json.get("meeting_id", None)
        # meeting = orm.Meeting.query.filter(orm.Meeting.owner_id == get_jwt_identity(),
        meeting = orm.Meeting.query.filter(orm.Meeting.owner_id == 1,
                                           orm.Meeting.visible > 0,
                                           orm.Meeting.meeting_id == external_id).first()
        max_number = orm.Record.query.filter(orm.Record.meeting_id == meeting.meeting_id).order_by(orm.Record.sort_num.desc()).first()
        new_record = orm.Record(
            meeting_id = meeting.meeting_id,
            input_text = request.json.get("text", ''), # изменить тут способ распознавания и вставить запрос сюда
            sort_num   = max_number.sort_num + 1)
        db.session.add(new_record)
        db.session.commit()
        return  jsonify(result=new_record.serialize)
        
# Сгенерировать минутки
@app.route("/gen_minutes", methods=['POST'])
# @jwt_required()
def gen_minutes():
    # Проверка на права
    if request.method == "POST":
        external_id = request.json.get("meeting_id", None)
        # meeting = orm.Meeting.query.filter(orm.Meeting.owner_id == get_jwt_identity(),
        meeting = orm.Meeting.query.filter(orm.Meeting.owner_id == 1,
                                           orm.Meeting.visible > 0,
                                           orm.Meeting.meeting_id == external_id).first()        
        records = orm.Record.query.filter(orm.Record.meeting_id == meeting.meeting_id).order_by(orm.Record.sort_num).all()
        # Генерируем минутки
        minutes = gen_min(' '.join(filter(None, meeting.serialize_text)))
        [db.session.add(orm.Minute(text = x['text'],
                                   sort_num = x['sort_num'],
                                   meeting_id = meeting.meeting_id)) for x in minutes]
        return  jsonify(result=minutes)
    
# Запускаем сервис в случае старта как отдельного скрипта на 5000 порту с шифрованием (https)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
