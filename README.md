# Wapt - Web Application Packaging Toolkit

[中文](README_zh.md) | English

It helps to package Web URL into a single executable file via [Webui](https://webui.me).

## How to build

1. Clone the repository

	```bash
	git clone https://github.com/hibays/Wapt.git
	cd Wapt
	```

2. Directly build via CMake

	```bash
	cmake -B build -DCMAKE_BUILD_TYPE=Release
	cmake --build build
	```

Then, you can find the executable file in the `build` directory.
You can just run the executable file to start the web application.
**That's it! Simple as that!**

## How to add a new Web URL

Just use the `add_url.py` script to add a new Web URL.

```bash
# Interactive mode
python add_url.py

# CLI mode
python add_url.py --name myapp --url https://myapp.com --icon myapp.ico
```
