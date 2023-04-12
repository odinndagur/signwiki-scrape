from bs4 import BeautifulSoup as bs
import os
import mwparserfromhell

def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    # this has to be last:
    s = s.replace("&amp;", "&")
    return s

import re
def split_by_number(input_str):
    match = re.search("\d", input_str)

    if match:
        index = match.start()
        first_part = input_str[:index]
        second_part = input_str[index:]
        return first_part, second_part
        # print("First part:", first_part)
        # print("Second part:", second_part)
    else:
        return input_str, ''
        # print("No numbers found in string")

all_signs = []

def strip_html_comments_and_whitespace(input_str):
    youtube_pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|v\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    output_str = input_str

    output_str = re.sub(youtube_pattern,r'\1',output_str)
    output_str = re.split('<!--.*',output_str)[0]
    output_str = output_str.strip()

    return output_str    


def main():
    # Read the XML file
    xml_dir = 'xml_data'
    files = os.listdir(xml_dir)
    sorted_files = sorted(files,key=lambda f: int(f[:2]))

    for file in sorted_files:
        full_path = os.path.join(xml_dir,file)
        with open(full_path, "r") as file:
            content = file.read()
        bs_parsed = bs(content, 'lxml')
        pages = bs_parsed.findAll('page')
        print(f'{len(pages)} pages')
        for page in pages:
            print(page.title.text)
            title = page.title.text
            sign = {
                'title':title.strip(),
                'signwiki_id':page.id.text.strip()
            }
            if title:
                mwparsed = mwparserfromhell.parse(page.text)
                templates = mwparsed.filter_templates()
                # breakpoint()
                if templates:
                    params_list = templates[0].params
                    for param in params_list:
                        param,_,value = param.partition('=')
                        param = param.strip()
                        value = strip_html_comments_and_whitespace(value)
                        sign.update({param:value})
                        print(param,value)
                        val, num = split_by_number(param)
                        rank = 0
                        if num:
                            rank = num
            all_signs.append(sign)

    import json
    with open('signwiki-json-dump.json','wb') as f:
        f.write(json.dumps(all_signs,indent=4,ensure_ascii=False).encode('utf-8'))



    # {
    #     "phrase": "Bikar",
    #     "Image1": "bikar.jpg         <!--- t.d. sign_epli.jpg-->\n",
    #     "texti": "<!--- lýsið hvernig táknið er myndað-->\n",
    #     "myndunarstadur": "Hlutlaust rými\n",
    #     "handform": "A handform lokað\n",
    #     "ordflokkur": "Nafnorð\n",
    #     "efnisflokkur": "Hlutir <!--- Flokkur  -->\n",
    #     "munnhreyfing": "bikar\n",
    #     "tengsl1": "Vinna/sigra\n",
    #     "tengsl2": "Bestur\n",
    #     "tengsl3": "Hlaupa\n",
    #     "Image2": "Cup Winners' Cup.jpg          <!--- Mynd sem tengist merkingu táknsins-->\n",
    #     "youtube1": "hyONVASqaDA <!--- Kóði YouTube myndbands fyrir táknið-->\n",
    #     "utskyring": "<!--- Útskýring á notkun-->\n",
    #     "youtube2": "<!--- Kóði YouTube myndbands fyrir dæmi-->\n",
    #     "taknmal": "<!--- Setning á táknmáli-->\n",
    #     "islenska": "<!--- Setning á íslensku-->\n",
    #     "myndatexti": "bikar\n",
    #     "name": "bikar\n"
    # },


def test():
    # Read the XML file
    xml_dir = 'xml_data'
    files = os.listdir(xml_dir)
    sorted_files = sorted(files,key=lambda f: int(f[:2]))

    for file in sorted_files[3:4]:
        full_path = os.path.join(xml_dir,file)
        with open(full_path, "r") as file:
            content = file.read()
        bs_parsed = bs(content, 'lxml')
        pages = bs_parsed.findAll('page')
        print(f'{len(pages)} pages')
        breakpoint()

main()