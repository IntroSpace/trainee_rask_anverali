import requests
import psycopg2


BITRIX_WEBHOOK_GET = ''  # Ссылка на WebHook Битрикса (для получения данных)
BITRIX_WEBHOOK_UPDATE = ''  # Ссылка на WebHook Битрикса (для обновления данных)
DBNAME = ''  # Имя базы данных
USER = ''  # Имя админа БД
PASSWORD = ''  # Пароль админа БД
HOST = ''  # Хост для подключения к БД
PORT = ''  # Порт для подключения к БД
CONTACT_ID = ''  # ID интересующего нас контакта


def get_contact_data(contact_id):
    params = {
        'filter': {
            'ID': contact_id
        },
        'select': ['NAME', 'ID']
    }
    response = requests.get(BITRIX_WEBHOOK_GET, params=params)
    return response.json()['result'][0]


def check_name_in_db(name, gender_table):
    conn = psycopg2.connect(
        dbname=DBNAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    cursor = conn.cursor()
    query = f"SELECT * FROM {gender_table} WHERE name = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None


def update_contact_gender(contact_id, gender):
    params = {
        'ID': contact_id,
        'GENDER': gender
    }
    response = requests.post(BITRIX_WEBHOOK_UPDATE, json=params)
    return response.json()['result']


def main():
    contact_data = get_contact_data(CONTACT_ID)

    name = contact_data['NAME']
    gender = 'Неизвестно'
    if check_name_in_db(name, 'names_man'):
        gender = 'Мужчина'
    elif check_name_in_db(name, 'names_woman'):
        gender = 'Женщина'

    update_contact_gender(CONTACT_ID, gender)


if __name__ == '__main__':
    main()
