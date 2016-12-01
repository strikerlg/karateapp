# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
def index(): 
    fight_id = request.vars.match_id or redirect(URL('default','matchs'))
    Athlete_red  =  db.athlete.with_alias('athlete_red')
    Athlete_blue  =  db.athlete.with_alias('athlete_blue')
    matchs = db(  db.fight.id==fight_id).select( db.fight.ALL, Athlete_red.ALL, Athlete_blue.ALL,
                                                            left=(  Athlete_red.on(Athlete_red.id == db.fight.athlete_red_id),
                                                                      Athlete_blue.on(Athlete_blue.id == db.fight.athlete_blue_id )    
                                                            )).first()
    response.files.append(URL('static','js/shortcut.js') )
    


    tatami = db(db.tatami.id==matchs.fight.tatami_id).select(db.tatami.ALL).first().as_dict()['name'] if db(db.tatami.id==matchs.fight.tatami_id).select(db.tatami.ALL).first() else 0
    category = db(db.category.id==matchs.fight.category_id).select(db.category.ALL).first()
    #return str(matchs)
    return dict(record=matchs,tatami_name=tatami, category = category)
    
def refresh():
    fight_id = request.vars.fight_id or 0
    max_ = db.fight_json.id.max()
    record = db(db.fight_json.fight_id==fight_id).select().first()[max_]
    return str(record)
    
    
def save_fight_log():
    import json
    data = request.vars.data or '{s:1}'
    fight = json.loads(data)
    #db.fight_json.insert(fight_id=fight['fight_id'], data_log = data)
    return str(fight['fight_id'])
@auth.requires_login()
def save_fight():
    import json
    data = request.vars.data or '{s:1}'
    fight = json.loads(data)

    qry = db(db.fight.id==fight['fight_id'])


    qry.update(
        athlete_win_id = fight['winner_athlete_id'],
        red_score =  fight['red_score'],
        blue_score =  fight['blue_score'],
        finished = True if fight['finished']==1 else False,
        red_c1 =   fight['red_c1'],
        red_c2 =  fight['red_c2'],
        blue_c1 =  fight['blue_c1'],
        blue_c2 =  fight['blue_c2'],

        )
    rs1 = qry.select(db.fight.ALL).first()
    import math
    fight_num = math.ceil(rs1.fight_num/2.0)
    is_blue = False if rs1.fight_num % 2 ==0 else True

    qry2 = db( (db.fight.subcategory_id==rs1.subcategory_id ) & (db.fight.phase==rs1.phase+1) & (db.fight.fight_num== fight_num) ) 
    if is_blue:
        qry2.update(
            athlete_blue_id = fight['winner_athlete_id'],
            )
    else:
        qry2.update(
            athlete_red_id = fight['winner_athlete_id'],          
            )        
    #db.fight_json.insert(fight_id=fight['fight_id'], data_log = data)
    return "XX "+str(fight_num)