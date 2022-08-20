create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    username VARCHAR(32),
    tel_number VARCHAR(32),
    bio VARCHAR(70),
    language_code VARCHAR(32),
    count_exec_script INT,
    created_at VARCHAR(32),
    modified_at VARCHAR(32) )
"""
