from json import loads
import argparse
from platform import system
from re import match
from os import environ
from os.path import expanduser

# 过滤name
filter_name_list = {'My work', '书签栏', 'websites'}

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&#39;",
    ">": "&gt;",
    "<": "&lt;",
}

output_file_template = """
<h3>书签目录</h3>
{catelog}
{bookmark_bar}

{other}
"""

# 如需本地调试可注释掉这一段 START
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description="python导出chrome书签到markdown文件.")
parser.add_argument("input_file", type=argparse.FileType('r', encoding='utf-8'), nargs="?",
                    help="读取书签的位置,可以指定文件位置(相对路径，绝对路径都可以),非必填,默认为Chrome的默认书签位置")
parser.add_argument("output_file", type=argparse.FileType('w', encoding='utf-8'),
                    help="读取书签的位置,可以指定文件位置(相对路径，绝对路径都可以),必填")

args = parser.parse_args()

if args.input_file:
    input_file = args.input_file
else:
    if system() == "Darwin":
        input_filename = expanduser("~/Library/Application Support/Google/Chrome/Default/Bookmarks")
    elif system() == "Linux":
        input_filename = expanduser("~/.config/google-chrome/Default/Bookmarks")
    elif system() == "Windows":
        input_filename = environ["LOCALAPPDATA"] + r"\Google\Chrome\User Data\Default\Bookmarks"
    else:
        print('Your system ("{}") is not recognized. Please specify the input file manually.'.format(system()))
        exit(1)

    try:
        input_file = open(input_filename, 'r', encoding='utf-8')
    except IOError as e:
        if e.errno == 2:
            print("The bookmarks file could not be found in its default location ({}). ".format(e.filename) +
                  "Please specify the input file manually.")
            exit(1)

output_file = args.output_file

# 如需本地调试可注释掉这一段 END

# 本地调试可以指定文件名测试 START
# input_filename = 'C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default/Bookmarks'
# input_file = open(input_filename, 'r', encoding='utf-8')
# output_file_name = 'test2.md'
# output_file = open(output_file_name, 'w', encoding='utf-8')
# 本地调试可以指定文件名测试 END

# 目录
catelog = list()


def html_escape(text):
    return ''.join(html_escape_table.get(c, c) for c in text)


def html_for_node(node):
    # 判断url和children即判断是否包含在文件夹中
    if 'url' in node:
        return html_for_url_node(node)
    elif 'children' in node:
        return html_for_parent_node(node)
    else:
        return ''


def html_for_url_node(node):
    if not match("javascript:", node['url']):
        return '- [{}]({})\n'.format(node['name'], node['url'])
    else:
        return ''


def html_for_parent_node(node):
    return '{0}\n\n{1}\n'.format(filter_catelog_name(node),
                                 ''.join([filter_name(n) for n in node['children']]))


# 过滤文件夹
def filter_name(n):
    if n['name'] in filter_name_list:
        return ''
    else:
        return html_for_node(n)


# 过滤目录名
def filter_catelog_name(n):
    if n['name'] in filter_name_list:
        return ''
    else:
        catelog.append('- [{0}](#{0})\n'.format(n['name']))
        return '<h4 id={0}>{0}</h4>'.format(n['name'])


contents = loads(input_file.read())
input_file.close()

bookmark_bar = html_for_node(contents['roots']['bookmark_bar'])
other = html_for_node(contents['roots']['other'])
catelog_str = ''.join(a for a in catelog)

output_file.write(output_file_template.format(catelog=catelog_str, bookmark_bar=bookmark_bar, other=other))
