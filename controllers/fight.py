# -*- coding: utf-8 -*-
# try something like


def index():
    cat_min = db.category.id.min()
    cat_id= request.vars.category_id or db().select(cat_min).first()[cat_min]
    categories = db(  db.category.id>0  ).select(db.category.ALL)

    db.fight.athlete_blue_id.represent = lambda i,r: db( db.athlete.id == r.athlete_blue_id).select(db.athlete.name).first().as_dict()['name'] if db( db.athlete.id == r.athlete_blue_id).select(db.athlete.name).first() else '..'
    db.fight.athlete_red_id.represent = lambda i,r: db( db.athlete.id == r.athlete_red_id).select(db.athlete.name).first().as_dict()['name'] if db( db.athlete.id == r.athlete_red_id).select(db.athlete.name).first() else '..'
    db.fight.athlete_win_id.represent = lambda i,r: db( db.athlete.id == r.athlete_win_id).select(db.athlete.name).first().as_dict()['name'] if db( db.athlete.id == r.athlete_win_id).select(db.athlete.name).first() else '..'
 
    db.fight.category_id.default = cat_id
    db.fight.category_id.writable=False 
    
    qry=(db.fight.category_id==cat_id)
    grid = SQLFORM.grid(qry,showbuttontext=False)
    return dict(grid=grid,categories = categories, cat_id=cat_id)

def bracket():
    import json
    response.files.append(URL('static','js/jquery.bracket.min.js') )
    response.files.append(URL('static','css/jquery.bracket.min.css') )

    cat_min = db.category.id.min()
    cat_id= request.vars.category_id or db().select(cat_min).first()[cat_min]
    categories = db(  db.category.id>0  ).select(db.category.ALL)
    
    fights = db.executesql ("""
     select coalesce(b2.name,'sinf') as red, coalesce(b1.name,'sinf') as blue 
     from fight a 
     left join athlete b1 on a.athlete_blue_id = b1.id 
     left join athlete b2 on a.athlete_red_id = b2.id
     where a.category_id=%s limit 32

     """%str(cat_id)
     ,as_dict=True)
    #return str(fights)
    return dict(fights=fights,categories = categories, cat_id=cat_id)

def generate_matchs():
    import math
    import random
    mensaje=[]
    categories_count = db(db.category.id>0).count()


    categories = db(db.category.id>0).select(db.category.ALL)

    for cat in categories:
        athletes_count = db( (db.athlete.id>0 )& (db.athlete.category_id == cat.id) ).count()
        athletes = [ rs.id for rs in  db((db.athlete.id>0 )& (db.athlete.category_id == cat.id)).select(db.athlete.id)]
        matchs_count = math.ceil(athletes_count/2.0)
        
        


        def is_divisible(count_):
            val=False
            for v in xrange(5):
                try:
                    num = 2**v
                    tmp = num/count_
                    if tmp == 1:
                        val = True
                        break
                except:
                    pass
            return val

        def is_fight_empty(category_id_):
            val = False
            val = db(db.fight.category_id == category_id_).isempty()
            return val
        
        def pick_athlete():
            val=None
            if len(athletes)>0:
                idx = random.randint(0,len(athletes)-1)
                val= athletes[idx]
                athletes.remove(val)
            return val
            
           
            
        if is_divisible(matchs_count):
            if is_fight_empty(cat.id):
                for i in xrange(int(matchs_count)):
                    db.fight.insert(
                        tournament_id = 1,
                        athlete_blue_id =pick_athlete(),
                        athlete_red_id = pick_athlete(),
                        category_id = cat.id
                        
                    )
                mensaje.append("CARGA CATEGORIA %s OK, %s COMBATES CARGADOS "% (str(B(cat.name)) , str(matchs_count)))
            else:
                mensaje.append("CARGA CATEGORIA %s FALLO POR: EXISTEN COMBATES  YA CARGADOS"% (str(B(cat.name))))
        else:
            mensaje.append("CARGA CATEGORIA %s FALLO POR: CANTIDAD DE ATLETAS NO ES DIVISIBLE ENTRE 2,4,8,16... " % str(B(cat.name)))
    
    
    
    return dict(message=mensaje)

