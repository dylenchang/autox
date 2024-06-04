import io
import shutil
import sqlite3
import zipfile


def read_binary_file(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    return binary_data


def save_to_sqlite(db_path, table_name, binary_data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建表（如果不存在）
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY,
        data BLOB
    )
    ''')

    # 插入二进制数据
    cursor.execute(f'''
    INSERT INTO {table_name} (data)
    VALUES (?)
    ''', (binary_data,))

    conn.commit()
    conn.close()


# 示例用法
zip_file_path = r'E:\tmp\output.zip'
# binary_data = read_binary_file(zip_file_path)

# 示例用法
sqlite_db_path = './sqlite.db'
table_name = 'your_table'


# save_to_sqlite(sqlite_db_path, table_name, binary_data)

def read_and_decompress_from_sqlite(db_path, table_name, out_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 读取二进制数据
    cursor.execute(f'SELECT data FROM {table_name}')
    result = cursor.fetchone()

    if result:
        binary_data = result[0]

        file_like_object = io.BytesIO(binary_data)
        with zipfile.ZipFile(file_like_object, 'r') as zip_ref:
            zip_ref.extractall(out_path)

    conn.close()


read_and_decompress_from_sqlite(sqlite_db_path, table_name, r'E:\tmp\test2')
