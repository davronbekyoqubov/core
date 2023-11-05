
# This is Main (Public) file

# Main liblaries
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import sqlite3
import logging

# Config Data
from config import *

# Media files (cloud import)
# Datas files
from clouds import *
from address import *

# This is Bot's Basic Settings !
API_TOKEN = Bot(token = BOT_TOKEN, parse_mode="HTML")
bot = Dispatcher(API_TOKEN)
botName = str("Hi Germany Bot")

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Database


# Import SQLAlchemy and create an engine
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL. Replace 'sqlite:///mydatabase.db' with your SQLite database path.
DATABASE_URL = 'sqlite:///users.db'

# Create an engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create a base class for declarative models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    username = Column(String(255))
    firstname = Column(String(255))
    first_interaction = Column(Boolean, default=True)
    selected_language = Column(String(2), default="uz")  # Add a column for selected language

# Create the users table if it doesn't exist
Base.metadata.create_all(engine)


# Users request, (helps)
conn = sqlite3.connect('messages.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  message_text TEXT
                )''')
conn.commit()

# Admins request, (important with (admins))
conn_admins = sqlite3.connect('admins.db')
cursor_admins = conn_admins.cursor()

cursor_admins.execute('''CREATE TABLE IF NOT EXISTS admins (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  admin_id INTEGER
                )''')
conn_admins.commit()


try:
    # This is Main Buttons
    couBut = InlineKeyboardButton(text="📚 Kurslar (new)")
    useBut = InlineKeyboardButton(text="💎 Foydali Ma'lumotlar (new)")
    AscBut = InlineKeyboardButton(text="☎️ Bog'lanish")
    aboutBut = InlineKeyboardButton(text="📜 Biz haqimizda")
    messABut = InlineKeyboardButton(text="👨‍💻 Yordam | Habar yozish")
    setBut= InlineKeyboardButton(text="⚙️ Sozlamalar (set)")
    keyboard_inline = InlineKeyboardMarkup().add(couBut, useBut, AscBut, aboutBut, messABut, setBut)

    keyboards = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(couBut,
                                    useBut, AscBut, aboutBut, messABut, setBut)
    
    couBut_ru = InlineKeyboardButton(text="📚 Курсы (новые)")
    useBut_ru = InlineKeyboardButton(text="💎 Полезная информация (new)")
    AscBut_ru = InlineKeyboardButton(text="☎️ Связь")
    aboutBut_ru = InlineKeyboardButton(text="📜 О нас")
    messABut = InlineKeyboardButton(text="👨‍💻 Помощь | Написать сообщение")
    setBut_ru = InlineKeyboardButton(text="⚙️ Настройки (set)")
    keyboard_inline_ru = InlineKeyboardMarkup().add(couBut_ru,
                                            useBut_ru, AscBut_ru, aboutBut_ru, messABut, setBut_ru)

    keyboards_ru = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(couBut_ru,
                                            useBut_ru, AscBut_ru, aboutBut_ru, messABut, setBut_ru)
    
    # Select language
    
    def selectsLanguages():
        keyboard = types.InlineKeyboardMarkup()
        btn_uz = types.InlineKeyboardButton("🇺🇿 O'zbek", callback_data='uz')
        btn_ru = types.InlineKeyboardButton("🇷🇺 Русский", callback_data='ru')
        keyboard.add(btn_uz, btn_ru)

        return keyboard
    
    def getUserLanguage(user_id):
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            return user.selected_language
        return None


    # This is "Follov" channel buttons function
    def followChannel():
        channel = InlineKeyboardButton(
            text="➡️ Obuna Bo'lish (Подписаться)",
            url=CHANNEL_URLS
        )
        check_follow = InlineKeyboardButton(
            text="✅ Tekshirish (проверять)",
            callback_data="subdone"
        )
        chAllBtn = InlineKeyboardMarkup(row_width=1).add(channel, check_follow)

        return chAllBtn


    @bot.message_handler(commands=['start', 'hello', 'hi', 'restart'])
    async def welcome(message: types.Message):
        # Users Data

        # Check if the user is already in the database
        user = session.query(User).filter_by(user_id=message.from_user.id).first()

        if not user:
            # User is interacting for the first time, save their data
            user = User(
                user_id=message.from_user.id,
                username=message.from_user.username,
                firstname=message.from_user.first_name
            )
            session.add(user)
            session.commit()
    
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()
        
        # Check System follow
        checkSubChan = await API_TOKEN.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)

        userName = str(message.chat.first_name)
        welToUz = f"<b>✋ <em>{ userName }</em>, <em>{ botName }</em> - ga xush kelibsiz.</b>"
        welToRu = f"<b>✋ <em>{ userName }</em>, <em>{ botName }</em> - Добро пожаловать в бот.</b>"
        user_id = message.from_user.id


        if checkSubChan['status'] != 'left':
            if user.selected_language == "uz":
                await message.answer(welToUz)
            elif user.selected_language == "ru":
                await message.answer(welToRu)
            if not user:
                if user.selected_language == "uz":
                    await message.answer(welToUz)
                elif user.selected_language == "ru":
                    await message.answer(welToRu)

                await message.answer(
                    text=f"<b><em>{ userName }, Tilni tanlang / Выберите язык</em></b>",
                    reply_markup=selectsLanguages()
                )
            else:
                if user.selected_language == "uz":
                    await message.answer(
                        text="<b><em>Menuni tanlang: </em></b>",
                        reply_markup=keyboards,
                    )
                elif user.selected_language == "ru":
                    await message.answer(
                        text="<b><em>Выберите меню: </em></b>",
                        reply_markup=keyboards_ru,
                    )
            
        else:
            await message.answer(
                text = f"<b>✋ <em>{ userName }, { botName } ga xush kelibsiz. \n(Добро пожаловать в бот.)</em> \n\n❗️ <em>{ userName }</em>, Botdan foydalanish uchun Kanalimizga obuna bo'ling. \n(Подпишитесь на наш канал, чтобы посетить бота.)</b>",
                reply_markup=followChannel()
            )

            
    @bot.callback_query_handler(lambda checkSub: checkSub.data=="subdone")
    async def checkSubMes(callback: types.CallbackQuery):
        checkSubChan = await API_TOKEN.get_chat_member(chat_id=CHANNEL_ID, user_id=callback.from_user.id)
        userName = str(callback.message.chat.first_name)

        if callback.data == "subdone":
            if checkSubChan['status'] != 'left':
                await callback.message.answer(
                    text = f"<b>🎉 <em>{ userName }</em>, Tabriklaymiz endi botimizdan to'liq foydalanishingiz mumkin. \n\n(Поздравляем, теперь наш бот полностью обнаруживает его.)</b>",
                    # reply_markup=keyboards
                )
                await callback.message.answer(
                    text=f"<b><em>Tilni tanlang / Выберите язык</em></b>",
                    reply_markup=selectsLanguages()
                )
            else:
                await callback.message.answer(
                    text = f"<b>❌ <em>{ userName }</em>, hali kanalimizga obuna bo'lmadingiz. \n\n(Вы еще не подписаны на наш канал.)</b>",
                    reply_markup=followChannel()
                )



    @bot.callback_query_handler(lambda c: c.data in ['uz', 'ru'])
    async def process_callback(callback_query: types.CallbackQuery):
        selected_language = callback_query.data
        user_id = callback_query.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        if user:
            user.selected_language = selected_language
        else:
            new_user = User(user_id=user_id, selected_language=selected_language)
            session.add(new_user)

        session.commit()
        
        logging.info(f"Foydalanuvchi (ID: {user_id}) tanlagan til: { selected_language }")
        
        try:
            if selected_language == 'uz':
                await bot.bot.send_message(
                    user_id,
                    text=f"<b>🇺🇿 Siz <em>O'zbek</em> tilini tanladingiz</b>",
                    reply_markup=keyboards,
                )
            elif selected_language == 'ru':
                await bot.bot.send_message(
                    user_id,
                    text=f"<b>🇷🇺 Вы выбрали <em>Русский</em></b>",
                    reply_markup=keyboards_ru,
                )
        except Exception as e:
            logging.error(f"Xatolik: {e}")
            
            await bot.bot.send_message(user_id, text=f"Siz { selected_language } tilini tanladingiz. Xatolik sodir bo'ldi va xabar yetkazilmadi.")

    
    @bot.message_handler(text="🔄 Tilni o'zgartirish / Изменение языка")
    async def settings(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()
        
        if user:
            await message.answer("<b>🔁 Tilni o'zgartirish / Изменить язык</b>", reply_markup=selectsLanguages())
        else:
            # Foydalanuvchi hali tanlagan tili yo'q
            await message.answer("🥺 Iltimos, birorta til tanlang / Выберите язык.")


    @bot.message_handler(lambda message: message.text in ["👨‍💻 Yordam | Habar yozish", "👨‍💻 Помощь | Написать сообщение"])
    async def helpMess(message: types.Message):
        userData = message.from_user.first_name
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first() 
        messagetext = f"<b>👨‍💻 <em>Yordam</em> yoki <em>Habar yozish</em></b> \n\n{ userData }, <em>siz bu bo'lim orqali, Biznig xodimlarimizga bot yuzasizdan qandaydir #Xatoliklar, #Tushunmovchiliklar yoki Qandaydir #Yodam yuzasidan murojaat qilishingiz mumkun.</em> \n\n<b><em>Biz imkon qadar murojatingiznchi o'qib haq qilishg harakat qilamiz !</em></b>"
        reMessageF = f"<b>💬 Murojaat qilish tartibi!</b> \n\n/mail Assalomu Aleykum. Menga shu masala bo'yicha yordam bera olasizmi. Bla bla bla... \nTelefon #raqam Yoki Telegram #username \n\n<b>P.S. Murojatingiz boshida <em>/mail</em> yozishni unutmang aks holsa soʻrovingizni xodimlarimiz javobsiz qoldirishi mumkun ❗️</b>"

        messagetextRu = f"<b>👨‍💻 <em>Напишите помощь или сообщение</em></b> \n\n{ userData }, <em>Через этот раздел вы можете связаться с нашими сотрудниками по поводу любых #Ошибок, #Недопониманий или #Воспоминаний.</em> \n\n<b><em>Мы постараемся прочитать Ваш запрос максимально внимательно !</em></b>"
        reMessageFRu = f"<b>💬Порядок подачи заявки!</b> \n\n/mail Здравствуйте. Можете ли вы дать мне несколько советов по этому поводу? Бла бла бла... \n#номер телефона или Telegram #имя пользователя \n\n<b>P.S. Не забудьте написать <em>/mail</em> в начале заявки, иначе наши сотрудники могут оставить ваш вопрос без ответа ❗️</b>"

        if user.selected_language == "uz":
            await message.answer_photo(
                helpCenter,
                messagetext,
            )
            await message.answer(reMessageF)

        elif user.selected_language == "ru":
            await message.answer_photo(
                helpCenter,
                messagetextRu,
            )
            await message.answer(reMessageFRu)

    @bot.message_handler(commands=['mail'])
    async def userAdminMessage(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        user_id = message.from_user.id
        message_text = message.get_args()

        if user.selected_language == "uz":
            if not message_text:
                await message.reply("💬 /mail Xabar matnini yuboring")
            else:
                cursor.execute("INSERT INTO messages (user_id, message_text) VALUES (?, ?)", (user_id, message_text))
                conn.commit()
                await message.reply("<b><em>✅ Xabaringiz hodimlarimizga muvoffaqiyatni jo'natildi.</em></b>")

        elif user.selected_language == "ru":
            if not message_text:
                await message.reply("💬 /mail Отправить текст сообщения")
            else:
                cursor.execute("INSERT INTO messages (user_id, message_text) VALUES (?, ?)", (user_id, message_text))
                conn.commit()
                await message.reply("<b><em>✅ Ваше сообщение успешно отправлено нашим сотрудникам.</em></b>")


    @bot.message_handler(commands=['admin'])
    async def admin_command(message: types.Message):
        userName = str(message.chat.first_name)

        if message.from_user.id in admins.values():
            admin_options = [
                [
                    types.InlineKeyboardButton(text="📊 Bot Statitikasi", callback_data="chart"),
                    types.InlineKeyboardButton(text="➕ Add Admins", callback_data="add_admins"),
                ],
                [
                    types.InlineKeyboardButton(text="✍️ Bot foydalanuvchilarga xabar yuborish", callback_data="message_admin"),
                ],
                [   
                    types.InlineKeyboardButton(text="💬 Foydalanuvchilardan kelgan Xabarlarni o'qish", callback_data="read_add_mess"),
                ],
            ]

            keyboards = types.InlineKeyboardMarkup(inline_keyboard=admin_options)

            await message.answer(
                text=f"<b><em>🤖 { botName }</em> ni Xodimlar boshqaruv paneli (v2.1) \n\n✋ <em>{ userName }, Admin</em> Xush kelibsiz. \n\nMenuni tanlang:</b>",
                reply_markup=keyboards
            )

        else:
            await message.reply(f"❌ <em>{ userName }</em> Siz Admin Emassiz ❗️")

    @bot.message_handler(text="🔙 Back Admin Menu")
    async def admin_command(message: types.Message):
        userName = str(message.chat.first_name)

        if message.from_user.id in admins.values():
            admin_options = [
                [
                    types.InlineKeyboardButton(text="📊 Bot Statitikasi", callback_data="chart"),
                    types.InlineKeyboardButton(text="➕ Add Admins", callback_data="add_admins"),
                ],
                [
                    types.InlineKeyboardButton(text="✍️ Bot foydalanuvchilarga xabar yuborish", callback_data="message_admin"),
                ],
                [   
                    types.InlineKeyboardButton(text="💬 Foydalanuvchilardan kelgan Xabarlarni o'qish", callback_data="read_add_mess"),
                ],
            ]

            keyboards = types.InlineKeyboardMarkup(inline_keyboard=admin_options)

            await message.answer(
                text=f"<b><em>🤖 { botName }</em> ni Xodimlar boshqaruv paneli (v2.1) \n\n✋ <em>{ userName }, Admin</em> Xush kelibsiz. \n\nMenuni tanlang:</b>",
                reply_markup=keyboards
            )

        else:
            await message.reply(f"❌ <em>{ userName }</em> Siz Admin Emassiz ❗️")

    @bot.callback_query_handler(lambda callback_query: callback_query.data in ["backhomeadmin"])
    async def admin_command(callback: types.CallbackQuery):
        userName = str(callback.message.chat.first_name)

        admin_options = [
                [
                    types.InlineKeyboardButton(text="📊 Bot Statitikasi", callback_data="chart"),
                    types.InlineKeyboardButton(text="➕ Add Admins", callback_data="add_admins"),
                ],
                [
                    types.InlineKeyboardButton(text="✍️ Bot foydalanuvchilarga xabar yuborish", callback_data="message_admin"),
                ],
                [   
                    types.InlineKeyboardButton(text="💬 Foydalanuvchilardan kelgan Xabarlarni o'qish", callback_data="add_admins"),
                ],
            ]

        keyboards = types.InlineKeyboardMarkup(inline_keyboard=admin_options)

        await callback.message.answer(
            text=f"<b><em>🤖 { botName }</em> ni Xodimlar boshqaruv paneli (v2.1) \n\n✋ <em>{ userName }, Admin</em> Xush kelibsiz. \n\nMenuni tanlang:</b>",
            reply_markup=keyboards
        )

    @bot.callback_query_handler(lambda callback_query: callback_query.data == 'chart')
    async def chartAdmin(callback_admin_query: types.CallbackQuery):
        if callback_admin_query.from_user.id in admins.values():
            chart_options = [
                        [
                            types.InlineKeyboardButton(text="🔢 Ja'mi foydalanuvchilar soni", callback_data="totUsers"),
                        ],
                        [
                            types.InlineKeyboardButton(text="👥 So'ngi foydalanuvchilar ro'yhati", callback_data="lastUsers"),
                        ],
                        [
                            types.InlineKeyboardButton(text="🔙 Back Admin Menu", callback_data="backhomeadmin"),
                        ]
                    ]

            keyboards = types.InlineKeyboardMarkup(inline_keyboard=chart_options)
        else:
            chart_options = [
                        [
                            types.InlineKeyboardButton(text="🔢 Ja'mi foydalanuvchilar soni", callback_data="totUsers"),
                        ],
                        [
                            types.InlineKeyboardButton(text="👥 So'ngi foydalanuvchilar ro'yhati", callback_data="lastUsers"),
                        ],
                    ]

            keyboards = types.InlineKeyboardMarkup(inline_keyboard=chart_options)

        await callback_admin_query.message.answer(
            text=f"<b><em>🤖 { botName }</em> \n\nMenuni tanlang:</b>",
            reply_markup=keyboards
        )

    @bot.callback_query_handler(lambda callback_query: callback_query.data == 'totUsers')
    async def totUseAdmin(callback_admin_query: types.CallbackQuery):
        total_users = session.query(User).count()
        await callback_admin_query.message.answer(f"<b>{ botName } - ja'mi foydalanuvchilar soni: <em>\"{ total_users }\"</em></b>")

    @bot.callback_query_handler(lambda callback_query: callback_query.data == 'lastUsers')
    async def lasUseAdmin(callback_admin_query: types.CallbackQuery):
        last_20_users = session.query(User.username, User.firstname).order_by(User.id.desc()).limit(35).all()

        response = f"<b>{ botName } - Eng so'nggi 35 ta foydalanuvchilar: \n\n</b>"
        for user in last_20_users:
            response += f"@{user.username} {user.firstname}\n"

        await callback_admin_query.message.answer(response)

    @bot.callback_query_handler(lambda callback_query: callback_query.data == 'add_admins')
    async def addAdmins(callback_data: types.CallbackQuery):
        userName = callback_data.from_user.first_name
        user_id = callback_data.from_user.id

        back_options = [
                    [
                        types.InlineKeyboardButton(text="🔙 Back Admin Menu", callback_data="backhomeadmin"),
                    ]
                ]

        keyboards = types.InlineKeyboardMarkup(inline_keyboard=back_options)
        
        if user_id in admins.values():
            await callback_data.message.answer(
                text=f"<b><em>``🤖 Hi Germany Bot ni Xodimlar boshqaruv paneli (v2.1)``</em> - uchun Admin (l3) qo'shmoqchisiz. \n\n❗️ (Muhim). { userName } siz Admin qo'shish orqali botning 80% boshqaruvini Adminga topshirasiz.</b>"
            )
            await callback_data.message.answer(
                text=f"<b><em>{ userName } Adminlik boshqaruv ruhsatnomangiz Admin (l2)</em> \n\nAdmin qo'shish maxsus \"/addadminset admin_id\" kamandasi orqali amalga oshiriladi. \n\n/addadminset kamandasi va shu kamandadan keyin qo'shilmoqchi bo'lgana adminning #user_id kiritiladi. \n\n<em>❗️ Eslatmalar</em>\n#1./addadminset kamandasi bo'lmasa bot bunday #id ni tasdiqlamaydi. \n#2. /addadminset keyin #raqamlar bo'lishi muhim. \n#3. /addadminset keyin raqamlardan tashqari hech qanday so'z bo'lmasligi kerak \n#4. /addadminset orqali siz admin qo'shishga rozilik bildirasiz.</b>",
                reply_markup=keyboards
            )
        else:
            await callback_data.message.reply(f"❌ <em>{ userName }</em> Siz Admin Emassiz ❗️")


    @bot.message_handler(commands=['addadminset'])
    async def userAdminMessage(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()


        user_id = message.from_user.id
        userName = message.from_user.first_name
        admin_id = message.get_args()
        if user_id in admins.values():
            if user.selected_language == "uz":
                if not admin_id:
                    await message.reply("🆔 Main Admin \"/addadminset\" orqali (admin_id) foydalanuvchi identification jo'nating.")
                else:
                    cursor_admins.execute("INSERT INTO admins (user_id, admin_id) VALUES (?, ?)", (user_id, admin_id))
                    conn_admins.commit()
                    await message.reply("<b><em>✅ Admin muvoffaqiyatni qo'shildi.</em></b>")
        else:
            await message.reply(f"❌ <em>{ userName }</em> Siz Admin Emassiz ❗️")

    # Main
    access_granted = True

    @bot.callback_query_handler(lambda callback_query: callback_query.data == 'message_admin')
    async def addDatas(callback_data: types.CallbackQuery):
        await callback_data.message.answer("<b><em>\"✍️ Bot foydalanuvchilarga xabar yuborish\" - Tez kunlarda ishga tushadi...</em></b>")

    @bot.callback_query_handler(lambda callback_query: callback_query.data == 'read_add_mess')
    async def readMes(callback_data: types.CallbackQuery):
        await callback_data.message.answer("<b><em>\"💬 Foydalanuvchilardan kelgan Xabarlarni o'qish\" - Tez kunlarda ishga tushadi...</em></b>")


    async def is_user_admin(admin_id):
        try:
            cursor_admins.execute("SELECT admin_id FROM admins WHERE admin_id = ?", (admin_id,))
            result = cursor_admins.fetchone()
            return result is not None
        except sqlite3.Error as e:
            print(f"Error checking admin status: {e}")
            return False

    @bot.message_handler(commands=['moder'])
    async def modAdmin(message: types.Message):
        admin_id = message.from_user.id
        userName = str(message.chat.first_name)
        
        try:
            if await is_user_admin(admin_id):
                if await is_user_admin(admin_id):
                    admin_options = [
                        [
                            types.InlineKeyboardButton(text="📊 Bot Statitikasi", callback_data="chart"),
                        ],
                        [
                            types.InlineKeyboardButton(text="✍️ Bot foydalanuvchilarga xabar yuborish", callback_data="message_admin"),
                        ],
                        [   
                            types.InlineKeyboardButton(text="💬 Foydalanuvchilardan kelgan Xabarlarni o'qish", callback_data="read_add_mess"),
                        ],
                    ]

                    keyboards = types.InlineKeyboardMarkup(inline_keyboard=admin_options)

                    await message.answer(
                        text=f"<b><em>🤖 YourBotName</em> ni Xodimlar boshqaruv paneli (v2.1) \n\n✋ <em>{userName}, Admin</em> Xush kelibsiz. \n\nMenuni tanlang:</b>",
                        reply_markup=keyboards
                    )
                else:
                    await message.reply(f"❌ <em>{userName}</em> Siz Admin Emassiz ❗️")
            else:
                await message.reply(f"❌ <em>{userName}</em> Siz Admin Emassiz ❗️")
        except Exception as e:
            print(f"Error handling /moder command: {e}")

    

    @bot.message_handler(lambda message: message.text in ["⚙️ Sozlamalar (set)", "⚙️ Настройки (set)"])
    async def setMenu(message: types.Message):
        userData = message.from_user.first_name
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        setChangeLanBut = InlineKeyboardButton("🔄 Tilni o'zgartirish / Изменение языка")
        homeExit = InlineKeyboardButton(text="🔙 Asosiy menu")
        inline_keyboard = InlineKeyboardMarkup().add(setChangeLanBut, homeExit)
        keyboards = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(setChangeLanBut, homeExit)

        homeExitRu = InlineKeyboardButton(text="🔙 Главное меню")
        inline_keyboard_ru = InlineKeyboardMarkup().add(setChangeLanBut, homeExitRu)
        keyboards_ru = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(setChangeLanBut, homeExitRu)

        if user.selected_language == "uz":
            await message.answer(
                f"<b>⚙️ <em>{ userData }, `Settings`</em> orqali shaxsiy sozlamalaringizni o'zgartirishingiz mumkun !</b>", reply_markup=keyboards
            )
        elif user.selected_language == "ru":
            await message.answer(
                f"<b>⚙️ <em>{ userData }, `Настройки`</em> Вы можете изменить свои личные настройки через !</b>", reply_markup=keyboards_ru
            )

    
    @bot.message_handler(lambda message: message.text in ["🔙 Asosiy menu", "🔙 Главное меню"])
    async def exitHome(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        if user.selected_language == "uz":
            await message.answer(
                text="<b>🏠 Asosiy menu.</b>",
                reply_markup=keyboards
            )
        elif user.selected_language == "ru":
            await message.answer(
                text="<b>🏠 Главное меню.</b>",
                reply_markup=keyboards_ru
            )

    @bot.message_handler(lambda message: message.text in ["☎️ Bog'lanish", "☎️ Связь"])
    async def connectCall(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        cPost = str(
            f"<b>📲 { botName }</b> - Xodimlar bilan bog'lanish. \n\n👤 <em><b>Murojaat uchun: @Mirzakhidov1ch</b></em> \n\n\n <b>💎 @hi_Germany - eng yaxshilarini sizga ulashamiz.</b>"
        )
        cPostRu = str(f"<b>📲 { botName }</b> Связаться с персоналом. \n\n👤 <em><b>Для апелляции: @Mirzakhidov1ch</b></em> \n\n\n <b>💎 @hi_Germany - Мы свяжем с вами лучшее.</b>")
        
        if user.selected_language == "uz":
            await message.answer_photo(
                callCenter,
                cPost
            )
        elif user.selected_language == "ru":
            await message.answer_photo(
                callCenter,
                cPostRu
            )
    @bot.message_handler(commands=['help'])
    async def connectCall(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        cPost = str(
            f"<b>📲 { botName }</b> - Xodimlar bilan bog'lanish. \n\n👤 <em><b>Murojaat uchun: @Mirzakhidov1ch</b></em> \n\n\n <b>💎 @hi_Germany - eng yaxshilarini sizga ulashamiz.</b>"
        )
        cPostRu = str(f"<b>📲 { botName }</b> Связаться с персоналом. \n\n👤 <em><b>Для апелляции: @Mirzakhidov1ch</b></em> \n\n\n <b>💎 @hi_Germany - Мы свяжем с вами лучшее.")
        
        if user.selected_language == "uz":
            await message.answer_photo(
                callCenter,
                cPost
            )
        elif user.selected_language == "ru":
            await message.answer_photo(
                callCenter,
                cPostRu
            )

    @bot.message_handler(lambda message: message.text in ["📜 Biz haqimizda", "📜 О нас"])
    async def aboutG(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        about = f"<b>{ botName } - <em>Biz sizga 🇩🇪 GERMANIYADA #Talim, #Sayohat va Boshqa maqsadlarda Maslahat va Yordam beramiz. \n\n👤 Murojaat uchun: @Mirzakhidov1ch \n\n\n 💎 @hi_Germany - eng yaxshilarini sizga ulashamiz.</em></b>"
        about_ru = f"<b>{ botName } - <em>Biz sizga 🇩🇪 Мы предоставим вам консультацию и помощь в #Обучении, #Поездках и других целях в Германии. \n\n👤 Для апелляции: @Mirzakhidov1ch \n\n\n 💎 @hi_Germany - Мы свяжем с вами лучшее.</em></b>" 

        if user.selected_language == "uz":
            await message.answer_photo(
                aboutAP,
                about
            )
        elif user.selected_language == "ru":
            await message.answer_photo(
                aboutAP,
                about_ru
            )
    @bot.message_handler(commands=['about'])
    async def aboutG(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        about = f"<b>{ botName } - <em>Biz sizga 🇩🇪 GERMANIYADA #Talim, #Sayohat va Boshqa maqsadlarda Maslahat va Yordam beramiz. \n\n👤 Murojaat uchun: @Mirzakhidov1ch \n\n\n 💎 @hi_Germany - eng yaxshilarini sizga ulashamiz.</em></b>"
        about_ru = f"<b>{ botName } - <em>Biz sizga 🇩🇪 Мы предоставим вам консультацию и помощь в #Обучении, #Поездках и других целях в Германии. \n\n👤 Для апелляции: @Mirzakhidov1ch \n\n\n 💎 @hi_Germany - Мы свяжем с вами лучшее.</em></b>" 

        if user.selected_language == "uz":
            await message.answer_photo(
                aboutAP,
                about
            )
        elif user.selected_language == "ru":
            await message.answer_photo(
                aboutAP,
                about_ru
            )



    @bot.message_handler(lambda message: message.text in ["🇺🇿 Nemis tilini 0 dan | Uzbek tilida o'rganish", "🇺🇿 Немецкий от 0 | Учеба на узбекском языке"])
    async def on_nu_start(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, one_time_keyboard=True)
        buttons = [button for button in course_nu_data]
        keyboard.add(*buttons)

        if user.selected_language == "uz":
            homeOld = InlineKeyboardButton(text="🔙 Orqaga qaytish", callback_data="back_old")
            homeExit = InlineKeyboardButton(text="🔙 Asosiy menu",)
            keyboard.add(homeOld, homeExit)
        elif user.selected_language == "ru":
            homeOld = InlineKeyboardButton(text="🔙 Отвали")
            homeExit = InlineKeyboardButton(text="🔙 Главное меню")
            keyboard.add(homeOld, homeExit)

        await message.answer("Select", reply_markup=keyboard)

    @bot.message_handler(lambda message: message.text in course_nu_data)
    async def on_button_nu_click(message: types.Message):
        button_name = message.text
        button_info = course_nu_data[button_name]
        title = button_info["title"]
        address = button_info["address"]
        await message.answer(f"<b><em>{ title }</em></b>")
        await message.answer(f"<b><em>{ address }</em></b>")




    # German Languages


    @bot.message_handler(lambda message: message.text in ["🇩🇪 Nemis tilini 0 dan | Nemis tilida o'rganish", "🇩🇪 Немецкий от 0 | Обучение на немецком языке"])
    async def on_nn__start(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, one_time_keyboard=True)
        buttons = [button for button in course_nn_data]
        keyboard.add(*buttons)

        if user.selected_language == "uz":
            homeOld = InlineKeyboardButton(text="🔙 Orqaga qaytish", callback_data="back_old")
            homeExit = InlineKeyboardButton(text="🔙 Asosiy menu",)
            keyboard.add(homeOld, homeExit)
        elif user.selected_language == "ru":
            homeOld = InlineKeyboardButton(text="🔙 Отвали")
            homeExit = InlineKeyboardButton(text="🔙 Главное меню")
            keyboard.add(homeOld, homeExit)

        await message.answer("Select", reply_markup=keyboard)

    @bot.message_handler(lambda message: message.text in course_nn_data)
    async def on_button_nn_click(message: types.Message):
        button_name = message.text
        button_info = course_nn_data[button_name]
        title = button_info["title"]
        address = button_info["address"]
        await message.answer(f"<b><em>{ title }</em></b>")
        await message.answer(f"<b><em>{ address }</em></b>")



    # "Ibrat Farzandlari" cources


    @bot.message_handler(lambda message: message.text in ["🈹 Ibrat Farzandlari", "🈹 Ибрат Фарзандлари"])
    async def on_ib__start(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, one_time_keyboard=True)
        buttons = [button for button in course_ib_data]
        keyboard.add(*buttons)

        if user.selected_language == "uz":
            homeOld = InlineKeyboardButton(text="🔙 Orqaga qaytish", callback_data="back_old")
            homeExit = InlineKeyboardButton(text="🔙 Asosiy menu",)
            keyboard.add(homeOld, homeExit)
        elif user.selected_language == "ru":
            homeOld = InlineKeyboardButton(text="🔙 Отвали")
            homeExit = InlineKeyboardButton(text="🔙 Главное меню")
            keyboard.add(homeOld, homeExit)

        await message.answer("Select", reply_markup=keyboard)

    @bot.message_handler(lambda message: message.text in course_ib_data)
    async def on_button_ib_click(message: types.Message):
        button_name = message.text
        button_info = course_ib_data[button_name]
        title = button_info["title"]
        address = button_info["address"]
        await message.answer(f"<b><em>{ title }</em></b>")
        await message.answer(f"<b><em>{ address }</em></b>")



    @bot.message_handler(lambda message: message.text in ["🔙 Orqaga qaytish", "🔙 Отвали"])
    async def exitHome(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        cource1 = InlineKeyboardButton(text="🇺🇿 Nemis tilini 0 dan | Uzbek tilida o'rganish")
        cource2 = InlineKeyboardButton(text="🇩🇪 Nemis tilini 0 dan | Nemis tilida o'rganish")
        cource3 = InlineKeyboardButton(text="🈹 Ibrat Farzandlari")
        cource4 = InlineKeyboardButton(text="🏫 Darsliklar (Maktab darsliklari)")
        homeExit = InlineKeyboardButton(text="🔙 Asosiy menu")
        course_buttons = InlineKeyboardMarkup().add(cource1, cource2, cource3, cource4, homeExit)

        keyboards = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(cource1,
                                    cource2, cource3, cource4, homeExit)
        
        cource1_ru = InlineKeyboardButton(text="🇺🇿 Немецкий от 0 | Учеба на узбекском языке")
        cource2_ru = InlineKeyboardButton(text="🇩🇪 Немецкий от 0 | Обучение на немецком языке")
        cource3_ru = InlineKeyboardButton(text="🈹 Ибрат Фарзандлари")
        cource4_ru = InlineKeyboardButton(text="🏫 Учебники (Школьные учебники)")
        homeExit = InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_home")
        course_buttons_ru = InlineKeyboardMarkup().add(cource1_ru, cource2_ru, cource3_ru, cource4_ru,
                                                    homeExit)

        keyboards_ru = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(cource1_ru,
                                    cource2_ru, cource3_ru, cource4_ru, homeExit)

        if user.selected_language == "uz":
            await message.answer(
                text="<b>📚 Kurslar (new)</b>",
                reply_markup=keyboards
            )
        elif user.selected_language == "ru":
            await message.answer(
                text="<b>📚 Курсы (новые)</b>",
                reply_markup=keyboards_ru
            )

        
    
    

    @bot.message_handler(lambda message: message.text in ["🏫 Darsliklar (Maktab darsliklari)", "🏫 Учебники (Школьные учебники)"])
    async def courceLes(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        coLess1 = InlineKeyboardButton(text="📔 1-sinf")
        coLess2 = InlineKeyboardButton(text="📓 2-sinf")
        coLess3 = InlineKeyboardButton(text="📕 3-sinf")
        coLess4 = InlineKeyboardButton(text="📘 4-5-sinflar")
        coLess5 = InlineKeyboardButton(text="📙 6-7-sinflar")
        coLess6 = InlineKeyboardButton(text="📒 8-9-sinflar")
        coLess7 = InlineKeyboardButton(text="📗 10-11-sinflar")
        backMenu = InlineKeyboardButton(text="🔙 Orqaga qaytish")
        homeExit = InlineKeyboardButton(text="🔙 Asosiy menu", callback_data="back_home")
        eyboard_inline = InlineKeyboardMarkup().add(coLess1, coLess2, coLess3, coLess4, coLess5, coLess6, coLess7)
        keyboards = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(coLess1,
                                coLess2, coLess3, coLess4, coLess5, coLess6, coLess7)
        keyboards.add(backMenu, homeExit)

        coLess1_ru = InlineKeyboardButton(text="📔 1-класс")
        coLess2_ru = InlineKeyboardButton(text="📓 2-класс")
        coLess3_ru = InlineKeyboardButton(text="📕 3-класс")
        coLess4_ru = InlineKeyboardButton(text="📘 4-5-классы")
        coLess5_ru = InlineKeyboardButton(text="📙 6-7-классы")
        coLess6_ru = InlineKeyboardButton(text="📒 8-9-классы")
        coLess7_ru = InlineKeyboardButton(text="📗 10-11-классы")
        backMenu_ru = InlineKeyboardButton(text="🔙 Отвали")
        homeExit_ru = InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_home")
        eyboard_inline_ru = InlineKeyboardMarkup().add(coLess1_ru, coLess2_ru, coLess3_ru, coLess4_ru, coLess5_ru, coLess6_ru, coLess7_ru)
        keyboards_ru = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(coLess1_ru,
                                coLess2_ru, coLess3_ru, coLess4_ru, coLess5_ru, coLess6_ru, coLess7_ru)
        keyboards_ru.add(backMenu_ru, homeExit_ru)

        if user.selected_language == "uz":
            await message.answer_photo(
                schoolCouses,
                f"<b><em>🏫 Darsliklar (Maktab darsliklari)</em> \n\n📚{ botName } - ning barcha Maktab darsliklari</b> \n\n🔠 Biror bir sinfni tanlang:",
                reply_markup=keyboards
            )
        elif user.selected_language == "ru":
            await message.answer_photo(
                schoolCouses,
                f"<b><em>🏫 Учебники (Школьные учебники)</em> \n\n📚{ botName } - Все школьные учебники</b> \n\n🔠 Выбирайте любой класс:",
                reply_markup=keyboards_ru
            )


    
    @bot.message_handler(lambda message: message.text in ["📔 1-sinf", "📔 1-класс"])
    async def courceLes1(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        file_path1 = './BasicMediaFiles/lsOne/1-sinf Fabuli Schulerbuch.pdf'
        file_path2 = './BasicMediaFiles/lsOne/1-sinf Fabuli_Arbeitsbuch.pdf'
        file_path3 = './BasicMediaFiles/lsOne/Fabuli_LHB_pages 1-49.pdf'
        if user.selected_language == "uz":
            caption = '📂 Fayl jo\'natilmoqda... \n\n<em>Iltimos biroz kuting.</em>'
            caption_end = "✅ Barcha fayllar yuklandi."
        elif user.selected_language == "ru":
            caption = '📂 Отправка файла... \n\n<em>Пожалуйста, подождите несколько секунд.</em>'
            caption_end = "✅ Все файлы загружены."
        
        with open(file_path1, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path2, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path3, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file, caption=caption_end)
    
    @bot.message_handler(lambda message: message.text in ["📓 2-sinf", "📓 2-класс"])
    async def courceLes1(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        file_path1 = './BasicMediaFiles/lsTwo/2-sinf Wo ist Paula_Arbeitsbuch_1_bez titul.pdf'
        file_path2 = './BasicMediaFiles/lsTwo/2-sinf Wo ist Paula_Kursbuch_1__compressed.pdf'
        file_path3 = './BasicMediaFiles/lsTwo/Wo ist Paula_LHB_1_2.pdf'
        if user.selected_language == "uz":
            caption = '📂 Fayl jo\'natilmoqda... \n\n<em>Iltimos biroz kuting.</em>'
            caption_end = "✅ Barcha fayllar yuklandi."
        elif user.selected_language == "ru":
            caption = '📂 Отправка файла... \n\n<em>Пожалуйста, подождите несколько секунд.</em>'
            caption_end = "✅ Все файлы загружены."
            
        with open(file_path1, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path2, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path3, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file, caption="✅ Barcha fayllar yuklandi.")

    @bot.message_handler(lambda message: message.text in ["📕 3-sinf", "📕 3-класс"])
    async def courceLes1(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        file_path1 = './BasicMediaFiles/lsThree/3-sinf Wo ist Paula_2_Übungsbuch.pdf'
        if user.selected_language == "uz":
            caption = '📂 Fayl jo\'natilmoqda... \n\n<em>Iltimos biroz kuting.</em>'
            caption_end = "✅ Barcha fayllar yuklandi."
        elif user.selected_language == "ru":
            caption = '📂 Отправка файла... \n\n<em>Пожалуйста, подождите несколько секунд.</em>'
            caption_end = "✅ Все файлы загружены."

        with open(file_path1, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file, caption="✅ Barcha fayllar yuklandi.")

    @bot.message_handler(lambda message: message.text in ["📘 4-5-sinflar", "📘 4-5-классы"])
    async def courceLes1(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        file_path1 = './BasicMediaFiles/lsFour/4-5 - sinflar Deutschprofis_1_Arbeitsbuch.pdf'
        file_path2 = './BasicMediaFiles/lsFour/4-5 - sinflar Deutschprofis_1_Kursbuch.pdf'
        file_path3 = './BasicMediaFiles/lsFour/4-5 - sinflar Deutschprofis_1_Testheft.pdf'
        file_path4 = './BasicMediaFiles/lsFour/Die Deutschprofis A1 Lehrerhandbuch.pdf'
        if user.selected_language == "uz":
            caption = '📂 Fayl jo\'natilmoqda... \n\n<em>Iltimos biroz kuting.</em>'
            caption_end = "✅ Barcha fayllar yuklandi."
        elif user.selected_language == "ru":
            caption = '📂 Отправка файла... \n\n<em>Пожалуйста, подождите несколько секунд.</em>'
            caption_end = "✅ Все файлы загружены."

        with open(file_path1, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path2, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path3, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path4, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file, caption="✅ Barcha fayllar yuklandi.")

    @bot.message_handler(lambda message: message.text in ["📙 6-7-sinflar", "📙 6-7-классы"])
    async def courceLes1(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        file_path1 = './BasicMediaFiles/lsFive/6-7 - sinflar Die Deutschprofis A2 Kursbuch.pdf'
        file_path2 = './BasicMediaFiles/lsFive/6-7 - sinflar Die Deutschprofis A2 Übungsbuch.pdf'
        file_path3 = './BasicMediaFiles/lsFive/Die Deutschprofis A2 Lehrerhandbuch.pdf'
        if user.selected_language == "uz":
            caption = '📂 Fayl jo\'natilmoqda... \n\n<em>Iltimos biroz kuting.</em>'
            caption_end = "✅ Barcha fayllar yuklandi."
        elif user.selected_language == "ru":
            caption = '📂 Отправка файла... \n\n<em>Пожалуйста, подождите несколько секунд.</em>'
            caption_end = "✅ Все файлы загружены."

        with open(file_path1, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path2, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path3, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file, caption="✅ Barcha fayllar yuklandi.")

    @bot.message_handler(lambda message: message.text in ["📒 8-9-sinflar", "📒 8-9-классы"])
    async def courceLes1(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        file_path1 = './BasicMediaFiles/lsSix/8-9 - sinflar Die Deutschprofis B1 Kursbuch.pdf'
        file_path2 = './BasicMediaFiles/lsSix/8-9 - sinflar Die Deutschprofis B1 Übungsbuch.pdf'
        file_path3 = './BasicMediaFiles/lsSix/Die Deutschprofis B1 Lehrerhandbuch.pdf'
        if user.selected_language == "uz":
            caption = '📂 Fayl jo\'natilmoqda... \n\n<em>Iltimos biroz kuting.</em>'
            caption_end = "✅ Barcha fayllar yuklandi."
        elif user.selected_language == "ru":
            caption = '📂 Отправка файла... \n\n<em>Пожалуйста, подождите несколько секунд.</em>'
            caption_end = "✅ Все файлы загружены."

        with open(file_path1, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path2, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path3, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file, caption="✅ Barcha fayllar yuklandi.")

    @bot.message_handler(lambda message: message.text in ["📗 10-11-sinflar", "📗 10-11-классы"])
    async def courceLes1(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        file_path1 = './BasicMediaFiles/lsSeven/10-11 - sinflar Aspekte Junior B1+ Kursbuch.pdf'
        file_path2 = './BasicMediaFiles/lsSeven/10-11 - sinflar Aspekte Junior B1+ Übungsbuch.pdf'
        file_path3 = './BasicMediaFiles/lsSeven/sol3e_preint_cumulative_test_units_1-9_b.pdf'
        file_path4 = './BasicMediaFiles/lsSeven/sol3e_preint_cumulative_test_units_6-9_a.pdf'
        file_path5 = './BasicMediaFiles/lsSeven/sol3e_preint_cumulative_test_units_6-9_b.pdf'
        if user.selected_language == "uz":
            caption = '📂 Fayl jo\'natilmoqda... \n\n<em>Iltimos biroz kuting.</em>'
            caption_end = "✅ Barcha fayllar yuklandi."
        elif user.selected_language == "ru":
            caption = '📂 Отправка файла... \n\n<em>Пожалуйста, подождите несколько секунд.</em>'
            caption_end = "✅ Все файлы загружены."

        with open(file_path1, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path2, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path3, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path4, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file)
        with open(file_path5, 'rb') as file:
            msg = await message.answer(caption)
            await bot.bot.send_document(message.chat.id, file, caption="✅ Barcha fayllar yuklandi.")

        




    
    @bot.message_handler(lambda message: message.text in ["💎 Foydali Ma'lumotlar (new)", "💎 Полезная информация (new)"])
    async def usefullData(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        useP1 = InlineKeyboardButton(text="🇩🇪 Germaniya davlati, sharoitlari va boshqalar...")
        useP2 = InlineKeyboardButton(text="🇩🇪 Germaniya ta'limi, testlari va va boshqalar...")
        homeExit = InlineKeyboardButton(text="🔙 Asosiy menu", callback_data="back_home")
        eyboard_inline = InlineKeyboardMarkup().add(useP1, useP2, homeExit)
        keyboards = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(useP1,
                                            useP2, homeExit)
        
        useP1_ru = InlineKeyboardButton(text="🇩🇪 Немецкое государство, условия и так далее...")
        useP2_ru = InlineKeyboardButton(text="🇩🇪 Немецкое образование, тесты и т.д...")
        homeExit_ru = InlineKeyboardButton(text="🔙 Главное меню")
        eyboard_inline_ru = InlineKeyboardMarkup().add(useP1_ru, useP2_ru, homeExit_ru)
        keyboards_ru = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(useP1_ru,
                                            useP2_ru, homeExit_ru)
        
        if user.selected_language == "uz":
            await message.answer_photo(
                usefullDatas,
                "<b>💎 Foydali Ma'lumotlar</b> \n\n<b><em>🇩🇪 Germaniya:</em>\n#Haqida\n#Talimi\n#Tibbiyoti\n#Ishlari\nva boshqa ko'plab <em>#Foydali va #Qiziqarli</em> ma'lumotlar.</b> \n\n🔠 Biron bir menuni tanlang:",
                reply_markup=keyboards
            )
        elif user.selected_language == "ru":
            await message.answer_photo(
                usefullDatas,
                "<b>💎 Полезная информация</b> \n\n<b><em>🇩🇪 Германия:</em>\n#Около\n#Образование\n#Лекарство\n#Завод\nи многие другие <em>#Полезный va #Интересный</em> данные.</b> \n\n🔠 Выберите любое меню:",
                reply_markup=keyboards_ru
            )



    @bot.message_handler(lambda message: message.text in ["🇩🇪 Germaniya davlati, sharoitlari va boshqalar...", "🇩🇪 Немецкое государство, условия и так далее..."])
    async def usefullData1(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        usefull_data = [
                [
                    types.InlineKeyboardButton(text="📍GERMANIYAGA BORISH TALABLARI", callback_data="uDn1"),
                    types.InlineKeyboardButton(text="✅ AUPAIR HAQIDA TO'LIQ", callback_data="uDn2"),
                ],
                [
                    types.InlineKeyboardButton(text="✅ AUSBILDUNG HAQIDA MA'LUMOT", callback_data="uDn5"),
                    types.InlineKeyboardButton(text="📞 ELCHIXONA EMAILLARI TEL NOMERLARI", callback_data="uDn6"),
                ],
                [
                    types.InlineKeyboardButton(text="🎧 BARCHA SOHADA OVOZLI CHAT", callback_data="uDn7"),
                    types.InlineKeyboardButton(text="✅ FSJ HAQIDA MA'LUMOT: FSJ BFD", callback_data="uDn8"),
                ],
                [
                    types.InlineKeyboardButton(text="🟦 BLAU KARTA (moviy karta) Blaue_karte", callback_data="uDn9"),
                    types.InlineKeyboardButton(text="👨‍💻 FERIENJOB (Work_and_Travel_in_De)", callback_data="uDn10"),
                ],
                [
                    types.InlineKeyboardButton(text="🏦 BANKSHOT Bloklangan_hisob_raqam", callback_data="uDn11"),
                    types.InlineKeyboardButton(text="🏘 STUDIENKOLLEG # Studienkolleg", callback_data="uDn12"),
                ],
                [
                    types.InlineKeyboardButton(text="🎫 CHIPTA SOTIB OLISH", callback_data="uDn13"),
                    types.InlineKeyboardButton(text="✅ STIPENDIYA XOHLOVCHILAR UCHUN", callback_data="uDn14"),
                ],
                [
                    types.InlineKeyboardButton(text="♾ GERMANIYADA BEPUL BAKALAVR VA MAGISTRATURA ÒQISH SHARTLARI", callback_data="uDn15"),
                    types.InlineKeyboardButton(text="✅ GERMANIYADA AUSBILDUNG QILISH", callback_data="uDn16"),
                ],
                [
                    types.InlineKeyboardButton(text="🇺🇿 GERMANIYADA TAN OLINGAN UZB UNIVERSITUTLARI", callback_data="uDn17"),
                    types.InlineKeyboardButton(text="💉 GERMANIYADA TIBBIYOT SOHASIDA ÒQISH VA UZB DAN GERMANIYAGA ÒQISHINI KÒCHIRISH", callback_data="uDn18"),
                ],
                [
                    types.InlineKeyboardButton(text="🔎 GERMANIYADA IJARAGA UY IZLASH", callback_data="uDn19"),
                    types.InlineKeyboardButton(text="🧑‍🎓 GERMANIYADA BACHELOR YOKI MASTER ÒQIMOQCHI BÒLGANLARGA", callback_data="uDn20"),
                ],
            ]

        keyboards = types.InlineKeyboardMarkup(inline_keyboard=usefull_data)

        if user.selected_language == "uz":
            await message.answer(
                text="<b><em>💎 Germaniya #borish, #elchixona, #xonadonar, #ishlar va boshqa ko'plab narsalar haqida Qiziqarli va Foydali ma'lumotlar.</em></b>",
                reply_markup=keyboards
            )
        elif user.selected_language == "ru":
            await message.answer(text="🇷🇺 Пока информация не полностью переведена на русский язык. Информация будет переведена в ближайшее время.")
            await message.answer(
                text="<b><em>💎 Интересная и полезная информация о Германии #путешествия, #посольство, #ведение домашнего хозяйства, #работа и многое другое.</em></b>",
                reply_markup=keyboards
            )


    @bot.callback_query_handler(lambda c: c.data in usefull_data1)
    async def handle_useful_data(callback_query: types.CallbackQuery):
        selected_data = callback_query.data
        if selected_data in usefull_data1:
            response = usefull_data1[selected_data]
            await callback_query.message.answer(f"<b>{ response }</b>")
        else:
            await callback_query.message.answer("Bunday ma'lumot topilmadi.")



    @bot.message_handler(lambda message: message.text in ["🇩🇪 Germaniya ta'limi, testlari va va boshqalar...", "🇩🇪 Немецкое образование, тесты и т.д..."])
    async def usefullData2(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        usefull_data = [
                [
                    types.InlineKeyboardButton(text="🏡 GERMANIYA UNIVERSITETLARI RÒYXATI:", callback_data="uDn21"),
                    types.InlineKeyboardButton(text="🗂 TESTDAF HAQIDA MA'LUMOT", callback_data="uDn22"),
                ],
                [
                    types.InlineKeyboardButton(text="📖 ANTRAG NAMUNA", callback_data="uDn23"),
                    types.InlineKeyboardButton(text="❗️ GERMANIYA ORZUSIDA ALDANGANLAR: (OGOH BO'LING)", callback_data="uDn24"),
                ], 
                [
                    types.InlineKeyboardButton(text="❓ UZB PRAVASINI GERMANIYADA FOYDALANSA BÒLADIMI", callback_data="uDn25"),
                    types.InlineKeyboardButton(text="✅ WEITERBILDUNG", callback_data="uDn26"),
                ],
                [
                    types.InlineKeyboardButton(text="🦷 UZB DA STAMATOLOGIYADA O'QIB GERMANIYADA STAMATOLOG BO'LIB ISHLASH", callback_data="uDn27"),
                    types.InlineKeyboardButton(text="🇩🇪 SPRACHKURS (Til kursi)", callback_data="uDn4"),
                ],
                [
                    types.InlineKeyboardButton(text="💊 GERMANIYADA DAVOLANISH UCHUN NIMALAR QILISH KERAK", callback_data="uDn30"),
                    types.InlineKeyboardButton(text="✅ GERMANIYADA TIBBIY TA'LIM:", callback_data="uDn34"),
                ],
                [
                    types.InlineKeyboardButton(text="✅ GERMANIYADA OLIY TA'LIM OLISH: maktab, kollej, litseyni tamomlab Ger da òqish. Studienkolleg", callback_data="uDn31"),
                    types.InlineKeyboardButton(text="🏫 GERMANIYADA BAKALAVRDA O'QISH UCHUN TO'LIQ MA'LUMOT", callback_data="uDn32"),

                ],
                [
                    types.InlineKeyboardButton(text="✅ GERMANIYAGA QARINDOSHLARINI MEHMONGA CHAQIRISH:", callback_data="uDn35"),
                    types.InlineKeyboardButton(text="✅ O'zbekistonda tibbiyot sohasida bakalavrni bitirib, Germaniyada ishlash va mutaxassislikka (LOR, Kardiolog, Kardioxirurg va hkz) erishish haqidagi", callback_data="uDn36"),
                ],
                [
                    types.InlineKeyboardButton(text="✅ O'zbekistonda MEDKOLLEJ ni bitirib Germaniyada ishlash haqida", callback_data="uDn37"),
                    types.InlineKeyboardButton(text="✅ DAAD PORTALI ORQALI TURLI STIPENDIYALARGA HUJJAT TOPSHIRISH:", callback_data="uDn40"),
                ],
                [
                    types.InlineKeyboardButton(text="🇺🇿 UZB DAGI O'QISHINI GERMANIYAGA KO'CHIRISH. (PEREVOD) ", callback_data="uDn38"),
                    types.InlineKeyboardButton(text="🇩🇪 GERMANIYA FUQOROLIGINI OLISH:", callback_data="uDn39"),
                ],
        ]


        keyboards = types.InlineKeyboardMarkup(inline_keyboard=usefull_data)
        if user.selected_language == "uz":
            await message.answer(
                text="<b><em>💎 Germaniya #talim, #universitetlar, #testlaer, #xonadonar, #tibbiyot va boshqa ko'plab narsalar haqida Qiziqarli va Foydali ma'lumotlar.</em></b>",
                reply_markup=keyboards
            )
        elif user.selected_language == "ru":
            await message.answer(text="🇷🇺 Пока информация не полностью переведена на русский язык. Информация будет переведена в ближайшее время.")
            await message.answer(
                text="<b><em>💎 Интересная и полезная информация о Германии #образование, #университеты, #testlaer, #домоводство, #медицина и многое другое.</em></b>",
                reply_markup=keyboards
            )

    @bot.callback_query_handler(lambda c: c.data in usefull_data2)
    async def handle_useful_data(callback_query: types.CallbackQuery):
        selected_data = callback_query.data
        if selected_data in usefull_data2:
            response = usefull_data2[selected_data]
            await callback_query.message.answer(f"<b>{ response }</b>")
        else:
            await callback_query.message.answer("Bunday ma'lumot topilmadi.")





    @bot.message_handler()
    async def kb_answer(message: types.Message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()

        # Cources List
        cources_message = str(f"<em><b>🔎 { botName } - Kurslarimiz bilan tanishishingiz mumkin.</b></em>")

        cource1 = InlineKeyboardButton(text="🇺🇿 Nemis tilini 0 dan | Uzbek tilida o'rganish", callback_data="cource1")
        cource2 = InlineKeyboardButton(text="🇩🇪 Nemis tilini 0 dan | Nemis tilida o'rganish", callback_data="cource2")
        cource3 = InlineKeyboardButton(text="🈹 Ibrat Farzandlari", callback_data="cource3")
        cource4 = InlineKeyboardButton(text="🏫 Darsliklar (Maktab darsliklari)", callback_data="cource4")
        homeExit = InlineKeyboardButton(text="🔙 Asosiy menu", callback_data="back_home")
        course_buttons = InlineKeyboardMarkup().add(cource1, cource2, cource3, cource4, homeExit)

        keyboards = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(cource1,
                                    cource2, cource3, cource4, homeExit)
        

        cources_message_ru = str(f"<em><b>🔎 { botName } - Вы можете ознакомиться с нашими курсами.</b></em>")

        cource1_ru = InlineKeyboardButton(text="🇺🇿 Немецкий от 0 | Учеба на узбекском языке", callback_data="cource1")
        cource2_ru = InlineKeyboardButton(text="🇩🇪 Немецкий от 0 | Обучение на немецком языке", callback_data="cource2")
        cource3_ru = InlineKeyboardButton(text="🈹 Ибрат Фарзандлари", callback_data="cource3")
        cource4_ru = InlineKeyboardButton(text="🏫 Учебники (Школьные учебники)")
        homeExit = InlineKeyboardButton(text="🔙 Главное меню")
        course_buttons_ru = InlineKeyboardMarkup().add(cource1_ru, cource2_ru, cource3_ru, cource4_ru,
                                                    homeExit)

        keyboards_ru = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(cource1_ru,
                                    cource2_ru, cource3_ru, cource4_ru, homeExit)
        
        # Connect

        # Users Data

        # user_id = message.from_user.id
        # username = message.from_user.username
        # firstname = message.from_user.first_name

        # cursor.execute('INSERT OR REPLACE INTO users (user_id, username, firstname) VALUES (?, ?, ?)', (user_id, username, firstname))
        # conn.commit()

        if message.text == '📚 Kurslar (new)':
            if user.selected_language == "uz":
                await message.reply(
                    cources_message,
                    reply_markup=keyboards
                )
        elif message.text == '📚 Курсы (новые)':
            if user.selected_language == "ru":
                await message.reply(
                    cources_message_ru,
                    reply_markup=keyboards_ru
                )
        
        else:
            await message.reply(f"❌ { message.chat.first_name }, Mavjud bo'lmaan buyruq kiritdingiz \"{ message.text }\" \nBosha so`z yozing...")


        
    

    # ALl errors
    # All posible errors will pass through here

    @bot.errors_handler(exception = ['BotBlocked', 'TimeoutError', 'TypeError'])
    async def bot_block(update: types.Update, excention: Exception):
        print(f"I think The Bot was blocked by the User { update } { excention }")
        return True

except:
    executor.start_polling(dispatcher=bot, skip_updates=True)



if __name__ == '__main__':
    executor.start_polling(dispatcher=bot, skip_updates=True)