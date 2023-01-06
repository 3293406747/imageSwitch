import sys
import time, os
import click
import pyperclip
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

	def main(self, choice="link"):
		print("******剪切板图片转link工具******")
		logger.info("> 程序开始运行>>>>>>>>>>>>>>>>")
		while True:
			im = self.getIm()
			if isinstance(im, Image.Image):
				imName = "im.png"
				im.save(imName)
				with open(imName, "rb") as f:
					s = self.b64encode(f.read())
					if choice == "link":
						# 转为链接
						s = "data:image/png;base64," + s
						flag = "link"
					elif choice == "base64":
						# 转为base64
						flag = "base64"
					else:
						raise ValueError
					self.copy(s)
					logger.info(f"剪切板图片转{flag}成功!!!")
				os.remove(imName)
			time.sleep(2)

	def __del__(self):
		logger.info("> 程序运行结束")


@click.option("--choice", "-c", default="link", type=click.Choice(["link", "base64"]), help="选择转为link或base64，默认转为link")
@click.command()
def main(choice):
	ImageSwitch().main(choice)


if __name__ == '__main__':
	main()
