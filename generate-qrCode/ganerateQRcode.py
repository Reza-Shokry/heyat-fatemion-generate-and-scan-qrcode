import qrcode
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display


def create_qr_code(data):
    # ایجاد یک شیء QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=24,
        border=0,
    )

    # اضافه کردن داده به کد QR
    qr.add_data(data)
    qr.make(fit=True)

    # ایجاد یک تصویر با کد QR
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save("temp_qr.png")


def embed_qr_code(background_image_filename, qr_data):
    # باز کردن تصویر اصلی
    original_img = Image.open(background_image_filename)

    # ایجاد یک کد QR
    create_qr_code(qr_data)

    # باز کردن تصویر Q
    qr_img = Image.open("temp_qr.png")

    # Embedding کد QR در تصویر اصلی
    original_img.paste(qr_img, (73, 73))  # مثال: Embed در یک مکان خاص (10, 10)

    # حذف تصویر موقت QR
    qr_img.close()

    return original_img


def add_text_to_image(original_img, output_image_path, text, position=(590, 690), font_size=40,
                      font_color=(255, 255, 255)):
    # ایجاد یک شیء ImageDraw برای افزودن متن
    draw = ImageDraw.Draw(original_img)

    font_path = "BTitrBold.ttf"
    # font_path = "BNazanin.TTF"

    # استفاده از یک فونت پیش‌فراخوانی شده یا مشخص کردن فونت
    font = ImageFont.truetype(font_path, font_size,
                              encoding='unic')  # می‌توانید یک فونت مخصوص با آدرس دلخواهتان استفاده کنید
    reshaped_text = arabic_reshaper.reshape(text)
    display_text = get_display(reshaped_text)

    # Get the text size
    text_size = draw.textlength(display_text, font=font)

    # Calculate the position to draw the text
    x = (position[0] - int(text_size)) / 2

    # y = (original_img.height - text_size[1]) / 2
    # افزودن متن به تصویر
    draw.text((x, position[1]), display_text, font=font, fill=font_color)

    # ذخیره تصویر نهایی
    original_img.save(output_image_path)
    # original_img.show()


file = open("dataBase.csv", "r", encoding='utf-8')
for line in file:
    splitLine = line.split(",")
    path = f"output\{splitLine[0]}.png"
    embed_image = embed_qr_code("background.png", splitLine[3])
    add_text_to_image(embed_image, path, splitLine[0], position=(650, 620))

