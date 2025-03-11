import cv2
import face_recognition
import numpy as np
import sqlite3  # 使用 SQLite 作为数据库示例

# 加载 Haar 级联人脸检测器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def load_face_database():
    conn = sqlite3.connect('face_database.db')  # 连接到数据库
    cursor = conn.cursor()

    # 确保数据库表存在
    cursor.execute('''CREATE TABLE IF NOT EXISTS faces
                      (id INTEGER PRIMARY KEY, name TEXT, face_encoding BLOB, province TEXT)''')

    cursor.execute('SELECT * FROM faces')
    rows = cursor.fetchall()

    print(f"数据库返回 {len(rows)} 行数据")  # 打印数据库查询到的行数

    face_database = []
    for row in rows:
        face_encoding = np.frombuffer(row[2], dtype=np.float32)  # 解析 BLOB 数据
        print(f"加载用户: {row[1]}, 人脸编码长度: {len(face_encoding)}")  # 打印每个用户信息
        face_database.append({'id': row[0], 'name': row[1], 'face_encoding': face_encoding, 'province': row[3]})

    conn.close()
    return face_database



# 提取面部特征
def extract_face_encoding(frame):
    # 转换为 RGB 格式（face_recognition 需要 RGB 格式）
    # rgb_frame = frame[:, :, ::-1]
    # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 检测人脸（使用 face_recognition 而不是 cv2.CascadeClassifier 提供的坐标）
    face_locations = face_recognition.face_locations(frame)
    if not face_locations:
        print("Warning: No face detected.")
        return [], []  # 避免 face_encodings() 传入空列表
    # 计算面部特征
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    return face_encodings, face_locations


def compare_faces(face_encoding, face_database):
    print(f"待匹配编码长度: {len(face_encoding)}, 类型: {face_encoding.dtype}")  # 128 维，检查类型
    print(f"数据库人数: {len(face_database)}")

    for user in face_database:
        print(f"匹配 {user['name']}，编码类型: {user['face_encoding'].dtype}")  # 检查类型
        # 确保数据类型一致
        user_encoding = user['face_encoding'].astype(np.float64)  # 转换类型以匹配 face_recognition
        matches = face_recognition.compare_faces([user_encoding], face_encoding)
        print(f"匹配结果: {matches}")  # 打印匹配结果
        if matches[0]:
            return user['name'], user['province']

    return None, None  # 未找到匹配



# 加载数据库中的人脸特征
face_database = load_face_database()

# 打开视频
cap = cv2.VideoCapture(0)  # 使用摄像头

if not cap.isOpened():
    print("Error: Cannot open video.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video.")
        break

    # 使用 face_recognition 直接检测人脸
    face_encodings, face_locations = extract_face_encoding(frame)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        name, province = compare_faces(face_encoding, face_database)

        top, right, bottom, left = face_location  # 这里 face_recognition 返回的是 (top, right, bottom, left)

        # 显示匹配信息
        label = f'Name: {name}, Province: {province}' if name else "Unknown"
        cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # 画出人脸框
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放视频对象并关闭窗口
cap.release()
cv2.destroyAllWindows()
