from create_table import create_connection

def execute_query(sql: str, params: tuple = (), query_number: int = 1) -> None:
    print(f"\n--- Запит {query_number} ---\n")
    with create_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        
        if sql.strip().upper().startswith("SELECT"):
            results = cur.fetchall()
            for row in results:
                print(row)
        else:
            conn.commit()
            print("Запит виконано успішно.")

if __name__ == "__main__":
    
    # Отримати всі завдання певного користувача
    user_id = 2  
    sql_1 = """
    SELECT *
    FROM users as u
    LEFT JOIN tasks as t ON u.id = t.user_id
    WHERE u.id = %s;
    """
    execute_query(sql_1, (user_id,), query_number=1)

    # Вибрати завдання за певним статусом
    status_name = 'new'
    sql_2 = """
    SELECT *
    FROM tasks as t
    WHERE t.status_id = (
        SELECT id
        FROM statuses
        WHERE name = %s
    );
    """
    execute_query(sql_2, (status_name,), query_number=2)

    # Оновити статус конкретного завдання
    task_id = 1
    new_status_name = 'in progress'
    sql_3 = """
    UPDATE tasks
    SET status_id = (
        SELECT id
        FROM statuses
        WHERE name = %s
    )
    WHERE id = %s;
    """
    execute_query(sql_3, (new_status_name, task_id), query_number=3)

    # Отримати список користувачів, які не мають жодного завдання
    sql_4 = """
    SELECT *
    FROM users
    WHERE id NOT IN (
        SELECT DISTINCT user_id
        FROM tasks
    );
    """
    execute_query(sql_4, query_number=4)

    # Додати нове завдання для конкретного користувача
    new_task_title = "New Task"
    new_task_description = "Description of new task"
    new_task_status = 'new'
    new_task_user_id = 2
    sql_5 = """
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES (%s, %s, (SELECT id FROM statuses WHERE name = %s), %s);
    """
    execute_query(sql_5, (new_task_title, new_task_description, new_task_status, new_task_user_id), query_number=5)

    # Отримати всі завдання, які ще не завершено
    sql_6 = """
    SELECT *
    FROM tasks
    WHERE status_id != (
        SELECT id
        FROM statuses
        WHERE name = 'completed'
    );
    """
    execute_query(sql_6, query_number=6)

    # Видалити конкретне завдання
    delete_task_id = 1
    sql_7 = """
    DELETE FROM tasks
    WHERE id = %s;
    """
    execute_query(sql_7, (delete_task_id,), query_number=7)

    # Знайти користувачів з певною електронною поштою
    email_pattern = '%@example.com'
    sql_8 = """
    SELECT *
    FROM users
    WHERE email LIKE %s;
    """
    execute_query(sql_8, (email_pattern,), query_number=8)

    # Оновити ім'я користувача
    update_user_id = 1
    new_fullname = "Updated Name"
    sql_9 = """
    UPDATE users
    SET fullname = %s
    WHERE id = %s;
    """
    execute_query(sql_9, (new_fullname, update_user_id), query_number=9)

    # Отримати кількість завдань для кожного статусу
    sql_10 = """
    SELECT s.name, COUNT(t.id) as task_count
    FROM statuses s
    LEFT JOIN tasks t ON s.id = t.status_id
    GROUP BY s.name;
    """
    execute_query(sql_10, query_number=10)

    # Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
    domain_pattern = '%@example.com'
    sql_11 = """
    SELECT t.*
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    WHERE u.email LIKE %s;
    """
    execute_query(sql_11, (domain_pattern,), query_number=11)

    # Отримати список завдань, що не мають опису
    sql_12 = """
    SELECT *
    FROM tasks
    WHERE description IS NULL;
    """
    execute_query(sql_12, query_number=12)

    # Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
    status_in_progress = 'in progress'
    sql_13 = """
    SELECT u.*, t.*
    FROM users u
    JOIN tasks t ON u.id = t.user_id
    WHERE t.status_id = (
        SELECT id
        FROM statuses
        WHERE name = %s
    );
    """
    execute_query(sql_13, (status_in_progress,), query_number=13)

    # Отримати користувачів та кількість їхніх завдань
    sql_14 = """
    SELECT u.fullname, COUNT(t.id) as task_count
    FROM users u
    LEFT JOIN tasks t ON u.id = t.user_id
    GROUP BY u.fullname;
    """
    execute_query(sql_14, query_number=14)
