import sys
import time
import os
import click
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
	"""处理图片"""

	def __init__(self):
		self.last_image = None

	@staticmethod
	def get_clipboard_image() -> Image.Image|None:
		"""获取剪切板图片"""
		return ImageGrab.grabclipboard()

	@staticmethod
	def convert_to_bytes(image: Image.Image, quality: int = 30, optimize: bool = True, progressive: bool = True) -> bytes:
		"""将图片转换为bytes格式"""
		io = BytesIO()
		image.save(io, format="JPEG", quality=quality, optimize=optimize, progressive=progressive)
		return io.getvalue()

class Clipboard:
	"""剪切板，包括剪切板内容的获取及设置"""

	@staticmethod
	def get():
		"""获取剪贴板内容"""
		return pyperclip.paste()

	@staticmethod
	def set(text):
		"""设置剪贴板内容"""
		pyperclip.copy(text)



class ImageConverter:
	"""将图片转换为指定格式"""

	def __init__(self, choice: str):
		self.choice = choice

	def convert(self, image_bytes: bytes) -> str:
		"""将图片转换为指定格式，包括转换为链接或者base64"""
		if self.choice == "link":
			return "data:image/png;base64," + self.encode_base64(image_bytes)
		elif self.choice == "base64":
			return self.encode_base64(image_bytes)
		else:
			raise ValueError(f"Invalid choice: {self.choice}")

	@staticmethod
	def encode_base64(image_bytes: bytes) -> str:
		"""将bytes格式的图片转换为base64格式"""
		return base64.b64encode(image_bytes).decode()


class ClipboardMonitor:
	"""监视剪切板内容是否发生变化，并根据变化执行相应操作"""

	def __init__(self, delay: int, image_processor: ImageProcessor, image_converter: ImageConverter):
		self.delay = delay
		self.image_processor = image_processor
		self.image_converter = image_converter

	def start(self):
		clipboard = Clipboard()
		while True:
			try:
				if clipboard.get() != self.image_processor.last_image:
					self.image_processor.last_image = clipboard.get()
					image = self.image_processor.get_clipboard_image()		# 获取剪切板图片
					if image and isinstance(image, Image.Image):
						image_bytes = self.image_processor.convert_to_bytes(image)
						result = self.image_converter.convert(image_bytes)	# 将图片转为指定的格式
						clipboard.set(result)		# 设置剪切板内容
						logger.info(f"剪切板图片转{self.image_converter.choice}成功!!!")
				time.sleep(self.delay)
			except KeyboardInterrupt:
				break


class Program:
	"""启动程序，并进行相应的配置，包括选择转换格式、轮询间隔等"""

	def __init__(self,choice,delay):
		logger.info("******剪切板图片转link工具******")
		logger.info(f"> 选择转换方式：{choice}")
		logger.info(f"> 轮询间隔时间：{delay}秒")
		logger.info("> 程序开始运行>>>>>>>>>>>>>>>>")
		imageProcessor = ImageProcessor()
		imageConverter = ImageConverter(choice)
		ClipboardMonitor(delay, imageProcessor, imageConverter).start()

	def __del__(self):
		logger.info("程序已退出")



@click.command()
@click.option("--choice", "-c", default="link", type=click.Choice(["link", "base64"]),
			  help="选择转为link或base64，默认转为link")
@click.option("--delay", "-d", default=2, type=int, help="轮询间隔时间，默认为2秒")
def main(choice,delay):
	Program(choice,delay)


if __name__ == '__main__':
	main()
