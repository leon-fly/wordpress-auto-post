import mistune
import frontmatter
import os
import re
from blogpost import make_post
filepath = '/Users/Mac/Library/Mobile Documents/com~apple~CloudDocs/iworkspace/git-doc/study/kubernetes'
image_base_url = 'https://blog.leon.kylins.tech/wp-content/uploads/github/picture/'

def post(filepath):
    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
            print("post file [" + filepath + "]  >>>>>>>>>>>>>> ")
            post_one(content)
            print("post file [" + filepath + "]  <<<<<<<<<<<<<< ")
    elif os.path.isdir(filepath):
        print("post directory [" + filepath + "]  >>>>>>>>>>>>>> ")
        for file in os.listdir(filepath):
            if file.endswith('.md'):
                with open(filepath + '/' + file, 'r') as f:
                    content = f.read()
                    print("post file [" + filepath + '/' + file + "]")
                    post_one(content)
        print("post directory [" + filepath + "]  <<<<<<<<<<<<<< ")
    else:
        return 'File or directory not found'


def post_one(markdown_text):
    markdown_text = markdown_text.strip()
    parsed_markdown_data = frontmatter.loads(markdown_text) 
    front_matter = parsed_markdown_data.metadata
    markdown_body = parsed_markdown_data.content
    # find 
    
    markdown_body = relocate_all_image_in_markdown_text(markdown_body)
    markdown_body = remove_title_in_body(markdown_body)
    html_content = mistune.markdown(markdown_body) # 使用markdown和markdown2有格式混乱的情况，改用mistune
    title = front_matter['title']
    categories = front_matter['categories']
    tags = front_matter['tags']
    json_content = {"title":title, "body": html_content}
    make_post( json_content, categories, tags, None)

def relocate_all_image_in_markdown_text(markdown_body):
    markdown_image_replaced_text = markdown_body.replace("](../../../picture/", ']('+image_base_url)
    markdown_image_replaced_text = markdown_image_replaced_text.replace('](../../picture/', ']('+image_base_url)
    markdown_image_replaced_text = markdown_image_replaced_text.replace('](../picture/', ']('+image_base_url)
    return markdown_image_replaced_text

def remove_title_in_body(markdown_body):
    lines = markdown_body.split('\n')
    count = 0
    title = ''
    for line in lines:
        if line.startswith('# '):
            title = line
            count += 1
            if count > 1 :
                return markdown_body
    if (count == 1) :
        markdown_body = markdown_body.replace(title+'\n', '')
        return markdown_body
    return markdown_body
        
post(filepath)