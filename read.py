import os
from PIL import Image
import json

folder_path = "processed_image"

for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        image_path = os.path.join(folder_path, filename)
        try:
            img = Image.open(image_path)
            metadata = img.text
            json_str = metadata.get("json_metadata", None)

            if json_str:
                json_data = json.loads(json_str)
                print(f"提取的 JSON 数据 ({filename})：", json_data)
            else:
                print(f"未找到嵌入的 JSON 数据 ({filename})。")
        except Exception as e:
            print(f"处理文件 {filename} 时出错：{e}")
