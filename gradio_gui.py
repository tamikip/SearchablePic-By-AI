import gradio as gr
from PIL import Image
from find import *
from face import *
from write import write


def generate_image(text_input, option_input, upload_input):
    if option_input == "相机":
        option_input = "camera"
    elif option_input == "其他(网络图片，截屏等)":
        option_input = "others"
    else:
        option_input = "all"

    matching_images = find_images_by_query("processed_image", text_input, option_input)
    matching_images = ["processed_image/" + item for item in matching_images]

    if matching_images:
        if upload_input is not None:
            matching_images = [x for x in matching_images if face_match(x, upload_input)]

        if matching_images:
            try:
                return f"匹配到的图片: {', '.join(matching_images)}", matching_images
            except Exception as e:
                return f"无法打开匹配的图片: {e}", []
        else:
            return "没有找到与上传图片匹配的人脸。", []
    else:
        return "没有找到符合条件的图片。", []


with gr.Blocks() as demo:
    with gr.Tab("图片打标"):
        gr.Markdown("## 图片打标")
        output_text_page1 = gr.Textbox(label="提示信息", interactive=False)
        tag_button = gr.Button("开始打标！")
        tag_button.click(fn=write, outputs=output_text_page1)

    with gr.Tab("图片查找"):
        gr.Markdown("## 图片查找器")

        # 页面 2 的内容
        text_input_page2 = gr.Textbox(label="图片的描述", placeholder="请输入一些查找的图片的信息...")
        option_input_page2 = gr.Radio(label="图片种类", choices=["相机", "其他(网络图片，截屏等)", "不限"], value="相机")
        upload_input_page2 = gr.File(label="上传你想匹配的人脸（可选）", type="filepath", file_types=["image"])
        generate_button_page2 = gr.Button("开始查找")
        output_text_page2 = gr.Textbox(label="提示信息")
        output_gallery_page2 = gr.Gallery(label="生成的图片")

        # 页面 2 的按钮点击事件
        generate_button_page2.click(fn=generate_image,
                                    inputs=[text_input_page2, option_input_page2, upload_input_page2],
                                    outputs=[output_text_page2, output_gallery_page2])

demo.launch(server_port=7500)
