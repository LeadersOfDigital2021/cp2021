# Импорт модулей
from meety_config import db

# Объекты для работы с базой данных через Алхимию

# Пользователи
class User(db.Model):
    # Поля таблицы в БД
    user_id       = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(32), unique=False, nullable=False)
    active        = db.Column(db.Integer, unique=False, nullable=False)
    # Текстовое представление таблицы для print
    def __repr__(self):
        return '<User %r>' % self.email.split('@')[0]
        
# Встречи
class Meeting(db.Model):
    # Поля таблицы в БД
    meeting_id            = db.Column(db.Integer, primary_key=True)
    external_id           = db.Column(db.String(36), unique=True, nullable=False)
    meeting_subject       = db.Column(db.String(120), unique=False, nullable=False)
    meeting_datetime_ts   = db.Column(db.Integer, unique=False, nullable=False)
    meeting_duration      = db.Column(db.String(120), unique=False, nullable=False)
    meeting_place         = db.Column(db.String(120), unique=False, nullable=False)
    owner_id              = db.Column(db.Integer, db.ForeignKey(User.user_id), unique=False, nullable=False)
    visible               = db.Column(db.Integer, unique=False, nullable=False)
    # Сериализация данных
    @property
    def serialize(self):
        return {
            'meeting_id'             :self.meeting_id,
            'external_id'            :self.source,
            'meeting_subject'        :self.meeting_subject,
            'meeting_participants'   :self.serialize_participants,
            'meeting_datetime_ts'    :self.meeting_datetime_ts,
            'duration'               :self.meeting_window_duration,
            'meeting_place'          :self.meeting_place
       }
    @property
    def serialize_participants(self):
        return [item.serialize for item in self.participant]
    @property
    def serialize_minutes(self):
        return [item.serialize_text for item in self.minute]
    @property
    def serialize_text(self):
        return [item.serialize_text for item in self.record]
    # Текстовое представление таблицы для print
    def __repr__(self):
        return '<Meeting: %r>' % self.meeting_subject
    
# Участники встречи
class Meeting_Participant(db.Model):
    # Поля таблицы в БД
    mpartic_id  = db.Column(db.Integer, primary_key=True)
    meeting_id  = db.Column(db.Integer, db.ForeignKey(Meeting.meeting_id), unique=False, nullable=False)
    meeting     = db.relationship('Meeting', backref=db.backref('participant', lazy=True))
    user_id     = db.Column(db.Integer, db.ForeignKey(User.user_id), unique=False, nullable=True)
    user        = db.relationship('User', backref=db.backref('participant', lazy=True))
    description = db.Column(db.String(120), unique=False, nullable=False)
    status      = db.Column(db.String(6), unique=False, nullable=False)
    email       = db.Column(db.String(120), unique=False, nullable=False)
    @property
    def serialize(self):
        return {
            'description':self.description,
            'status'     :self.status,
            'email'      :self.email
       }
    # Задание составного ключа - уникальная пара полей
    __table_args__ = (
        db.UniqueConstraint('meeting_id','email'),
    )
    # Текстовое представление таблицы для print
    def __repr__(self):
        return '<Participant: %r>' % self.description
    
# Кусочек текста
class Record(db.Model):
    # Поля таблицы в БД
    record_id    = db.Column(db.Integer, primary_key=True)
    meeting_id   = db.Column(db.Integer, db.ForeignKey(Meeting.meeting_id), unique=False, nullable=False)
    meeting      = db.relationship('Meeting', backref=db.backref('record', lazy=True))
    input_text   = db.Column(db.String(255), unique=False, nullable=True)
    sort_num     = db.Column(db.Float, unique=False, nullable=False)
    # Сериализация данных
    @property
    def serialize(self):
        return {
            'record_id':self.record_id,
            'text'     :self.input_text,
            'sort_num' :self.sort_num
       }
    @property
    def serialize_text(self):
        return self.input_text
    # Текстовое представление таблицы для print
    def __repr__(self):
        return '<Text: %r>' % self.input_text
        
# Минутки встречи
class Minute(db.Model):
    # Поля таблицы в БД
    minute_id    = db.Column(db.Integer, primary_key=True)
    meeting_id   = db.Column(db.Integer, db.ForeignKey(Meeting.meeting_id), unique=False, nullable=False)
    meeting      = db.relationship('Meeting', backref=db.backref('minute', lazy=True))
    text         = db.Column(db.String(255), unique=False, nullable=True)
    sort_num     = db.Column(db.Float, unique=False, nullable=False)
    # Сериализация данных
    @property
    def serialize(self):
        return {
            'minute_id':self.minute_id,
            'text'     :self.text,
            'sort_num' :self.sort_num
       }
    @property
    def serialize_text(self):
        return self.input_text
    # Текстовое представление таблицы для print
    def __repr__(self):
        return '<Minute: %r>' % self.text
    
# Создаем БД в случае запуска модуля как отдельного скрипта
# Если модуль импортируется - не выполняется
if __name__ == '__main__':
    db.create_all()
