import re
import json
import os
from config.config import ROOT_DIR, out_dir

out_file = open(ROOT_DIR.joinpath('data/wikipedia.json'), 'w+', encoding='utf8')
out_file.write("[\n")

# parse all files in directory
for filename in os.listdir(out_dir):
    with open(os.path.join(out_dir, filename), 'r', encoding='utf8') as input_file:
        content = input_file.readlines()

        page = False
        page_text = False
        text = ""

        for line in content:
            if re.search("</page", line):
                page = False

            if page:
                if re.search("<title>", line):
                    page_title = re.findall(r'>.*<', line)
                    page_title = page_title[0].replace('>', '')
                    page_title = page_title.replace('<', '')

                if re.search("<text", line):
                    page_text = True
                if re.search("</text>", line):
                    page_text = False
                    text = text + line
                    data = {
                        "title": page_title,
                        "raw_text": text,
                        "language": "Slovenčina"
                    }
                    out_file.write(json.dumps(data, indent=2, ensure_ascii=False))
                    out_file.write(",\n")
                    text = ""

            if page_text:
                text = text + line

            if re.search("<page", line):
                page = True

out_file.write("]\n")
out_file.close()
