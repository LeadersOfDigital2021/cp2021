# Импорт модулей
import re
from meety_orm import User

# Получение пользователя по enail (email уникален для таблицы)
def get_user_by_email(email):
    try:
        return User.query.filter(User.email == re.search(r'[\w\.-]+@[\w\.-]+', email).group()).first().user_id
    except AttributeError:
        return None
