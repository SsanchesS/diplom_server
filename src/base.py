import sqlite3
import os

class BaseWorker:

    def set_base_path(self, base_path: str):
        self.base_path = base_path

    def check_base(self) -> bool:
        print("Проверка наличия БД")
        return os.path.exists(self.base_path)

    def create_base(self, sql_file: str) -> None:
        print("Наполняем БД...")
        connection = sqlite3.connect(self.base_path)
        cur = connection.cursor()

        with open(sql_file, 'r', encoding='utf-8') as file:
            scripts = file.read()
            try:
                cur.executescript(scripts)
                connection.commit()
                print("БД создано")
            except sqlite3.Error as error:
                print(f"ОШИБКА!!!!!!! {error}")
            finally:
                connection.close()

    def insert_data(self, query: str, args: tuple[str]):
        print("Работа с БД...")
        connection = sqlite3.connect(self.base_path, isolation_level=None)
        cur = connection.cursor()
        res = cur.execute(query, args).fetchall()
        connection.commit()
        connection.close()
        return res
    
base_worker = BaseWorker()