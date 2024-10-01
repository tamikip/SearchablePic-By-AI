# 项目名称

图片处理与标签生成系统

## 项目简介

该项目旨在自动化处理图片，生成图片标签，并将标签嵌入到 PNG 图片的元数据中。项目还支持通过自然语言查询图片，并根据图片的描述和相似度进行检索。项目还包括 JPG 到 PNG 的批量转换功能，以及人脸识别功能。

## 功能

1. **图片标签生成**：使用 AI 模型（GLM-4V-Plus）为图片生成标签，并将标签嵌入到 PNG 图片的元数据中。
2. **图片元数据嵌入**：将生成的标签、图片类型（相机图片或其他图片）以及图片的修改日期嵌入到 PNG 图片的元数据中。
3. **自然语言图片检索**：根据用户输入的自然语言查询，使用句子相似度模型（SentenceTransformer）检索符合描述的图片。
4. **JPG 到 PNG 批量转换**：批量将 JPG 图片转换为 PNG 格式。
5. **人脸识别**：通过人脸识别技术，识别图片中是否包含指定人物。

## 文件结构

```
project/
│
├── jpg_to_png.py                # JPG 到 PNG 的批量转换脚本
├── write.py                     # 将tag写入图片
├── face.py                      # 人脸识别功能
├── read.py                      # 批量读取tag
├── find.py                      # 通过自然语言搜索相应图片
├── requirements.txt             # 项目依赖的 Python 库
├── README.md                    # 项目说明文档
└── new/                         # 存储处理后的 PNG 图片
└── before/                      # 存储原始图片（JPG/PNG）
```

## 安装与运行

### 1. 克隆项目

首先，克隆该项目到本地：

```bash
git clone https://github.com/tamikip/SearchablePic-By-AI.git
cd SearchablePic-By-AI
```

### 2. 安装依赖

使用 `pip` 安装项目所需的依赖：

```bash
pip install -r requirements.txt
```

### 3. 运行主程序

主程序会处理 `before` 文件夹中的图片，并将处理后的 PNG 图片存储在 `new` 文件夹中：

```bash
python main.py
```

### 4. 进行自然语言查询

在运行主程序后，您可以通过输入自然语言描述来查询符合条件的图片：
例如:
```bash
请输入查询条件: 女生拉着男生的手
图片是否是由相机拍摄？ 是
```

### 5. 批量转换 JPG 到 PNG

如果您有 JPG 图片需要转换为 PNG，可以使用以下命令：

```bash
python jpg_to_png.py
```

### 6. 人脸识别

要使用人脸识别功能，请将已知人物的图片放入项目中，并运行人脸识别脚本：

```bash
python face_recognition.py
```

## 代码说明

### 1. `get_png_files(folder_path)`

该函数用于获取指定文件夹下所有 PNG 文件的路径。

### 2. `gpt_pic(img_path)`

使用 GLM-4V-Plus 模型生成图片的标签，并返回标签内容。

### 3. `Text_embedded_in_image(image_path, content)`

将生成的标签、图片类型和修改日期嵌入到 PNG 图片的元数据中。

### 4. `process_image(image_path)`

处理单张图片，生成标签并嵌入元数据。

### 5. `find_images_by_query(folder_path, query, if_camera)`

根据用户输入的自然语言查询，检索符合描述的图片。

### 6. `batch_convert_jpg_to_png(input_folder)`

批量将指定文件夹中的 JPG 图片转换为 PNG。

### 7. `face.py`

通过人脸识别技术，识别图片中是否包含指定人物。

## 注意事项

- 该项目依赖于外部 API（如 GLM-4V-Plus 模型），请确保您有正确的 API 密钥并且网络连接正常。
- 请确保在 `before` 文件夹中放入需要处理的图片，处理后的图片会保存到 `new` 文件夹中。
- 人脸识别功能需要安装 `face_recognition` 库，并确保图片中有清晰的人脸。

## 未来计划

- 增强图片标签生成的准确性。
- 支持更多的图片格式和处理功能。
- 增加更多的自然语言处理能力，提升图片检索的效果。

## 贡献

欢迎任何形式的贡献！如果您有任何建议或发现了问题，请通过提交 issue 或 pull request 的方式与我们联系。

## 许可证

该项目使用 MIT 许可证。
