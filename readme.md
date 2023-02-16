# 剪切板图片转换工具

这是一个Python编写的剪切板图片转换工具，它可以将剪切板中的图片转换为指定格式，并将转换后的结果设置回剪切板中。
适用于无法粘贴图片的情况，可使用该工具将剪切板截图转换为链接或base64进行文本输入。

![](img/show.gif)

## 使用方法
### 依赖安装

在使用本工具之前，请确保已经安装以下依赖包：
- click
- pyperclip
- Pillow
- loguru

在命令行可以通过以下命令安装：
```shell
pip install requirements.txt
```

### 运行程序

在命令行运行以下命令启动程序：
```shell
python imageSwitch.py
```

### 参数设置

程序支持两个参数：
- --choice / -c：选择转换格式，可选项为 link 或 base64，默认为 link。
- --delay / -d：轮询间隔时间，单位为秒，默认为 2 秒。

例如，下面的命令将转换格式设为 base64，轮询间隔时间设为 3 秒：
```shell
python imageSwitch.py --choice base64 --delay 3
```

## 转换结果

程序将剪切板中的图片转换为指定格式，并将转换后的结果设置回剪切板中。转换结果可以通过直接粘贴或者通过其他支持的方式进行使用。

## 代码结构
- `logger`：配置控制台日志的格式、级别等。
- `ImageProcessor`：处理图片，包括获取剪切板图片并转换为bytes格式。
- `Clipboard`：获取和设置剪切板内容。
- `ImageConverter`：将图片转换为指定格式，包括转换为链接或者base64。
- `ClipboardMonitor`：监视剪切板内容是否发生变化，并根据变化执行相应操作。
- `Program`：启动程序，并进行相应的配置，包括选择转换格式、轮询间隔等。
- `main`：命令行入口，接受参数并调用 Program 类启动程序。

## 打包成可执行程序

如果你想将该 Python 程序打包成 Windows 可执行文件，可以使用 PyInstaller 工具进行打包。
打包后的程序可以在 Windows 上运行，而无需安装 Python 环境。

1. 安装 pyinstaller 工具

在命令行中运行以下命令安装 pyinstaller 工具：
```shell
pip install pyinstaller
```
2. 执行打包命令

在命令行中进入程序所在的文件夹，执行以下命令：
```shell
pyinstaller -F imageSwitch.py
```
其中，-F 表示打包成单个可执行文件，imageSwitch.py 是程序入口文件名。

3. 查找可执行文件

打包完成后，在生成的 dist 文件夹中可以找到可执行文件，其文件名与程序入口文件名相同。
将该文件拷贝到需要使用的计算机上，即可双击打开程序。

## 注意事项
- 该程序只能转换剪切板中的图片，无法转换文件或其他格式的图片。
- 由于转换图片会消耗一定的系统资源，建议适当增加轮询间隔时间，避免程序运行占用过多系统资源。
- 如果需要退出程序，可以按Ctrl+C组合键。
- 保证图像清晰度的条件下，生成的文本长度特别长，不适合大图片转换。

