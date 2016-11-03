# -*- coding: utf-8 -*-
# try something like
def index(): 
    fight_id = request.vars.match_id or redirect(URL('default','matchs'))
    Athlete_red  =  db.athlete.with_alias('athlete_red')
    Athlete_blue  =  db.athlete.with_alias('athlete_blue')
    matchs = db(  db.fight.id==fight_id).select( db.fight.ALL, Athlete_red.ALL, Athlete_blue.ALL,
                                                            left=(  Athlete_red.on(Athlete_red.id == db.fight.athlete_red_id),
                                                                      Athlete_blue.on(Athlete_blue.id == db.fight.athlete_blue_id )    
                                                            )).first()
    response.files.append(URL('static','js/shortcut.js') )
    
    #return str(matchs)
    return dict(record=matchs)
    
def refresh():
    fight_id = request.vars.fight_id or 0
    max_ = db.fight_json.id.max()
    record = db(db.fight_json.fight_id==fight_id).select().first()[max_]
    return str(record)
    
    
def save_fight_log():
    import json
    data = request.vars.data or '{s:1}'
    fight = json.loads(data)
    db.fight_json.insert(fight_id=fight['fight_id'], data_log = data)
    return str(fight['fight_id'])
