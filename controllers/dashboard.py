# -*- coding: utf-8 -*-
# try something like
def index(): 
    
    response.files.append(URL('static','js/shortcut.js') )
    return dict(message="hello from dashboard.py")
    
def refresh():
    fight_id = request.vars.fight_id or 0
    max_ = db.fight_json.id.max()
    record = db(db.fight_json.fight_id==fight_id).select().first()[max_]
    return str(record)
    
