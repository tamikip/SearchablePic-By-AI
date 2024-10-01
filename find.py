from sentence_transformers import SentenceTransformer, util
import os
import json
from PIL import Image

# 使用更好的句子相似度模型
model = SentenceTransformer(r"C:\Users\TamikiP\PycharmProjects\AI_PIC\aaa")


def get_png_files(folder_path):
    """
    获取文件夹中的所有 PNG 文件。
    """
    png_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".png"):
                png_files.append(os.path.join(root, file))
    return png_files


def read_metadata_from_image(image_path):
    """
    从 PNG 图片中读取嵌入的 JSON 元数据。
    """
    try:
        img = Image.open(image_path)
        metadata = img.info.get("json_metadata")
        if metadata:
            return json.loads(metadata)
        else:
            return None
    except Exception as e:
        print(f"读取图片 {image_path} 的元数据时出错: {e}")
        return None


def calculate_similarity(query, description):
    """
    使用 sentence-transformers 计算查询和描述之间的相似度。
    """
    query_embedding = model.encode(query, convert_to_tensor=True)
    description_embedding = model.encode(description, convert_to_tensor=True)

    # 计算余弦相似度
    similarity = util.pytorch_cos_sim(query_embedding, description_embedding)
    return similarity.item()


def find_images_by_query(folder_path, query, if_camera):
    """
    根据自然语言查询查找符合条件的图片。
    """
    png_files = get_png_files(folder_path)
    image_similarities = []

    # 计算每张图片的相似度
    for image_path in png_files:
        metadata = read_metadata_from_image(image_path)
        if metadata:
            description = metadata.get("description", "")
            if if_camera == metadata.get("type", ""):
                similarity_score = calculate_similarity(query, description)
                if similarity_score >= 0.35:
                    image_similarities.append((image_path, similarity_score))

    # 如果没有符合条件的图片，直接返回
    if not image_similarities:
        return []

    # 按相似度从高到低排序
    image_similarities.sort(key=lambda x: x[1], reverse=True)

    # 找到相似度最高的图片
    best_similarity = image_similarities[0][1]

    if best_similarity <= 0.3:
        return []

    # 找到相似度差异小于0.04的图片
    matching_images = []
    for image_path, similarity in image_similarities:
        if best_similarity - similarity < 0.04:
            matching_images.append(os.path.basename(image_path))

    return matching_images


def main():
    folder_path = "new"
    query = input("请输入查询条件: ")
    if_camera = input("图片是否是由相机拍摄？ ")
    if_camera = "camera" if if_camera == "是" else "others"

    matching_images = find_images_by_query(folder_path, query,if_camera)

    if matching_images:
        print("找到符合条件的图片:")
        for image in matching_images:
            print(image)
    else:
        print("没有找到符合条件的图片。")


if __name__ == "__main__":
    main()
