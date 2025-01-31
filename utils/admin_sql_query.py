create_table_admins = """
CREATE TABLE IF NOT EXISTS admins (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  from_user_id INTEGER UNIQUE,
  from_user_username TEXT,
  from_user_firstname TEXT,
  regtime TEXT
);
"""

save_admin = """
INSERT INTO admins (
  from_user_id,
  from_user_username,
  from_user_firstname,
  regtime
  )
VALUES (?,?,?,?)
"""
get_admin_row = """
SELECT * FROM admins 
WHERE from_user_id = ?
"""

get_table_rows = """
SELECT * FROM "{table}"
"""

get_all_users = """
SELECT from_user_id FROM users
"""