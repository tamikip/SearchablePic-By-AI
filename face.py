import face_recognition


def face_match(pic_path1, pic_path2):
    known_image = face_recognition.load_image_file(pic_path1)
    known_encodings = face_recognition.face_encodings(known_image)

    if len(known_encodings) == 0:
        return False

    known_encoding = known_encodings[0]

    unknown_image = face_recognition.load_image_file(pic_path2)
    unknown_encodings = face_recognition.face_encodings(unknown_image)

    if len(unknown_encodings) == 0:
        return False

    unknown_encoding = unknown_encodings[0]

    results = face_recognition.compare_faces([known_encoding], unknown_encoding)

    return results[0]

