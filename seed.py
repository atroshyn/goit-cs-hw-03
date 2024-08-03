import psycopg2
from create_table import create_connection
from config import *
import faker
from random import randint

def generate_fake_data(NUMBER_USERS, NUMBER_TASKS) -> tuple:
    fake_users = []
    fake_tasks = []

    fake_data = faker.Faker()

    for _ in range(NUMBER_USERS):
        fake_users.append({
            'fullname': fake_data.name(),
            'email': fake_data.email()
        })

    for _ in range(NUMBER_TASKS):
        fake_tasks.append({
            'title': fake_data.sentence(),
            'description': fake_data.text(),
            'status_id': randint(1, NUMBER_STATUSES), 
            'user_id': randint(1, NUMBER_USERS) 
        })

    return fake_users, fake_tasks

def prepare_data(users, statuses, tasks) -> tuple:
    for_users = []
    for user in users:
        for_users.append((user['fullname'], user['email']))
    
    for_statuses = []
    for status in statuses:
        for_statuses.append((status,))

    for_tasks = []
    for task in tasks:
        for_tasks.append((task['title'], task['description'], task['status_id'], task['user_id']))

    return for_users, for_statuses, for_tasks

def insert_data_to_db(users, statuses, tasks) -> None:
    with create_connection() as conn:
        cur = conn.cursor()

        sql_users = '''
        INSERT INTO users (fullname, email) VALUES (%s, %s)
        ON CONFLICT (email) DO NOTHING;
        '''
        cur.executemany(sql_users, users)

        sql_statuses = '''
        INSERT INTO statuses (name) VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
        '''
        cur.executemany(sql_statuses, statuses)

        sql_tasks = '''
        INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);
        '''
        cur.executemany(sql_tasks, tasks)

        conn.commit()

if __name__ == "__main__":
    users, tasks = generate_fake_data(NUMBER_USERS, NUMBER_TASKS)
    users, statuses, tasks = prepare_data(users, STATUSES, tasks)
    insert_data_to_db(users, statuses, tasks)
