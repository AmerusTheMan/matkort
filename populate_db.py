import sqlite3

tags = [
    "butik",
    "mackor",
    "pasta",
    "sallad",
    "dryck",
    "sushi",
    "snabbmat",
    "café",
    "resturang",
    "kfc",

    "indiskt",
    "kinesiskt",
    "grekiskt",

    "max",
    "burger king",
    "subway",

    "vegitariskt",
    "veganskt"   
]

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect("sqlite.db")
cursor = conn.cursor()
cursor.row_factory = dict_factory

#fetch old data
places = cursor.execute("SELECT * FROM places ORDER BY id").fetchall()
conn.close()


#open new database
conn = sqlite3.connect("instance/data.db")
cursor = conn.cursor()
cursor.row_factory = dict_factory

#delete all data
cursor.execute("DELETE FROM places")
cursor.execute("DELETE FROM tags")
cursor.execute("DELETE FROM users")

# add tags
cursor.executemany(
    "INSERT INTO tags (tag_name) VALUES (?)",
    [(tag,) for tag in tags]
)

#add places
for place in places:
    tags = place["tags"].split(" ")
    
    id = place["id"]
    name = place["name"]
    address = place["address"]
    map = place["maps"]
    travel_time_min = place["travel_time_min"]
    extra_info = place["extra_info"]

    cursor.execute("""
        INSERT INTO places (place_name, address, map_link, travel_time_min, extra_info)
        VALUES (?, ?, ?, ?, ?)
    """,
        (name, address, map, travel_time_min, extra_info)
    )

    #add tagging for place
    for tag in tags:
        if tag == "burger": tag = "burger king"
        if tag == "king": continue

        tag_id = cursor.execute(f"""
            SELECT tag_id FROM tags WHERE tag_name='{tag}'
        """).fetchone()["tag_id"]


        cursor.execute("""
            INSERT INTO places_tags (place_id, tag_id)
            VALUES (?, ?)
        """, (place["id"], tag_id))

conn.commit()
conn.close()