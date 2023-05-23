import sys
import time
import os
import click
import requests
import pyperclip
from io import BytesIO
from PIL import Image, ImageGrab
import base64
from loguru import logger

# 控制台日志
logger.remove()
logger.add(
	sink=sys.stderr,
	level="INFO",
	format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>[<level>{level}</level>]<level>{message}</level>",
	backtrace=True,
	diagnose=False
)


class ImageProcessor:
	"""处理剪切板图片"""

	def __init__(self):
		self.last_image = None

	@staticmethod
	def get_clipboard_image() -> Image.Image | None:
		"""获取剪切板图片"""
		return ImageGrab.grabclipboard()

	@staticmethod
	def convert_to_bytes(image: Image.Image, optimize: bool = True, progressive: bool = True) -> bytes:
		"""将图片转换为字节串"""
		io = BytesIO()
		image.save(io, format="PNG", optimize=optimize, progressive=progressive)
		return io.getvalue()


class Clipboard:
	"""剪切板"""

	@staticmethod
	def get():
		"""获取剪贴板内容"""
		return pyperclip.paste()

	@staticmethod
	def set(text):
		"""设置剪贴板内容"""
		pyperclip.copy(text)


def upload_image(key: str, image_content: bytes) -> dict:
	"""上传图片"""
	url = "https://api.imgbb.com/1/upload"
	method = "post"
	payload = {
		"key": key
	}
	files = [("image", image_content)]
	try:
		response = requests.request(method=method, url=url, data=payload, files=files)
	except Exception as e:
		raise Exception({"message": f"网络连接异常，{str(e)}"})
	data = response.json()
	assert data.get("success") is True, data
	return {"url": data["data"]["url"]}


class ClipboardMonitor:
	"""监视剪切板内容是否发生变化，并根据变化执行相应操作"""

	def __init__(self, delay: int, image_processor: ImageProcessor):
		self.delay = delay
		self.image_processor = image_processor
		self.clipboard = Clipboard()

	def start(self, key):
		while True:
			try:
				if self.clipboard.get() == self.image_processor.last_image:
					continue
				self.image_processor.last_image = self.clipboard.get()
				image = self.image_processor.get_clipboard_image()  # 获取剪切板图片
				if not isinstance(image, Image.Image):
					continue
				image_bytes = self.image_processor.convert_to_bytes(image)
				url_dict = upload_image(key, image_bytes)
				self.clipboard.set(url_dict["url"])  # 设置剪切板内容
				logger.info(f"剪切板图片转链接成功，链接为{url_dict['url']}")
				time.sleep(self.delay)
			except KeyboardInterrupt:
				break


class Program:
	"""启动程序，并进行相应的配置"""

	def __init__(self, key, delay):
		logger.info("******剪切板图片转链接工具******")
		logger.info(f"> key: {key}")
		logger.info(f"> 轮询间隔时间：{delay}秒")
		logger.info("------- 程序开始运行")
		imageProcessor = ImageProcessor()
		ClipboardMonitor(delay, imageProcessor).start(key)

	def __del__(self):
		logger.info("------- 程序已退出")


@click.command()
@click.option("--key", "-k", prompt=True, required=True, help="key为从图像共享网站https://imgbb.com申请的API key")
@click.option("--delay", "-d", default=2, type=int, help="轮询间隔时间，默认为2秒")
def main(key, delay):
	Program(key, delay)


if __name__ == '__main__':
	main()
