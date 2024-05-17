import sqlite3
from src.base import base_worker
from src.models import usersM,ordersM

def get_user(id):
    try:
        user = base_worker.insert_data(f"SELECT * FROM users WHERE id = {id}",())
        if user is None:
            return None
        user = {"id":user[0],"f_name":user[1],"s_name":user[2],"password":None,"email":user[4]}
        return user  
    except Exception as e:
        print(f"Ошибка {e}")
        return 500
    
def create_admin(user:usersM):
    try:
        insert_fields = ["f_name", "s_name", "password","email","role_id"]
        insert_values = [f"'{user.f_name}'",f"'{user.s_name}'",f"'{user.password}'",f"'{user.email}'",f"{1}"] # 1 !!!!!!!!!!!!!

        fields_str = ', '.join(insert_fields)
        values_str = ', '.join(insert_values)
    except Exception as e:
        print(f"Ошибка {e}")
        return 500

    try:
        new_id = base_worker.insert_data(f"""
        INSERT INTO users ({fields_str})
        VALUES ({values_str})
        RETURNING id;                                                                                                 
        """, ())    
        if new_id is None:
            return None                                                                                                    
        user = {"id":new_id[0],"f_name":user.f_name,"s_name":user.s_name,"password":None,"email":user.email}
        return user   
    except sqlite3.IntegrityError as e:
        print(f"Ошибка: {e}")
        return None
    
def upd_user(id, user: usersM): # сюда свой id из клинтка пихаем из обьекта
    try:
        update_fields = []

        if user.f_name is not None and user.f_name != '':
            update_fields.append(f"f_name = '{user.f_name}'")

        if user.s_name is not None and user.s_name != '':
            update_fields.append(f"s_name = '{user.s_name}'")

        if user.password is not None and user.password != '':
            update_fields.append(f"password = '{user.password}'")

        if user.email is not None and user.email != '':
            update_fields.append(f"email = '{user.email}'")

        update_fields_str = ', '.join(update_fields)

        try:
            user_id = base_worker.insert_data(f"""
            UPDATE users
            SET {update_fields_str}
            WHERE id = {id} 
            RETURNING id;
            """, ())
        except sqlite3.IntegrityError as e:
            print(f"Ошибка: {e}")
            return None

        user = {"id":user_id[0],"f_name":None,"s_name":None,"password":None,"email":None}
        return user  
    except Exception as e:
        print(f"Ошибка {e}")
        return 500

def del_user(id): 
    try:
        user_id = base_worker.insert_data(f"DELETE FROM users WHERE id = {id} RETURNING id;",())
        if user_id is None:
            return None
        else:
            user = {"id":user_id[0],"f_name":None,"s_name":None,"password":None,"email":None}
            return user  
    except Exception as e:
        print(f"Ошибка {e}")
        return 500
##########
def upd_order(id, order: ordersM):
    try:
        update_fields = []

        if order.order_date is not None and order.order_date != '':        # Дата заказы или что?
            update_fields.append(f"order_date = '{order.order_date}'")

        if order.status is not None and order.status != '':
            update_fields.append(f"status = '{order.status}'")

        update_fields_str = ', '.join(update_fields)

        try:
            order_id = base_worker.insert_data(f"""
            UPDATE orders
            SET {update_fields_str}
            WHERE id = {id} 
            RETURNING id;
            """, ())
        except sqlite3.IntegrityError as e:
            print(f"Ошибка: {e}")
            return None
        order = {"id":order_id[0],"user_id":None,"order_date":None,"sum":None,"status":None,"delivery_method_id":None,"payment_method_id":None}
        return order  
    except Exception as e:
        print(f"Ошибка {e}")
        return 500