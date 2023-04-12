from bs4 import BeautifulSoup as bs
import os
from collections import defaultdict
import pprint
import mwparserfromhell
import sqlite3


_print = print
print = pprint.pprint

content = []
# Read the XML file
xml_dir = 'xml_data'
files = os.listdir(xml_dir)
sorted_files = sorted(files,key=lambda f: int(f[:2]))

types = defaultdict(set)

info_set = defaultdict(set)
for file in sorted_files[:1]:
    full_path = os.path.join(xml_dir,file)
    # print(full_path)
    with open(full_path, "r") as file:
        # Read each line in the file, readlines() returns a list of lines
        content = file.read()
    parsed = mwparserfromhell.parse(content)
    templates = parsed.filter_templates()
    for t in templates:
        if 'infobox' in str(t.name).lower():
            print(t.params[0].partition('='))
            for k,_,v in [p.partition('=') for p in t.params]:
                if 'video' in k:
                    print(f'{k}: {v}')
        # t_dict = {k:v for k,_,v in [p.partition('=') for p in t.params]}
        # info_set[str(t.name)].update(t_dict.keys())
        
# print(info_set)

# <page>
# <title>Reiðhjól</title>
# <ns>0</ns>
# <id>2</id>
# <revision>
# <id>64462</id>
# <parentid>32332</parentid>
# <timestamp>2020-07-31T15:36:11Z</timestamp>
# <contributor>
# <username>Jóna Kristín</username>
# <id>468</id>
# </contributor>
# <origin>64462</origin>
# <model>wikitext</model>
# <format>text/x-wiki</format>
# <text bytes="521" sha1="23vx79w4is25ewdv39ski7ctc8fahu1" xml:space="preserve">{{Infoboxsign
# |Image1=Takn hjol.JPG
# |texti=Snúið höndunum í hringi fyrir framan ykkur             &lt;!--- lýsið tákninu--&gt;
# |myndunarstadur=Hlutlaust rými
# |handform=A handform lokað
# |ordflokkur=Nafnorð
# |efnisflokkur=Farartæki          &lt;!--- Flokkur  --&gt;
# |tengsl1=Bíll    &lt;!--- Önnur svipuð eða tengd tákn--&gt;
# |tengsl2=Flugvél
# |tengsl3=Lest
# |Image2=Bike.jpg           &lt;!--- Mynd sem tengist merkingu táknsins--&gt;
# |youtube1=V4m5DSdV0as
# |utskyring=Hjól eða reiðhjól er fótknúið farartæki.
# |name=Hjól
# }}</text>
# <sha1>23vx79w4is25ewdv39ski7ctc8fahu1</sha1>
# </revision>
# </page>