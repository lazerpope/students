import telebot
import sqlite3
from telebot import types

import os
import time
from decouple import config

TOKEN = config("TOKEN", default="пусто")


def category(uid):
    with sqlite3.connect("shop.db") as connection:
        cursor = connection.cursor()
        cursor.execute(""" SELECT * FROM Category """)
        res = cursor.fetchall()

    key1 = types.InlineKeyboardButton(f"{res[0][1]}", callback_data=f"kateg{res[0][0]}")
    key2 = types.InlineKeyboardButton(f"{res[1][1]}", callback_data=f"kateg{res[1][0]}")
    key3 = types.InlineKeyboardButton(f"{res[2][1]}", callback_data=f"kateg{res[2][0]}")
    key4 = types.InlineKeyboardButton(f"{res[3][1]}", callback_data=f"kateg{res[3][0]}")
    add = [key1, key2, key3, key4]

    keyboard = types.InlineKeyboardMarkup([add])
    bot.send_message(uid, text="Выберите категорию товаров:", reply_markup=keyboard)


# =================================================================
def choice(uid, call):
    with sqlite3.connect("shop.db") as connection:
        cursor = connection.cursor()
        print(call[5:], "<<<------- категория при вызове")
        cursor.execute(
            """ SELECT name,artikul,balance FROM Product WHERE catigory_id =?""",
            (call[5:],),
        )
        res = cursor.fetchall()

    def price(art):
        """получить цену продукта"""
        # print(art)
        with sqlite3.connect("shop.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                """ SELECT price FROM Price WHERE artikul =?""",
                (art,),
            )
            res = cursor.fetchone()[0]
        return res

    list_key = []
    for i in range(len(res)):
        for j in range(1):
            key_plus = types.InlineKeyboardButton(
                f"➖",
                callback_data=f"min{res[i][1]}",
            )

            key_minus = types.InlineKeyboardButton(
                f"➕",
                callback_data=f"pls{res[i][1]}",
            )

            list_key.append(key_plus)
            # list_key.append(key)
            list_key.append(key_minus)

            keyboard = types.InlineKeyboardMarkup([list_key])

            bot.send_message(
                uid,
                text=f"{res[i][0]} Цена: {price(res[i][1])}р",
                reply_markup=keyboard,
            )

            list_key.clear()


bot = telebot.TeleBot(TOKEN)
command = telebot.types.BotCommand("start", "Показать категории")
bot.set_my_commands([command])


@bot.message_handler(commands=["start"])
def start(message):
    uid = message.chat.id
    category(uid)
    # ----------------------------- КНОПКИ ВЫБОРА КАТЕГОРИЙ ---------------------------------


@bot.callback_query_handler(func=lambda call: call.data.startswith("kateg"))
def handle_answer(call):
    uid = call.from_user.id
    print(call.data, " <<<<=========== категория из меню")
    choice(uid, call.data)
    category(uid)


# ================================ ЧЕК =================================


@bot.callback_query_handler(func=lambda call: call.data.startswith(("pls", "min")))
def handle_answer(call):
    print(call.data)
    uid = call.from_user.id
    # ---------------------------------------------------------------
    def balance(artikul) -> int:
        """Получает артикул - возвращает остаток товара"""
        with sqlite3.connect("shop.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                """ SELECT balance FROM Product 
                    WHERE Product.artikul =?""",
                (artikul,),
            )
            res_artikul = cursor.fetchone()[0]
            # connection.close()
        return res_artikul

    # -----------------------------------------------------------------
    def update(uid, action, artikul) -> None:

        with sqlite3.connect("shop.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                """ SELECT name,price,balance,catigory_id FROM Product 
                    JOIN Price ON Product.artikul = Price.artikul
                    WHERE Product.artikul =?""",
                (artikul,),
            )
            res = cursor.fetchall()
            name_product = res[0][0]
            price = res[0][1]
            kateg_id = res[0][3]
            print(f"{res} Имя - цена - остаток - категория")

            cursor.execute(
                """SELECT * FROM Basket WHERE user_id =? AND name=?""",
                (
                    uid,
                    name_product,
                ),
            )
            res = cursor.fetchone()
            action = call.data[:3]

            if res == None and action == "pls":
                print(action)
                total_sum = price
                cnt_qty = 1
                # ------------------------------------------------ ПЕРВАЯ ПОКУПКА ---------------------------
                with sqlite3.connect("shop.db") as connection:

                    try:
                        cursor.execute(
                            """ INSERT INTO Basket (name,price,qty,total_sum,user_id,artikul,kol_vo,kategory_id) VALUES (?,?,?,?,?,?,?,?)""",
                            (
                                name_product,
                                price,
                                cnt_qty,
                                total_sum,
                                uid,
                                artikul,
                                balance(artikul) - 1,
                                kateg_id,
                            ),
                        )
                        connection.commit()

                        # ------------------------- ВЫВОД ЧЕКА -------------------------------------------

                        cursor.execute(
                            """SELECT name,price,qty,total_sum,user_id,artikul,kol_vo,kategory_id FROM Basket WHERE user_id =?""",
                            (uid,),
                        )
                        res = cursor.fetchall()

                     
                    except Exception as e:

                        print(e)
                    




                    # -----------------------------------------
                print(res, "<<<============ 1 й чеk")

                print(
                    f"|======================= ЧЕК ==================================|"
                )
                total = 0
                itog_1 = ""
                for i in range(len(res)):
                    total += res[i][3]

                    print(
                        f" {res[i][0]} - {res[i][1]} руб.  Кол-во {res[i][2]} ед.   Сумма - {res[i][3]} р.   Остаток - {balance(res[i][5])-res[i][2]} КАТЕГ {res[i][7]}"
                    )
                    print(
                        f" ---------------------------------------------------------------------------------------------"
                    )
                    itog_1 += f" \n{res[i][0]} - {res[i][1]} руб.  Кол-во {res[i][2]} ед.   Сумма - {res[i][3]} р.   Остаток - {res[i][6]}\n---------------------------------------------------------------------- "

                bot.send_message(uid, itog_1)

                # --------------------------------------------------------------------
                key4 = types.InlineKeyboardButton(
                    f"Купить", callback_data=f"yes"
                )
                add = [key4]
                keyboard1 = types.InlineKeyboardMarkup([add])
                bot.send_message(
                    uid, text=f" Итого: {total}", reply_markup=keyboard1
                )

                print(f" Итого: {total}")
                print(
                    f"|==============================================================|"
                )

                category(uid)
                choice(uid, "kateg" + str(res[-1][7]))
                return
        
                # ---------------------------------------------
            try:
                cnt_qty = res[3]
                name_chek = res[1]
                total_chek = res[4]
            except Exception as e:
                print(e)

            finally:
                ...
            bal_chek = res[7]
            print(bal_chek, "=============================")
            if action == "pls":
                cnt_qty += 1
                total_chek += price
                bal_chek -= 1

            elif action == "min":
                cnt_qty -= 1
                total_chek -= price
                bal_chek += 1

            cursor = connection.cursor()
            try:
                cursor.execute(
                    """ UPDATE Basket SET qty=?, total_sum = ?, kol_vo=? WHERE user_id =? AND name=?""",
                    (
                        cnt_qty,
                        total_chek,
                        bal_chek,
                        uid,
                        name_chek,
                    ),
                )
            except Exception as e:
                print(e)
            connection.commit()

        cursor.execute(
            """SELECT name,price,qty,total_sum,user_id,artikul,kol_vo,kategory_id FROM Basket WHERE user_id =?""",
            (uid,),
        )
        res = cursor.fetchall()

        connection.close()

        # ============================ ПОКАЗАТЬ ЧЕК В КОНСОЛИ И В БОТЕ ==============================================

        def get_chek(res: list [list[]]=None):
            print(
                f"|====================================== ЧЕК ==================================|"
            )
            total = 0
            itog = ""
            bot.send_message(uid, text="⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇")

            for i in range(len(res)):
                total += res[i][3]

                print(
                    f" {res[i][0]} - {res[i][1]} руб.    Кол-во {res[i][2]} ед.     Сумма - {res[i][3]} р.  Остаток - {balance(res[i][5])-res[i][2]} "
                )
                print(
                    f" ---------------------------------------------------------------------------"
                )
                itog += f" \n{res[i][0]} - {res[i][1]} руб.  Кол-во {res[i][2]} ед.   Сумма - {res[i][3]} р.   Остаток - {res[i][6]}\n------------------------------------------------------------------------"

            bot.send_message(uid, itog)

            print(f" Итого: {total}")
            print(
                f"|=============================================================================|"
            )
            key4 = types.InlineKeyboardButton(f"Купить", callback_data=f"yes")
            add = [key4]

            keyboard1 = types.InlineKeyboardMarkup([add])
            bot.send_message(uid, text=f" Итого: {total}", reply_markup=keyboard1)

        get_chek(res)
        # kateg1
        print(res, "res[0][3]")
        choice(uid, "kateg" + str(res[-1][7]))
        category(uid)

    action = call.data[:3]
    artikul = call.data[3:]
    update(uid, action, artikul)


# ================================== ПОКУПКА ===========================================
@bot.callback_query_handler(func=lambda call: call.data.startswith(("yes")))
def handle_answer(call):
    uid = call.from_user.id
    with sqlite3.connect("shop.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """ SELECT user_id, name, qty, total_sum, price,kol_vo
                FROM Basket 
                WHERE user_id =?""",
            (uid,),
        )
        res = cursor.fetchall()

        cursor.execute("""SELECT id FROM Orders""")
        try:
            count_id = cursor.fetchall()[-1][0]
        except Exception as e:
            print(e)
            count_id = 0
        print(count_id)

        for i in range(len(res)):
            cursor.execute(
                """ INSERT INTO Orders (id, client_id, name_product,price, kol_vo,sum) VALUES(?,?,?,?,?,?)""",
                (count_id + 1, res[i][0], res[i][1], res[i][4], res[i][2], res[i][3]),
            )
        cursor.execute("""SELECT artikul,qty FROM Basket WHERE user_id = ?""", (uid,))
        upd = cursor.fetchall()
        print(upd)
        for i in range(len(upd)):

            cursor.execute(
                """UPDATE Product SET balance = balance - ? WHERE artikul = ?""",
                (upd[i][1], upd[i][0]),
            )

        cursor.execute("""DELETE FROM Basket WHERE user_id = ? """, (uid,))
        connection.commit()
        connection.close()
        bot.send_message(uid, f"Куплено  👍🏻")
        category(uid)


bot.infinity_polling()
# =================================================================
# with sqlite3.connect("shop.db") as connection:
#     cursor = connection.cursor()
#     res = cursor.execute(""" SELECT * FROM Img """)

# img = list(res)[0][1]

# with open(img, "rb") as img_file:
#     img_data = img_file.read()

# with open("123.jpg", "wb") as file:
#     file.write(img_data)

# connection.close()
# =========================

# lockfile_path = "my_bot.lock"


# def check_lockfile():
#     return os.path.exists(lockfile_path)


# def create_lockfile():
#     with open(lockfile_path, "w") as lockfile:
#         lockfile.write("Bot is running")


# def remove_lockfile():
#     if check_lockfile():
#         os.remove(lockfile_path)


# def main():
#     if check_lockfile():
#         print("Another instance of the bot is already running.")
#         return

#     create_lockfile()
#     print("Bot started.")

#     try:
#         # Основной код вашего бота
#         while True:
#             print("Bot is running...")
#             time.sleep(10)  # Пауза для примера
#     finally:
#         remove_lockfile()
#         print("Bot stopped.")


# if __name__ == "__main__":
#     main()
