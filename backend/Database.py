from tinydb import TinyDB, Query

db = TinyDB('backend/db.json')


def insert_new_user(name: str):
    db.insert({'name': name})


def get_user_by_name(name: str):
    user = Query()
    result = db.search(user.name == name)

    return result;


