import os
from markdownify import markdownify as md
import markdown as md_converter
from bs4 import BeautifulSoup
import argparse

def read_html_files(directory):
    """一个迭代器，遍历指定目录中的所有 HTML 文件"""
    for filename in os.listdir(directory):
        if filename.endswith('.html'):  # 只处理以 .html 结尾的文件
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                yield file.read(), filename  # 逐个读取文件内容和文件名

def html_to_markdown(directory):
    """将指定目录中的 HTML 文件转换为 Markdown 格式"""
    for html_content, filename in read_html_files(directory):
        markdown_content = md(html_content)  # 转换为 Markdown
        yield markdown_content, filename

def markdown_to_html(markdown_content):
    """将 Markdown 内容转换为 HTML 格式"""
    html_content = md_converter.markdown(markdown_content)  # 使用 markdown 库将其转换
    return html_content

def extract_title(html_content):
    """从 HTML 内容中提取 <h1> 标签中的标题"""
    soup = BeautifulSoup(html_content, 'html.parser')
    h1_title = soup.find('h1')  # 尝试找到第一个 <h1> 标签
    return h1_title.text.strip() if h1_title else 'Untitled'  # 如果<h1>存在则返回其文本，否则返回默认标题

def create_full_html(title, body_content):
    """根据标题和 body 内容创建完整的 HTML 文档"""
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
{body_content}
</body>
</html>
"""
    return full_html

def clear_unwanted_elements(html_content):
    """清除异常 SVG 数据 URI 图片标签和特定 <p> 标签"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # 清除所有 <img> 标签中 src 以 data:image/svg+xml 开头的元素
    for img in soup.find_all('img'):
        if img.get('src', '').startswith('data:image/svg+xml'):
            img.decompose()  # 移除该 img 标签

    # 清除特定空的 <p> 标签
    for p in soup.find_all('p'):
        if p.text.strip() == ")":  # 如果 <p> 标签内文本是‘)’
            p.decompose()  # 移除该 <p> 标签

    return str(soup)

def main():
    #设定输入输出目录
    parser = argparse.ArgumentParser(description='Convert HTML files to Markdown and generate new HTML files.')
    parser.add_argument('--input', type=str, default='./texts/', help='Input directory containing HTML files.')
    parser.add_argument('--output', type=str, default='./output/', help='Output directory for generated HTML files.')
    args = parser.parse_args()

    input_dir = args.input
    output_dir = args.output

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 使用函数读取并转换文件
    for markdown_content, filename in html_to_markdown(input_dir):
        # 去除前 7 行
        markdown_lines = markdown_content.splitlines(keepends=True)
        markdown_content_cleaned = ''.join(markdown_lines[7:])  # 仅保留从第 8 行开始的内容

        # 将 Markdown 转换为 HTML
        body_content = markdown_to_html(markdown_content_cleaned)

        # 提取原始 HTML 的标题（在 body 中查找 <h1>）
        title = extract_title(body_content)  # 从 HTML 提取标题

        # 清除异常 SVG 图片和特定的 <p> 标签
        body_content = clear_unwanted_elements(body_content)

        # 创建完整的 HTML 文档
        full_html = create_full_html(title, body_content)

        # 使用标题命名输出文件，去掉无效字符并确保唯一性
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-')).rstrip()
        file_base_name = safe_title or "Untitled"
        file_path = os.path.join(output_dir, f"{file_base_name}.html")

        # 如果文件存在，添加一个序号以确保文件名唯一
        count = 1
        while os.path.exists(file_path):
            file_path = os.path.join(output_dir, f"{file_base_name}_{count}.html")
            count += 1

        # 保存完整 HTML 输出到文件
        with open(file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(full_html)  # 保存新的完整 HTML 文档

if __name__ == '__main__':
    main()
