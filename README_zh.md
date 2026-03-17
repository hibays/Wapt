# Wapt - Web Application Packaging Toolkit

中文 | [English](README.md)

它通过 [Webui](https://webui.me) 帮助将 Web URL 打包成单个可执行文件。

## 如何构建

1. 克隆仓库

	```bash
	git clone https://github.com/hibays/Wapt.git
	cd Wapt
	```

2. 直接通过 CMake 构建

	```bash
	cmake -B build -DCMAKE_BUILD_TYPE=Release
	cmake --build build
	```

然后，您可以在 `build` 目录中找到可执行文件。
您可以直接运行可执行文件来启动 Web 应用程序。
**对！就是这么简单！**

## 如何添加新的 Web URL

只需使用 `add_url.py` 脚本添加新的 Web URL。

```bash
# 交互模式
python add_url.py

# CLI 模式
python add_url.py --name myapp --url https://myapp.com --icon myapp.ico
```
