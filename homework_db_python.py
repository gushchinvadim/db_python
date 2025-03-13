
import psycopg2
from psycopg2.sql import SQL, Identifier

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(database="postgres", user="postgres", password="postgres")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS phones (
                id SERIAL PRIMARY KEY,
                client_id INTEGER,
                phone_number TEXT,
                FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE
            )
        ''')
        self.connection.commit()

    def add_client(self, first_name, last_name, email):
        self.cursor.execute('''
            INSERT INTO clients (first_name, last_name, email) VALUES (%s, %s, %s)
        ''', (first_name, last_name, email))
        self.connection.commit()

    def add_phone(self, client_id, phone_number):
        self.cursor.execute('''
            INSERT INTO phones (client_id, phone_number) VALUES (%s, %s)
        ''', (client_id, phone_number))
        self.connection.commit()

    def update_client(self, id, first_name=None, last_name=None, email=None):

        arg_list = {'first_name': first_name, "last_name": last_name, 'email': email}
        for key, arg in arg_list.items():
            if arg:
                self.cursor.execute(SQL("UPDATE clients SET {}=%s WHERE id=%s").format(Identifier(key)),
                            (arg, id))
        self.connection.commit()

    def delete_phone(self, client_id, phone_id):
        self.cursor.execute('''
            DELETE FROM phones WHERE id = %s AND client_id = %s
        ''', (phone_id, client_id))
        self.connection.commit()

    def delete_client(self, client_id):
        self.cursor.execute('''
            DELETE FROM clients WHERE id = %s
        ''', (client_id,))
        self.connection.commit()

    def find_client(self, first_name=None,last_name=None, email=None):
        self.cursor.execute('''
            SELECT  id, first_name, last_name, email FROM clients
            WHERE first_name LIKE %s OR last_name LIKE %s OR email LIKE %s
        ''',  (first_name,last_name, email))
        return self.cursor.fetchall()

    def get_client_phones(self, client_id):
        self.cursor.execute('''
            SELECT phone_number FROM phones WHERE client_id = %s
        ''', (client_id,))
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    # with psycopg2.connect(database="postgres", user="postgres", password="postgres") as connection:

    db = Database()

    #Добавление клиента
    # db.add_client('Дмитрий', 'Иванов', 'iddvanov@example.com')
    # db.add_client('Ivan', 'Ivanoff', 'uuuvetrdov@example.com')

    # #Добавление телефонов для клиента
    # db.add_phone(1, '123456789')
    # db.add_phone(1, '987654321')
    # db.add_phone(2, '5565666777')

    #Поиск клиента
    # clients = db.find_client(first_name='Ivan')
    # print('Найденные клиенты:', clients)

    # Изменение данных клиента
    # db.update_client(2,first_name='Ivan')

    # Удаление телефона
    # db.delete_phone(1, 1)  # Удаляем первый телефон клиента с id 1
    #
    # # Получение телефонов клиента
    # phones = db.get_client_phones(1)
    # print('Телефоны клиента 1:', phones)

    # Удаление клиента
    # db.delete_client(7)

    # Закрытие базы данных
    db.close()