import sqlite3
import os
import json

db_name = 'sign.sqlite'

with open('signwiki-json-dump.json') as f:
    data = json.loads(f.read())

def initdb():
    if os.path.exists(db_name):
        os.remove(db_name)
    with open('signwiki-db-schema.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    with sqlite3.connect(db_name) as db:
        db.executescript(sql_script)

import re
def split_by_number(input_str):
    match = re.search("\d", input_str)

    if match:
        index = match.start()
        val = input_str[:index]
        num = input_str[index:]
        return val, num
        # print("First part:", first_part)
        # print("Second part:", second_part)
    else:
        return input_str, ''
        # print("No numbers found in string")


def insert_signs():
    signs = set()
    for entry in data:
        for key in entry.keys():
            if 'youtube' in key:
                phrase = entry['title']
                description = entry.get('texti',None)
                munnhreyfing = entry.get('munnhreyfing',None)
                islenska = entry.get('islenska',None)
                id = entry.get('signwiki_id',None)
                myndunarstadur = entry.get('myndunarstadur', None)
                ordflokkur = entry.get('ordflokkur',None)
                handform = entry.get('handform',None)
                taknmal = entry.get('taknmal',None)
                signs.add((phrase,description,munnhreyfing,islenska,id, myndunarstadur, ordflokkur,handform,taknmal))
                # print(f'{key}\t{entry[key]}')
    with sqlite3.connect(db_name) as db:
        db.executemany('''
        INSERT OR IGNORE
        INTO sign(phrase,description,munnhreyfing,islenska,id, myndunarstadur, ordflokkur,handform,taknmal)
        SELECT tmp.*, ?, ?, ?, ?, ?, ?, ?,? FROM (SELECT ?) as tmp
        WHERE NOT EXISTS (
            SELECT phrase FROM sign WHERE phrase = ?
        ) LIMIT 1
        ''',[[description, munnhreyfing, islenska, id, myndunarstadur, ordflokkur, handform, taknmal, phrase, phrase] for phrase, description, munnhreyfing, islenska, id, myndunarstadur, ordflokkur, handform, taknmal in signs])


def insert_sign_related():
    all_sign_related = []
    for entry in data:
        sign = {'phrase':entry['title'],'related':[]}
        for key in entry.keys():
            if 'tengsl' in key:
                rank = 0
                val, num = split_by_number(key)
                if num:
                    rank = num
                sign['related'].append({'phrase':entry[key],'rank':rank})
                all_sign_related.append((rank,entry['title'],entry[key]))

    with sqlite3.connect(db_name) as db:
        db.executemany('''
        INSERT OR IGNORE
        INTO sign_related(sign_id,related_id,rank)
        select sign.id, related.id, ?
        from sign
        join sign as related
        where sign.phrase = ?
        and related.phrase = ?
        ''',[[rank, sign_phrase, related_phrase] for rank, sign_phrase, related_phrase in all_sign_related])


def insert_sign_video():
    all_sign_video = []
    for entry in data:
        for key in entry.keys():
            if 'youtube' in key:
                rank = 0
                val, num = split_by_number(key)
                if num:
                    rank = num
                all_sign_video.append((entry[key],rank,entry['title']))
    # breakpoint()
    with sqlite3.connect(db_name) as db:
        db.executemany('''
        INSERT OR IGNORE
        INTO sign_video(sign_id,video_id,rank)
        select sign.id, ?, ?
        from sign
        where sign.phrase = ?
        ''',[[video_id, rank, sign_phrase] for video_id, rank, sign_phrase in all_sign_video])

def insert_sign_fts():
    with sqlite3.connect(db_name) as db:
        db.execute('''
        INSERT INTO sign_fts(id,phrase,related_signs)
        SELECT sign.id as id,
        sign.phrase as phrase,
        GROUP_CONCAT
        (related.phrase) as related_signs
        FROM sign
        JOIN sign_related
        ON sign.id = sign_related.sign_id
        JOIN sign as related
        ON sign_related.related_id = related.id
        GROUP BY sign.id
        ''')

def insert_myndunarstadur():
    '''
    CREATE TABLE IF NOT EXISTS "myndunarstadur"(
        "id" INTEGER PRIMARY KEY,
        "text" TEXT NOT NULL
    );
    '''
    # global myndunarstadir
    myndunarstadir = set()
    for entry in data:
        for key in entry.keys():
            if 'myndunarstadur' in key:
                myndunarstadir.add(entry[key])
    with sqlite3.connect(db_name) as db:
        db.executemany('INSERT INTO myndunarstadur(text) VALUES (?)',[[myndunarstadur] for myndunarstadur in myndunarstadir])
    # print(myndunarstadir)

def insert_sign_myndunarstadur():
    '''
    CREATE TABLE IF NOT EXISTS "sign_myndunarstadur"(
        "sign_id" INTEGER,
        "myndunarstadur_id" INTEGER,
        PRIMARY KEY("sign_id","myndunarstadur_id"),
        FOREIGN KEY("sign_id") REFERENCES "sign"("id"),
        FOREIGN KEY("myndunarstadur_id") REFERENCES "myndunarstadur"("id")
    );
    '''
    all_sign_myndunarstadir = set()
    for entry in data:
        for key in entry.keys():
            if 'myndunarstadur' in key:
                phrase = entry['title']
                myndunarstadur = entry[key]
                all_sign_myndunarstadir.add((phrase,myndunarstadur))
    # breakpoint()
    with sqlite3.connect(db_name) as db:
        db.executemany('''
                        INSERT INTO sign_myndunarstadur(sign_id,myndunarstadur_id)
                        SELECT sign.id, myndunarstadur.id
                        FROM sign
                        LEFT JOIN
                        myndunarstadur
                        WHERE sign.phrase = ?
                        AND myndunarstadur.text = ?
                        ''',
                        [[phrase,myndunarstadur] for phrase,myndunarstadur in all_sign_myndunarstadir])

def insert_ordflokkur():
    '''
    CREATE TABLE IF NOT EXISTS "ordflokkur"(
        "id" INTEGER PRIMARY KEY,
        "text" TEXT NOT NULL
    );
    '''
    ordflokkar = set()
    for entry in data:
        for key in entry.keys():
            if 'ordflokkur' in key:
                # phrase = entry['title']
                ordflokkur = entry[key]
                ordflokkar.add(ordflokkur)
    with sqlite3.connect(db_name) as db:
        db.executemany('INSERT INTO ordflokkur(text) VALUES (?)',[[ordflokkur] for ordflokkur in ordflokkar])
    
def insert_sign_ordflokkur():
    '''
    CREATE TABLE IF NOT EXISTS "sign_ordflokkur"(
        "sign_id" INTEGER,
        "ordflokkur_id" INTEGER,
        "rank" INTEGER,
        PRIMARY KEY("sign_id","ordflokkur_id"),
        FOREIGN KEY("sign_id") REFERENCES "sign"("id"),
        FOREIGN KEY("ordflokkur_id") REFERENCES "ordflokkur"("id")
    );
    '''
    sign_ordflokkar = set()
    for entry in data:
        for key in entry.keys():
            if 'ordflokkur' in key:
                phrase = entry['title']
                ordflokkur = entry[key]
                sign_ordflokkar.add((phrase,ordflokkur))
    with sqlite3.connect(db_name) as db:
        db.executemany('''
                        INSERT INTO sign_ordflokkur(sign_id,ordflokkur_id)
                        SELECT sign.id, ordflokkur.id
                        FROM sign
                        LEFT JOIN
                        ordflokkur
                        WHERE sign.phrase = ?
                        AND ordflokkur.text = ?
                        ''',
                        [[phrase,ordflokkur] for phrase,ordflokkur in sign_ordflokkar])
        

def insert_efnisflokkur():
    '''
    CREATE TABLE IF NOT EXISTS "efnisflokkur"(
        "id" INTEGER PRIMARY KEY,
        "text" TEXT NOT NULL
    );
    '''
    efnisflokkar = set()
    for entry in data:
        for key in entry.keys():
            if 'efnisflokkur' in key:
                
                # phrase = entry['title']
                efnisflokkur = entry[key]
                efnisflokkar.add(efnisflokkur)
    with sqlite3.connect(db_name) as db:
        db.executemany('INSERT INTO efnisflokkur(text) VALUES (?)',[[efnisflokkur] for efnisflokkur in efnisflokkar])
def insert_sign_efnisflokkur():
    '''
    CREATE TABLE IF NOT EXISTS "sign_efnisflokkur"(
        "sign_id" INTEGER,
        "efnisflokkur_id" INTEGER,
        "rank" INTEGER,
        PRIMARY KEY("sign_id","efnisflokkur_id"),
        FOREIGN KEY("sign_id") REFERENCES "sign"("id"),
        FOREIGN KEY("efnisflokkur_id") REFERENCES "efnisflokkur"("id")
    );
    '''
    sign_efnisflokkar = set()
    for entry in data:
        for key in entry.keys():
            if 'efnisflokkur' in key:
                rank = 0
                val, num = split_by_number(key)
                if num:
                    rank = num
                phrase = entry['title']
                efnisflokkur = entry[key]
                sign_efnisflokkar.add((rank,phrase,efnisflokkur))
    with sqlite3.connect(db_name) as db:
        db.executemany('''
                        INSERT INTO sign_efnisflokkur(sign_id,efnisflokkur_id, rank)
                        SELECT sign.id, efnisflokkur.id, ?
                        FROM sign
                        LEFT JOIN
                        efnisflokkur
                        WHERE sign.phrase = ?
                        AND efnisflokkur.text = ?
                        ''',
                        [[rank,phrase,efnisflokkur] for rank,phrase,efnisflokkur in sign_efnisflokkar])
        

initdb()
insert_signs()
insert_sign_related()
insert_sign_video()
# insert_myndunarstadur()
# insert_sign_myndunarstadur()
# insert_ordflokkur()
# insert_sign_ordflokkur()
insert_efnisflokkur()
insert_sign_efnisflokkur()


def dump_db():
    base_db_name = db_name.split('.sqlite')[0]
    dump_filename = f'{base_db_name}-dump.txt'
    pattern = r'CREATE TABLE.*?;\n'
    os.system(f'sqlite3 {db_name} ".dump" > {dump_filename}')
    with open(dump_filename) as f:
        dump_data = f.read()
    matches = re.findall(pattern,dump_data,re.DOTALL)
    dump_table_data = '\n'.join(matches)
    file_without_table_data = re.sub(pattern,'',dump_data,flags=re.DOTALL)
    with open(f'{base_db_name}_tables.txt', 'w') as f:
        f.write(dump_table_data)
    with open(f'{base_db_name}_db_data.txt','w') as f:
        f.write(file_without_table_data)

    # breakpoint()
dump_db()
# insert_sign_fts()
