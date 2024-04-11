# bw-cli-autotype

Python scripts to process bitwarden-cli server API (Using with quicker)

配合某个 Quicker 动作来实现 Bitwarden 在 Windows 桌面程序中的自动输入功能。具体说明参考该 Quicker 动作的介绍页面。

## 安装依赖

通过 pip 命令安装需要的第三方库：

```bash
pip install pyperclip requests python-dotenv
```

## 设置环境变量

在 python 脚本所在目录新建文件`.env`，在里面添加 bw-cli 通过 `serve` 命令暴露的API服务器的基本地址。

```properties
BASE_URL="http://127.0.0.1:8087"
MASTER_PASS="123456"
```
