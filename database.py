import json, os

DB = "db.json"

def load():
    if not os.path.exists(DB):
        return {"maps": {}, "stats": {"processed": 0}}
    return json.load(open(DB))

def save(data):
    json.dump(data, open(DB, "w"), indent=4)

def add_map(source, target):
    db = load()
    db["maps"].setdefault(source, [])
    if target not in db["maps"][source]:
        db["maps"][source].append(target)
    save(db)

def remove_map(source, target):
    db = load()
    if source in db["maps"]:
        if target in db["maps"][source]:
            db["maps"][source].remove(target)
    save(db)

def get_targets(source):
    return load()["maps"].get(source, [])

def inc_stats():
    db = load()
    db["stats"]["processed"] += 1
    save(db)