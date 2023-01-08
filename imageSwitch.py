import sys
import time, os
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


class ImageSwitch:
	""" 剪切板图片自动转为链接或base64 默认转为链接 """

	def __init__(self):
		self.__imageFlag = "link"

	@staticmethod
	def getIm():
		""" 获取剪切板图片 """
		return ImageGrab.grabclipboard()

	@staticmethod
	def copy(target):
		""" 复制到剪切板 """
		pyperclip.copy(target)

	@staticmethod
	def b64encode(target):
		""" base64编码 """
		return base64.b64encode(target).decode()

	def switch(self, im, choice):
		""" 图像转换link或base64 """
		io = BytesIO()
		im.save(io, format="JPEG", quality=30, optimize=True, progressive=True)
		s = self.b64encode(io.getvalue())
		if choice == "link":  # 转为链接
			s = "data:image/png;base64," + s
		elif choice == "base64":  # 转为base64
			self.__imageFlag = "base64"
		else:
			raise ValueError
		return s

	def main(self, choice="link"):
		print("******剪切板图片转link工具******")
		logger.info("> 程序开始运行>>>>>>>>>>>>>>>>")
		while True:
			im = self.getIm()  # 获取剪切板图片
			if isinstance(im, Image.Image):
				s = self.switch(im, choice)  # 图像转换link或base64
				self.copy(s)  # 复制到剪切板
				logger.info(f"剪切板图片转{self.__imageFlag}成功!!!")
			time.sleep(2)

	def __del__(self):
		logger.info("> 程序运行结束")


@click.option("--choice", "-c", default="link", type=click.Choice(["link", "base64"]), help="选择转为link或base64，默认转为link")
@click.command()
def main(choice):
	ImageSwitch().main(choice)


if __name__ == '__main__':
	main()
