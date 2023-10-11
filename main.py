import os

import keyboard
from PIL import ImageGrab
import datetime
import tempfile
import requests
from plyer import notification
import pyperclip

log_file_path = ""  # 日志保存的路径  绝对路径，如：C:\\User
upload_domain = ""  # 上传域名


def get_formatted_datetime():
    # 获取当前时间的datetime对象
    current_time = datetime.datetime.now()

    # 使用strftime函数格式化时间
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_time


def write_log(content=None):
    if content is None:
        return
    with open("{}\\log.log".format(log_file_path), 'a+', encoding='utf-8') as f:
        f.write("{} {}\n".format(get_formatted_datetime(), content))


def windows_notify(content):
    notification.notify(
        title="上传通知",  # 标题
        message=content,  # 内容
        # app_icon="None",  # 图标
        timeout=2,  # 通知持续时间
    )


# 判断本地路径的path是否为图片
def is_local_image_path(path):
    # 判断路径是否存在
    if not os.path.exists(path):
        return False

    # 判断路径是否为文件
    if not os.path.isfile(path):
        return False

    # 获取文件扩展名
    ext = os.path.splitext(path)[1].lower()

    # 判断文件扩展名是否为图片格式
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    if ext in image_extensions:
        return True

    return False


def upload_clipboard_image():
    # 获取剪贴板中的图片
    image = ImageGrab.grabclipboard()

    if image is None:
        not_image_tip = "剪贴板中没有图片数据。"
        write_log(not_image_tip)
        windows_notify(not_image_tip)
        return
    # print(image)
    write_log("开始上传")
    windows_notify("开始上传")
    # 创建临时文件来保存图片
    is_save_tem_file = True  # 是否需要保存临时文件
    if isinstance(image, list) and len(image) == 1:
        if is_local_image_path(image[0]) is False:
            windows_notify("剪切板中的地址非图片！")
            return
        is_save_tem_file = False  # 说明复制了图片的本地文件路径，就直接使用这个文件不需要临时文件了
        temp_file_path = image[0]

    if is_save_tem_file:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file_path = temp_file.name
            image.save(temp_file_path, 'PNG')
            write_log("temp_file_path:{}".format(temp_file_path))

    try:
        # 使用requests.post()方法上传图片文件
        with open(temp_file_path, 'rb') as file:
            response = requests.post("{}/upload".format(upload_domain), files={'image': file}, verify=False,
                                     proxies={"http": None, "https": None})
            if response.status_code == 200:
                write_log("图片上传成功。")
                upload_url = "{}{}".format(upload_domain, response.json()[0]['src'])
                write_log("图片地址：{}".format(upload_url))
                windows_notify("图片上传成功！地址为：" + upload_url)
                pyperclip.copy(upload_url)  # 将地址写到剪切板
            else:
                write_log("图片上传失败。")
    except Exception as e:
        write_log("图片上传发生错误:{}".format(str(e)))
    finally:
        # 删除临时文件
        if temp_file_path and is_save_tem_file:
            os.remove(temp_file_path)


def main():
    write_log("当前进程PID：{}".format(os.getpid()))
    keyboard.add_hotkey("shift+ctrl+alt+u", upload_clipboard_image)
    keyboard.wait()


if __name__ == '__main__':
    main()
