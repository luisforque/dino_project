import time
import datetime
import os, os.path
import glob
import json
from mysql import connector

#query_statement = f"SELECT * FROM {table_name}"
#query_output = pd.read_sql(query_statement, conn)

TARGET_JSON_LOCATION = f'./data_lake/json/'
DESCRIPTION_MAX_SIZE = 999

def get_list_of_dinos():
    json_list = []

    subfolders = [ f.path for f in os.scandir(TARGET_JSON_LOCATION) if f.is_dir() ]
    for subfolder in subfolders:
        files = [f for f in glob.glob(f"{subfolder}/*.json")]
        for file in files:
            with open(file) as dino_file:
                json_list.append(json.load(dino_file))

    return json_list

def insert_type(dino_json, cursor, database):
    cursor.execute(f'''INSERT INTO Type (type_name) VALUES ("{dino_json['type']}");''')
    database.commit()
    return cursor.lastrowid

def get_type_id(dino_json, cursor):
    cursor.execute(f'''SELECT type_id FROM Type where type_name = "{dino_json['type']}";''')
    result = cursor.fetchone()
    return False if result == None else result[0]

def insert_diet(dino_json, cursor, database):
    cursor.execute(f'''INSERT INTO Diet (diet_name) VALUES ("{dino_json['diet']}");''')
    database.commit()
    return cursor.lastrowid

def get_diet_id(dino_json, cursor):
    cursor.execute(f'''SELECT diet_id FROM Diet where diet_name = "{dino_json['diet']}";''')
    result = cursor.fetchone()
    return False if result == None else result[0]

def insert_era(dino_json, cursor, database):
    cursor.execute(f'''INSERT INTO Era (era_name) VALUES ("{dino_json['era']}");''')
    database.commit()
    return cursor.lastrowid

def get_era_id(dino_json, cursor):
    cursor.execute(f'''SELECT era_id FROM Era where era_name = "{dino_json['era']}";''')
    result = cursor.fetchone()
    return False if result == None else result[0]

def insert_country(dino_json, cursor, database):
    cursor.execute(f'''INSERT INTO Country (country_name) VALUES ("{dino_json['country']}");''')
    database.commit()
    return cursor.lastrowid

def get_country_id(dino_json, cursor):
    cursor.execute(f'''SELECT country_id FROM Country where country_name = "{dino_json['country']}";''')
    result = cursor.fetchone()
    return False if result == None else result[0]

def insert_name(dino_json, cursor, database):
    try: 
        cursor.execute(f'''INSERT INTO Name (name, pronunciation, meaning) VALUES \
                    ("{dino_json['name']}", "{dino_json['name_pronunciation']}", "{dino_json['name_meaning']}");''')
        database.commit()
    except connector.errors.IntegrityError:
        # expected if the name already exists
        print(f"Tried to add {dino_json['name']} again!")
        pass

def insert_dinosaur(dino_json, cursor, type_id, diet_id, country_id, era_id, database):
    try: 
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        description = None if dino_json['description'] == None else dino_json['description'][0:DESCRIPTION_MAX_SIZE]
        cursor.execute(f'''INSERT INTO Dinosaur (size, image, discovered, description, \
                    name, type_id, diet_id, era_id, country_id, created_at) VALUES \
                        ({float(dino_json['size'][:-1])}, "{dino_json['image']}", \
                        {int(dino_json['discovered'])}, "{description}", \
                        "{dino_json['name']}", {type_id}, {diet_id}, {era_id}, \
                        {country_id}, "{timestamp}");''')
        database.commit()
    except connector.errors.IntegrityError:
        # expected if the name already exists
        pass

def load_dinosaurs():
    print(f"Get list of dinos")
    dino_json_list = get_list_of_dinos()
    print(f"Finished get list of dinos")

    try:
        with connector.connect(host = "localhost", user = "user", password = "password", 
                               database = "dinosaurs", auth_plugin='mysql_native_password') as database:
            print(database)
            cursor = database.cursor()

            for dino_json in dino_json_list:
                print(f"Inserting {dino_json['name']}")
                type_id = get_type_id(dino_json, cursor)
                if not type_id:
                    type_id = insert_type(dino_json, cursor, database)
                    
                diet_id = get_diet_id(dino_json, cursor)
                if not diet_id:
                    diet_id = insert_diet(dino_json, cursor, database)
                    
                country_id = get_country_id(dino_json, cursor)
                if not country_id:
                    country_id = insert_country(dino_json, cursor, database)
                    
                era_id = get_era_id(dino_json, cursor)
                if not era_id:
                    era_id = insert_era(dino_json, cursor, database)

                insert_name(dino_json, cursor, database)
                insert_dinosaur(dino_json, cursor, type_id, diet_id, country_id, era_id, database)

        database.close()

    except connector.Error as e:
        print(e)

load_dinosaurs()

# insert into tab2 (id_customers, value)
# values ((select id from tab1 where customers='john'), 'alfa');