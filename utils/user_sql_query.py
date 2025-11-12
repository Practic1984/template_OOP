create_table_users = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  from_user_id INTEGER UNIQUE,
  from_user_username TEXT,
  from_user_first_name TEXT,
  regtime TEXT,
  about_time TEXT DEFAULT '-',
  faq_time TEXT DEFAULT '-'

);
"""

create_table_utm = """
CREATE TABLE IF NOT EXISTS utm (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  from_user_id INTEGER,
  from_user_username TEXT,
  from_user_first_name TEXT,
  regtime TEXT,
  utm_code TEXT
);
"""

save_user = """
INSERT INTO users (
  from_user_id,
  from_user_username,
  from_user_first_name,
  regtime
  )
VALUES (?,?,?,?)
"""

save_user_utm = """
INSERT INTO utm (
  from_user_id,
  from_user_username,
  from_user_first_name,
  regtime,
  utm_code
  )
VALUES (?,?,?,?,?)
"""

get_user_row = """
SELECT * FROM users 
WHERE from_user_id = ?
"""

find_user = """
SELECT from_user_id FROM users WHERE from_user_id = ?
"""