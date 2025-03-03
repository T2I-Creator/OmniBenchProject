from PIL import Image, ImageDraw, ImageFont
import os

# Directory paths
base_path = "static/images/for_show_cross"
output_base_path = "static/images/cross_combined"
os.makedirs(output_base_path,  exist_ok=True)
skill_dirs = os.listdir(base_path)

# Function to create a combined image for each skill

MODEL_DICT = {
    "mindalle": "minDALL-E",
    "sd21": "SD v2",
    "attend": "Attn-Exct v2",
    "sdxl": "SDXL",
    "pix": "PixArt-sigma",
    "sd3": "SD v3",
    "flux": "FLUX.1",
    "playground": "Playground v2.5",
    "sd35": "SD v3.5",
    "janus": "Janus Pro"
}
MODELS = ["mindalle", "sd21", "attend", "sdxl", "playground", "pix",
          "sd3", "flux", "sd35", "janus"]


def combine_images(skill_dir, id):
    skill_path = os.path.join(base_path, skill_dir)
    # Get all model subdirectories under the skill directory
    model_dirs = MODELS
    model_0 = model_dirs[0]
    # Read the description file (assuming it's named '1.txt')
    with open(os.path.join(skill_path, model_0, '1.txt'), 'r', encoding='utf-8') as f:
        description = f.read().strip()
    if description == "The excited dog is above a velvet bed that is underneath it.":
        description = "The excited dog is above a velvet bed."
    if description == "There is a curtain, a laptop, and a pair of eyeglasses. The curtain is positioned next to the laptop, while the laptop rests on top of the eyeglasses.":
        description = "The curtain is positioned next to the laptop, while the laptop rests on top of the eyeglasses."
    description = description.capitalize()
    if description[-1] != ".":
        description += "."

    images = []
    model_names = []
    # 设定图片裁剪或调整大小的目标尺寸（例如 256x256）
    target_size = (256, 256)
    for model in model_dirs:
        # 获取图片路径（假设每个模型只有一张图片）
        image_path = os.path.join(skill_path, model, "1.png")
        img = Image.open(image_path)
        img = img.resize(target_size)  # 调整图片大小为目标尺寸
        images.append(img)
        model_names.append(model)

    # 获取每张图片的宽度和高度
    img_width, img_height = images[0].size

    # 为每个图像添加上方的空白空间（比如 40 像素）
    title_height = 40

    # 创建一个空白的画布，大小为2x5排列的图像，并增加空白空间
    new_img = Image.new(
        'RGB', (img_width * 5+30, img_height * 2 + title_height*3), color="white")
    # 加载更大的字体
    font = ImageFont.truetype(
        "/System/Library/Fonts/Supplemental/Arial.ttf", 20)  # 可以根据需要调整字体大小
    font_d = ImageFont.truetype(
        "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf", 24)  # 可以根据需要调整字体大小
    # 遍历将图片粘贴到新画布
    for i, img in enumerate(images):
        x = 5+(i % 5) * (img_width+5)
        y = (i // 5) * (img_height + title_height) + \
            title_height  # 调整Y轴位置，留出空白空间

        new_img.paste(img, (x, y))

        # 添加模型名称文字
        draw = ImageDraw.Draw(new_img)
        text = MODEL_DICT[model_names[i]]
        text_width, text_height = draw.textsize(text, font=font)

        # 将文字居中并放置在每个图片的上方
        text_position = ((x + (img_width - text_width) // 2),
                         y - (title_height-(title_height-20)/2))
        draw.text(text_position, text, font=font, fill="black")  # 使用黑色字体
    # Prompt
    text_width, text_height = draw.textsize(description, font=font_d)
    text_position = (((img_width * 5+30-text_width) // 2),
                     img_height * 2 + title_height*3 - (title_height-(title_height-24)/2))
    draw.text(text_position, description, font=font_d, fill="black")  # 使用黑色字体

    # 保存合并后的图片
    output_path = os.path.join(
        output_base_path, f"6_{id}_{skill_dir}_combined.png")
    new_img.save(output_path)


# 处理每个技能目录
for id, skill_dir in enumerate(sorted(skill_dirs)):
    combine_images(skill_dir, id)
