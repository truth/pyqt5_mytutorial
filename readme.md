# 1. python环境

## 1.1 虚拟python环境

```shell
# To create a virtual environment in the current directory, execute the following command:
$ python3 -m venv venv

#This creates the venv/ folder. To activate the virtual environment on Windows, run:
$ call venv/scripts/activate.bat
On Mac and Linux, use:
$ source venv/bin/activate
```

## 1.2 安装包

> 注意需要时python3.5 or 3.6 环境， 不然fbs 生成exe有问题

```shell
# pip install pipreqs
$ pip freeze > requirements.txt #导出项目中的dependency
$ pip install pyqt5==5.9.2
$ pip install opencv-python==4.1.0.24
$ pip install fbs
$ pip install numpy 
```

**生成依赖包清单方法**

[使用Python项目生成所有依赖包的清单方式](https://www.cnblogs.com/simadi/p/15375911.html)

# 2. 项目实践

##  2.1 参考

> PyQt5 tutorial https://build-system.fman.io/pyqt5-tutorial
> fbs tutorial https://github.com/mherrmann/fbs-tutorial

```shell
# 安装fbs实例
$ pip install fbs-tutorial
```



## 2.2  创建

```shell
$ fbs startproject
```

<code>./src</code>目录下为项目文件

初始main.py如下:

```python
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow

import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = QMainWindow()
    window.resize(250, 150)
    window.show()
    exit_code = appctxt.app.exec()      # 2. Invoke appctxt.app.exec()
    sys.exit(exit_code)
```



## 2.3 运行工程

```shel
$ fbs run
```

## 2.4 冻结程序(Freezing the app)

```shell
$ fbs freeze 
Done. You can now run `target\MyFbsApp\MyFbsApp.exe`. If that doesn't
work, see https://build-system.fman.io/troubleshooting.
# 注意opencv的dll需要手工copy到`target\MyFbsApp`下
$ copy venv\Lib\site-packages\cv2\opencv_ffmpeg410_64.dll .\target\MyFbsApp
```

