# 密码生成器

一个用于生成强随机密码的桌面应用程序。

## 主要功能

*   生成可自定义长度和字符类型（大写字母、小写字母、数字、特殊字符）的密码。
*   一次生成多个密码。
*   显示密码强度和熵值。
*   将密码复制到剪贴板。
*   查看密码生成历史记录。
*   密码加密存储（可选，如果 `encryption_manager.py` 提供了此功能）。

## 技术栈

*   Python
*   PySide6 (用于图形用户界面)

## 安装

1.  克隆本仓库：
    ```bash
    git clone <repository_url>
    ```
2.  进入项目目录：
    ```bash
    cd password
    ```
3.  安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

## 使用方法

运行应用程序：

```bash
python main.py
```

## 如何贡献

1.  Fork 本仓库。
2.  创建一个新的分支 (`git checkout -b feature/AmazingFeature`)。
3.  提交您的更改 (`git commit -m 'Add some AmazingFeature'`)。
4.  将更改推送到分支 (`git push origin feature/AmazingFeature`)。
5.  打开一个 Pull Request。

## 项目截图 (可选)

(在此处可以添加应用程序的截图)

## 许可证

该项目采用 [MIT](LICENSE) 许可证。