import re
import json

with open("skwiki-20201101-pages-articles1.xml", encode='utf8') as f:
    content = f.readlines()
        
json_file = open('file.json','w', encoding='utf8')

  
page = 0
page_text = 0
text = ""
data_holder = []
data = None


for line in content:    
    if re.search("</page", line):
        page = 0

    if page == 1:
        if re.search("<title>", line):
            page_title = re.findall(r'>.*<', line)
            page_title = page_title[0].replace('>', '')
            page_title = page_title.replace('<', '')

        if re.search("<text", line):
            page_text = 1
        if re.search("</text>", line):
            page_text = 0
            text = text + line
            data = { 
                "title": page_title, 
                "raw_text":  text
            }
            data_holder.append(data)            
            text = ""

    if page_text == 1:
        text = text + line

    if re.search("<page", line):
        page = 1 


x = json.dumps(data_holder, indent=2)
json_file.write(x)   
json_file.close()
