import face_recognition
import sqlite3
import numpy as np

conn= sqlite3.connect('face_database.db')
cursor=conn.cursor()
def clean_db():
    conn.execute('''DROP TABLE faces''')




def save_face_to_db(name, face_image_path, province):

    # 读取人脸图片
    image = face_recognition.load_image_file(face_image_path)

    # 获取人脸编码
    face_encoding = face_recognition.face_encodings(image)[0]

    # 确保转换为 float32
    face_encoding = face_encoding.astype(np.float32)

    # 将人脸编码转换为字节数据
    face_encoding_bytes = face_encoding.tobytes()
    cursor.execute('''CREATE TABLE IF NOT EXISTS faces
                             (id INTEGER PRIMARY KEY, name TEXT, face_encoding BLOB, province TEXT)''')
    # 存入数据库
    cursor.execute('''INSERT INTO faces (name, face_encoding, province)
                      VALUES (?, ?, ?)''', (name, face_encoding_bytes, province))
def close_db():
    conn.commit()
    conn.close()


clean_db()
# 示例保存用户数据
save_face_to_db('liudehua', 'ldh.jpg', 'hongkong')
save_face_to_db('zhangchunhua', 'zch.jpg', 'henan')
save_face_to_db('gonghanyun', 'ghy.jpg', 'sc')
close_db()
