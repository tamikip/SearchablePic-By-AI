import face_recognition
import os

# 加载第一张图片并提取人脸特征
known_image = face_recognition.load_image_file("known_person.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

image_folder = "path_to_images"
matching_images = []

for image_name in os.listdir(image_folder):
    image_path = os.path.join(image_folder, image_name)
    unknown_image = face_recognition.load_image_file(image_path)

    # 提取当前图片中的人脸特征
    unknown_encodings = face_recognition.face_encodings(unknown_image)

    # 如果图片中有多张人脸，逐个比较
    for unknown_encoding in unknown_encodings:
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        if results[0]:
            matching_images.append(image_name)
            break

print("匹配的图片:", matching_images)
