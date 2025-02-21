# 📌 Шаблон тг бота

![GitHub Repo stars](https://img.shields.io/github/stars/Practic1984/template_OOP?style=social)
![GitHub forks](https://img.shields.io/github/forks/Practic1984/template_OOP?style=social)
![GitHub license](https://img.shields.io/github/license/Practic1984/template_OOP)

Шаблон проекта для создания синхронного телеграмм-бота. На базе данного шаблона удобно создавать коммерческих ботов. Включает в себя меню с разными разделами (О компании, Faq, Отзывы и т.д.). Панель админа включает в себя отчеты с временными метками и возможностью рассылки. 

## 📦 Установка

```bash
# Клонировать репозиторий
git clone https://github.com/Practic1984/template_OOP.git
cd template_OOP

# Установить зависимости
pip install -r requirements.txt, в зависимости от проекта
```

## 🚀 Использование

```bash
python3 bot.py
```

## 🛠 Технологии

- ✅ Основной стек: `Python`, `Sqlite3`

## 🏗 Структура проекта

```
📂 template_oop
 ┣ 📂 config
   ┣ 📜 config.py
 ┣ 📂 examples
   ┣ 📜 states.py
   ┣ 📜 textfilters.py
 ┣ 📂 handlers
   ┣ 📜 admin.py
   ┣ 📜 user.py
 ┣ 📂 keyboards
   ┣ 📜 keyboards_admin.py
   ┣ 📜 keyboards_user.py
 ┣ 📂 msg
   ┣ 📜 msg_user.py
   ┣ 📜 msg_admin.py
 ┣ 📂 utils
   ┣ 📜 admin_sql_query.py
   ┣ 📜 user_sql_query.py
   ┣ 📜 sqliteormmagic.py
   ┣ 📜 sql_fnc.py
   ┣ 📜 other.py
 ┣ 📜 bot.py
 ┣ 📜 bot_and_db.py
 ┣ 📜 README.md
```

## 🤝 Вклад

1. Форкните репозиторий
2. Создайте новую ветку (`git checkout -b feature-branch`)
3. Внесите изменения и закоммитьте (`git commit -m 'Добавлена новая фича'`)
4. Запушьте (`git push origin feature-branch`)
5. Откройте Pull Request

## 📬 Контакты

[![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Practic_old)  
