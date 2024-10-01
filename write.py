from PIL import Image, PngImagePlugin
import json
import os
from datetime import datetime
import requests
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from jpg_to_png import batch_convert_jpg_to_png


def get_png_files(folder_path):
    png_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".png"):
                png_files.append(os.path.join(root, file))
    return png_files


def extract_content_after_colon(text):
    if "：" or "：" in text and "标签" in text:
        colon_index = text.find("：")
        content_after_colon = text[colon_index + 1:].strip()
        return content_after_colon
    else:
        return text


def gpt_pic(img_path):
    with open(img_path, 'rb') as img_file:
        img_base = base64.b64encode(img_file.read()).decode('utf-8')
    key = "3a5661d2a3bafa406f4827e504eaee6d.6cEgSMwDVncZAhr8"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }
    base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    payload = json.dumps({
        "model": "GLM-4V-Plus",
        "messages": [
            {
                "role": "system",
                "content": "你是识图高手，可以帮我分析图片"
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "请你帮我给这张图片打标签（标签应该是一个或几个简短的句子），如果可以最好有时间，地点。结尾用["
                                             "]表示图片的类型，代表相机图片，2代表其他图片或网络图片，这是一个输出例子:女生拉着男生的手，晚上，街道上[1],"
                                             "只输出标签和中括号，不要输出多余的"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_base,
                        },
                    },
                ]
            }
        ]
    })

    response = requests.post(base_url, headers=headers, data=payload)
    parsed_data = json.loads(response.text)
    content = parsed_data['choices'][0]['message']['content']
    return extract_content_after_colon(content)


def Text_embedded_in_image(image_path, content):
    content, remaining = content.split('[')
    type_num = remaining.rstrip(']')
    image_type = "camera" if type_num == "1" else "others"

    img = Image.open(image_path)
    modification_time_stamp = os.path.getmtime(image_path)
    modification_date = datetime.fromtimestamp(modification_time_stamp).date()

    modification_date_str = modification_date.isoformat()

    json_data = {
        "description": content.strip(),
        "type": image_type,
        "date": modification_date_str,
        "person": "a"
    }

    json_str = json.dumps(json_data)
    meta = PngImagePlugin.PngInfo()
    meta.add_text("json_metadata", json_str)
    image_path = os.path.basename(image_path)
    if not os.path.exists("new"):
        os.makedirs("new")
    img.save(f"new/{image_path}", "png", pnginfo=meta)
    print(f"JSON 数据已嵌入到 {image_path} 的 PNG 元数据中。")


def process_image(image_path):
    try:
        content = gpt_pic(image_path)
        print(f"处理图片: {image_path}，标签: {content}")
        Text_embedded_in_image(image_path, content)
    except Exception as e:
        print(f"处理图片 {image_path} 时出错: {e}")


def main():
    png_list = get_png_files("before")
    batch_convert_jpg_to_png("before")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_image, img_path) for img_path in png_list]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"任务执行时出错: {e}")


if __name__ == "__main__":
    main()
