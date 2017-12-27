# py-chrome-bookmarks-markdown
python导出chrome书签到markdown文件

本代码是在 https://github.com/bdesham/py-chrome-bookmarks 基础上改动了一些内容. 感谢[Benjamin Esham](https://github.com/bdesham).导出html文件可参考此项目。

**本代码修改内容如下：**

1. 修改导出文件内容中文，原导出文件中中文为HTML Entities格式
2. 增加目录
3. 增加文件夹过滤

#### 使用方式

##### py-chrome-bookmarks-markdown

可直接使用命令行
```cmd
python py-chrome-bookmarks-markdown.py test1.md
```
会在当前项目中直接生成一个test1.md文件，也可指定书签位置，默认会去Chrome安装的相对路径去找，也可直接
调试py文件，我在里面标注好了注释。
