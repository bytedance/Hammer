# 文档编写

Hammer 使用 [Sphinx](https://www.sphinx-doc.org/) 来生成文档。

## 配置环境

要在本地生成文档，请先安装依赖项：

```shell
pip install -r requirements/doc.txt
```

## 文件结构

```shell
/doc/
├── en                    # English documentation
│   ├── Makefile          # Sphinx Makefile
│   ├── _build/           # Static web files
│   ├── api_reference/    # Directory of APIs (generated via docstring)
│   ├── conf.py           # Sphinx configuration
│   ├── developer_guide/  # Directory of developer guide
│   ├── faq.md            # Frequently asked questions
│   ├── index.rst         # Home of documentation
│   ├── make.bat          # Sphinx make script
│   └── user_guide/       # Directory of user guide
└── zh-hans               # Zh-Hans documentation
    ├── Makefile          # Sphinx Makefile
    ├── _build/           # Static web files
    ├── api_reference/    # Directory of APIs (generated via docstring)
    ├── conf.py           # Sphinx configuration
    ├── developer_guide/  # Directory of developer guide
    ├── faq.md            # Frequently asked questions
    ├── index.rst         # Home of documentation
    ├── make.bat          # Sphinx make script
    └── user_guide/       # Directory of user guide
```

## 生成静态文件

在文档源的根目录下运行以下命令生成静态文件：

```shell
make html
```

要删除生成的结果，你可以直接删除 `_build` 文件夹。
