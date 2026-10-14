from flask import *
import sqlite3
import hashlib
import app_secrets

app = Flask(__name__)
app.secret_key = app_secrets.flask_session_key


#####################
## GLOBAL VAIABLES ##
#####################
valid_tags = [
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


##############
## DATABASE ##
##############
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("data.db")
        g.db.row_factory = dict_factory

    return g.db

def teardown_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()






def full_user_by_id(id):
    db = get_db()

    command = f"SELECT * FROM users WHERE id=?"
    place = db.execute(command, (id,)).fetchone()

    return place


def full_user_by_name(username):
    db = get_db()

    valid_username = not contains_invalid_char(username)
    user = db.execute(f'''
        SELECT * FROM users 
        WHERE username IS ?
    ''', (username,)
    ).fetchone() if valid_username else None
        
    return user

def select_from_all_users(*columns):
    command_columns = ",".join(columns)

    db = get_db()
    res = db.execute(f"SELECT {command_columns} FROM users")

    return res.fetchall()


def attempt_login(full_user, password):
    try:
        db = get_db()
        correct_pass_hash = full_user["pass_hash"]
        salt = full_user["pass_salt"]

        salted_password = salt+password
        attempt_pass_hash = hashlib.md5(salted_password.encode()).hexdigest()

        return attempt_pass_hash == correct_pass_hash
    except:
        return False


#############
## SESSION ##
#############
def is_admin():
    return session["user"]["is_admin"] if "user" in session else False

def is_loged_in():
    return "user" in session


#########################
## SANITIZE USER INPUT ##
#########################
def contains_invalid_char(text):
    invalid_chars = "\'\"\\_-%\0\b\n\r\t "
    for char in text:
        if char in invalid_chars:
            break
    else:
        return False

    return True


def sanitize_place_data(data):
    new_data = {}
    new_data["name"] = data["name"].strip()
    new_data["address"] = data["address"].strip()
    new_data["maps"] = data["maps"].strip()
    new_data["tags"] = data["tags"].strip()
    new_data["extra_info"] = data["extra_info"].strip()


    try:
        new_data["travel_time_min"] = int(data["travel_time_min"])
    except ValueError:
        new_data["travel_time_min"] = None

    return new_data


def validate_tags(tags):
    for tag in tags:
        if tag not in valid_tags: break
    else:
        return True
    return False


############
## ROUTES ##
############
@app.before_request
def before_request():
    if request.path.startswith("/admin"):
        if not is_admin():
            return redirect(url_for("login"))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", tags=valid_tags)



#################
## AUTH ROUTES ##
#################
@app.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)

        user = full_user_by_name(username)

        success = attempt_login(user, password)

        if success:
            session["user"] = {
                "username": user["username"],
                "is_admin": user["is_admin"]
            }
        
        return redirect(url_for("login"))

    return render_template("/auth/login.html") if not is_loged_in() else redirect(url_for("index"))



@app.route("/auth/logout")
def logout():
    if "user" in session:
        session.pop("user")

    return redirect(url_for("index"))


###################
## PLACES ROUTES ##
###################
@app.route("/admin/places", methods=["GET"])
def places():
    return render_template("admin/places/show.html", places=find_places(filter={}))


@app.route("/admin/places/<int:place_id>/update", methods=["GET", "POST"])
def places_update(place_id):
    if request.method == "POST":
        data = {
            "name":         request.form.get("name", ""),
            "address":      request.form.get("address", ""),
            "maps":         request.form.get("maps", ""),
            "tags":         request.form.get("tags", None),
            "travel_time_min":  request.form.get("travel_time_min", None),
            "extra_info":   request.form.get("extra_info", None),
        }

        data = sanitize_place_data(data)
        db = get_db()
        db.execute('''
            UPDATE places
            SET name=?,
                address=?,
                maps=?,
                tags=?,
                travel_time_min=?,
                extra_info=?
            WHERE id=?
        ''',(
            data["name"],
            data["address"],
            data["maps"],
            data["tags"],
            data["travel_time_min"],
            data["extra_info"],
            place_id
        ))

        db.commit()
        return redirect(request.path)

    full_place = full_place_by_id(place_id)
    return render_template("admin/places/update.html", place=full_place) if full_place else abort(404)


@app.route("/admin/places/create", methods=["GET", "POST"])
def places_create():

    if request.method == "POST":
        data = {
            "name":         request.form.get("name", ""),
            "address":      request.form.get("address", ""),
            "maps":         request.form.get("maps", ""),
            "tags":         request.form.get("tags", None),
            "travel_time_min": request.form.get("travel_time_min", None),
            "extra_info":   request.form.get("extra_info", None),
        }
        data = sanitize_place_data(data)

        db = get_db()
        db.execute('''
            INSERT INTO places
            (name, address, maps, tags, travel_time_min, extra_info)
            VALUES (?, ?, ?, ?, ?, ?)
        ''',(
            data["name"],
            data["address"],
            data["maps"],
            data["tags"],
            data["travel_time_min"],
            data["extra_info"],
        ))

        db.commit()

        return redirect(url_for("places"))

    return render_template("admin/places/create.html")


@app.route("/admin/places/<int:place_id>/remove", methods=["POST"])
def places_delete_post(place_id):
    return redirect(url_for("places"))



##################
## USERS ROUTES ##
##################
@app.route("/admin/users", methods=["GET"])
def users():
    users = select_from_all_users("id", "username")
    return render_template("/admin/users/show.html", users=users)


@app.route("/admin/users/<int:user_id>/update", methods=["GET", "POST"])
def users_update(user_id):
    user = full_user_by_id(user_id)
    return render_template("/admin/users/update.html", user=full_user_by_id(user_id))


@app.route("/admin/users/create", methods=["GET", "POST"])
def users_create():
    return render_template("/admin/users/create.html")


@app.route("/admin/users/<int:user_id>/delete", methods=["POST"])
def users_delete_post(user_id):
    return redirect("/")



###################
## OTHER ROUTES  ##
###################
@app.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_file("static/img/logo.ico", mimetype="image/ico")


@app.route("/api/places", methods=["POST"])
def api_places():
    list_inner_html = ""
    data = request.get_json()

    tags = data.get("tags", {})
    sort = data.get("sort", "")
    filter = {
        "tags": tags,
        "sort": sort
    }

    places = find_places(filter)

    return jsonify(render_template("places_list.html", places=places, is_admin=is_admin()))


@app.teardown_request
def teardown_request(exception):
    teardown_db()

####################
## ERROR HANDLERS ##
####################
@app.errorhandler(404)
def handle_bad_request(exception):
    return render_template("error/404.html"), 404


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


