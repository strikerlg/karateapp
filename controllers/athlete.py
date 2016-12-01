# -*- coding: utf-8 -*-
# try something like

@auth.requires_login()
def index(): 

    cat_min = db.category.id.min()
    subcat_min = db.subcategory.id.min()
    
    
    gender_default = 0 if request.vars.gender_default is None else  int(request.vars.gender_default)
    palabra = '' if request.vars.palabra is None else  request.vars.palabra
        
    cat_id= 0 if request.vars.category_id is None else request.vars.category_id
    cat_id=   cat_id  if cat_id!=0 else  db(db.category.gender_id==gender_default).select(cat_min).first()[cat_min]
    cat_id = 0 if cat_id is None else int(cat_id)
    
    subcat_default = 0 if request.vars.subcat_default is None else request.vars.subcat_default
    subcat_default = subcat_default if subcat_default!=0 else db(db.subcategory.category_id==cat_id).select(subcat_min).first()[subcat_min]
    subcat_default = 0 if subcat_default is None else int(subcat_default)
    
    nu_phase_default = request.vars.nu_phase or 1
    genders = db(  db.gender.id>0  ).select(db.gender.ALL)
    categories = db(  (db.category.id>0) & (db.category.gender_id == gender_default)  ).select(db.category.ALL)
    subcategories = db( (db.subcategory.id>0) & (db.subcategory.category_id==cat_id) ).select(db.subcategory.ALL)

    db.athlete.photo.represent = lambda r,i: IMG( _width="80px",_heigth="80px",_src= URL('default', 'download', args=[i.photo]),_alt="de" )
    #links=[lambda r: IMG( _width="80px",_heigth="80px",_src= URL('default', 'download', args=[r.photo]),_alt="de" )]

    db.athlete.category_id.writable=False 


    qrys = []

    qrys.append(db.athlete.id>0 )

    if  gender_default>0:
      qrys.append(db.athlete.gender_id==gender_default )

    if  cat_id>0:
      qrys.append(db.athlete.category_id==cat_id )      
      
    if  cat_id>0 and subcat_default>0:
      qrys.append(db.athlete.subcategory_id==subcat_default ) 
       
    if len(palabra)>0:
      qrys.append(db.athlete.name.contains(palabra, case_sensitive=False))   
    qry = reduce(lambda a, b:(a & b), qrys)


    #qry=( (db.athlete.category_id==cat_id) & (db.athlete.gender_id== gender_default ))
    grid=SQLFORM.grid(qry,showbuttontext=False,searchable=False)
    return dict(grid=grid, palabra=palabra,genders= genders , gender_default=gender_default, categories = categories, cat_id=cat_id,subcategories = subcategories, subcat_default = subcat_default)
def populate():
    return ".."
    from gluon.contrib.populate import populate
    populate(db.athlete,100)
