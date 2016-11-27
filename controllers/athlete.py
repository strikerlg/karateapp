# -*- coding: utf-8 -*-
# try something like
def index(): 

    cat_min = db.category.id.min()
    cat_id= request.vars.category_id or db().select(cat_min).first()[cat_min]

    gender_default = request.vars.gender_default or 1
    gender = db(  db.gender.id>0  ).select(db.gender.ALL)
    categories = db( ( db.category.id>0) & (db.category.gender_id== gender_default ) ).select(db.category.ALL)
    db.athlete.photo.represent = lambda r,i: IMG( _width="80px",_heigth="80px",_src= URL('default', 'download', args=[i.photo]),_alt="de" )
    #links=[lambda r: IMG( _width="80px",_heigth="80px",_src= URL('default', 'download', args=[r.photo]),_alt="de" )]

    db.athlete.category_id.writable=False 
    qry=( (db.athlete.category_id==cat_id) & (db.athlete.gender_id== gender_default ))
    grid=SQLFORM.grid(qry,showbuttontext=False)
    return dict(grid=grid, categories = categories, cat_id=cat_id, gender_default = gender_default, gender = gender)

def populate():
    from gluon.contrib.populate import populate
    populate(db.athlete,100)
