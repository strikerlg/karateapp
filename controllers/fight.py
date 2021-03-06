# -*- coding: utf-8 -*-
# try something like

@auth.requires_login()
def index():
    cat_min = db.category.id.min()
    subcat_min = db.subcategory.id.min()
    gender_default = request.vars.gender_default or 1
    
    cat_id= request.vars.category_id or db(db.category.gender_id==gender_default).select(cat_min).first()[cat_min]
    
    subcat_default = request.vars.subcat_default or db(db.subcategory.category_id==cat_id).select(subcat_min).first()[subcat_min]
    nu_phase_default = request.vars.nu_phase or 1
    genders = db(  db.gender.id>0  ).select(db.gender.ALL)
    categories = db(  (db.category.id>0) & (db.category.gender_id == gender_default)  ).select(db.category.ALL)
    subcategories = db( (db.subcategory.id>0) & (db.subcategory.category_id==cat_id) ).select(db.subcategory.ALL)
    def get_photo_blue(i,r):
      dojo = ''
      try:
         rs = db( db.athlete.id == r.athlete_blue_id).select(db.athlete.dojo_id).render(0) 
         dojo = rs.dojo_id
      except:
         pass      
      txt = db( db.athlete.id == r.athlete_blue_id).select(db.athlete.name).first().as_dict()['name'] if db( db.athlete.id == r.athlete_blue_id).select(db.athlete.name).first() else '..'
      url_photo = db( db.athlete.id == r.athlete_blue_id).select(db.athlete.photo).first().as_dict()['photo'] if db( db.athlete.id == r.athlete_blue_id).select(db.athlete.name).first() else None
      photo =   IMG( _width="60px",_heigth="60px",_src= URL('default', 'download', args=[url_photo]),_alt='' )
      if url_photo is None:
       photo =   IMG( _width="60px",_heigth="60px",_src= URL('static', 'images/nophoto.jpg', args=[url_photo]),_alt='')

      return DIV(photo, txt,BR(),STRONG(dojo),_style="color:#0000ff;") 

    def get_photo_red(i,r):
      dojo = ''
      try:
         rs = db( db.athlete.id == r.athlete_red_id).select(db.athlete.dojo_id).render(0) 
         dojo = rs.dojo_id
      except:
         pass

      
      txt = db( db.athlete.id == r.athlete_red_id).select(db.athlete.name).first().as_dict()['name'] if db( db.athlete.id == r.athlete_red_id).select(db.athlete.name).first() else '..'
      url_photo = db( db.athlete.id == r.athlete_red_id).select(db.athlete.photo).first().as_dict()['photo'] if db( db.athlete.id == r.athlete_red_id).select(db.athlete.name).first() else None
      photo = IMG( _width="60px",_heigth="60px",_src= URL('default', 'download', args=[url_photo]),_alt='' )
      if url_photo is None:
       photo =   IMG( _width="60px",_heigth="60px",_src= URL('static', 'images/nophoto.jpg', args=[url_photo]),_alt='')
      return DIV(photo, txt,BR(),STRONG(dojo) ,_style="color:#ff0000;")       
    #db.athlete.photo.represent = lambda r,i: IMG( _width="80px",_heigth="80px",_src= URL('default', 'download', args=[i.photo]),_alt="de" )
    db.fight.athlete_blue_id.represent = lambda i,r: get_photo_blue(i,r)
    db.fight.athlete_red_id.represent = lambda i,r: get_photo_red(i,r)
    db.fight.athlete_win_id.represent = lambda i,r: db( db.athlete.id == r.athlete_win_id).select(db.athlete.name).first().as_dict()['name'] if db( db.athlete.id == r.athlete_win_id).select(db.athlete.name).first() else '..'
 
    db.fight.category_id.default = cat_id
    db.fight.category_id.writable=False 
    max_phase = db.fight.phase.max()
    qry=( (db.fight.subcategory_id==subcat_default )  )
    max_phase = db(qry).select(max_phase).first()[max_phase] or 0

    qry=( (db.fight.subcategory_id==subcat_default) & (db.fight.phase==nu_phase_default)) 

    fields = (db.fight.fight_num, 
              db.fight.gender_id,
              db.fight.category_id,
              db.fight.subcategory_id,
              db.fight.tatami_id,
              db.fight.athlete_blue_id, 
              db.fight.athlete_red_id,
              db.fight.athlete_win_id, 
              db.fight.blue_score,
              db.fight.red_score
              )

    grid = SQLFORM.grid(qry,showbuttontext=False, fields = fields, deletable=False, create=False, searchable=False)
    return dict(grid=grid,categories = categories, cat_id=cat_id, 
        max_phase = max_phase, nu_phase_default = nu_phase_default
        ,genders= genders , gender_default=gender_default, subcategories = subcategories, subcat_default = subcat_default)


@auth.requires_login()
def tatami():
    #cat_min = db.category.id.min()
    #cat_id= request.vars.category_id or db(db.category.gender_id==gender_default).select(cat_min).first()[cat_min]
    tatami_default = request.vars.tatami_id or '0'
    

    tatamis = db(  db.tatami.id>0  ).select(db.tatami.ALL)
    #categories = db(  (db.category.id>0) & (db.category.gender_id == gender_default)  ).select(db.category.ALL)

    def get_photo_blue(i,r):
      dojo = ''
      try:
         rs = db( db.athlete.id == r.athlete_blue_id).select(db.athlete.dojo_id).render(0) 
         dojo = rs.dojo_id
      except:
         pass      
      txt = db( db.athlete.id == r.athlete_blue_id).select(db.athlete.name).first().as_dict()['name'] if db( db.athlete.id == r.athlete_blue_id).select(db.athlete.name).first() else '..'
      url_photo = db( db.athlete.id == r.athlete_blue_id).select(db.athlete.photo).first().as_dict()['photo'] if db( db.athlete.id == r.athlete_blue_id).select(db.athlete.name).first() else None
      photo =   IMG( _width="60px",_heigth="60px",_src= URL('default', 'download', args=[url_photo]),_alt='' )
      if url_photo is None or len(url_photo)<1:
       photo =   IMG( _width="60px",_heigth="60px",_src= URL('static', 'images/nophoto.jpg', args=[url_photo]),_alt='')

      return DIV(photo, txt,BR(),STRONG(dojo),_style="color:#0000ff;") 

    def get_photo_red(i,r):
      dojo = ''
      try:
         rs = db( db.athlete.id == r.athlete_red_id).select(db.athlete.dojo_id).render(0) 
         dojo = rs.dojo_id
      except:
         pass

      
      txt = db( db.athlete.id == r.athlete_red_id).select(db.athlete.name).first().as_dict()['name'] if db( db.athlete.id == r.athlete_red_id).select(db.athlete.name).first() else '..'
      url_photo = db( db.athlete.id == r.athlete_red_id).select(db.athlete.photo).first().as_dict()['photo'] if db( db.athlete.id == r.athlete_red_id).select(db.athlete.name).first() else None
      photo = IMG( _width="60px",_heigth="60px",_src= URL('default', 'download', args=[url_photo]),_alt='' )
      if url_photo is None or len(url_photo)<1:
       photo =   IMG( _width="60px",_heigth="60px",_src= URL('static', 'images/nophoto.jpg', args=[url_photo]),_alt='')
      return DIV(photo, txt,BR(),STRONG(dojo) ,_style="color:#ff0000;")       
    #db.athlete.photo.represent = lambda r,i: IMG( _width="80px",_heigth="80px",_src= URL('default', 'download', args=[i.photo]),_alt="de" )
    db.fight.athlete_blue_id.represent = lambda i,r: get_photo_blue(i,r)
    db.fight.athlete_red_id.represent = lambda i,r: get_photo_red(i,r)
    db.fight.athlete_win_id.represent = lambda i,r: db( db.athlete.id == r.athlete_win_id).select(db.athlete.name).first().as_dict()['name'] if db( db.athlete.id == r.athlete_win_id).select(db.athlete.name).first() else '..'
 
    

    qry=( (db.fight.tatami_id==tatami_default) )
    if tatami_default == '0':
       qry=( (db.fight.tatami_id==None) )

    fields = (db.fight.phase,
              db.fight.fight_num, 
              db.fight.gender_id,
              db.fight.category_id,
              db.fight.subcategory_id,
              db.fight.tatami_id,
              db.fight.athlete_blue_id, 
              db.fight.athlete_red_id,
              db.fight.athlete_win_id, 
              db.fight.blue_score,
              db.fight.red_score
              )

    grid = SQLFORM.grid(qry,showbuttontext=False, fields = fields , deletable=False, create=False)
    return dict(grid=grid,tatamis=tatamis, tatami_default = tatami_default)

@auth.requires_login()
def bracket():
    import json
    response.files.append(URL('static','js/brackets.min.js') )

    cat_min = db.category.id.min()
    subcat_min = db.subcategory.id.min()
    gender_default = request.vars.gender_default or 1
    
    cat_id= request.vars.category_id or db(db.category.gender_id==gender_default).select(cat_min).first()[cat_min]
    
    subcat_default = request.vars.subcat_default or db(db.subcategory.category_id==cat_id).select(subcat_min).first()[subcat_min]
    nu_phase_default = request.vars.nu_phase or 1
    genders = db(  db.gender.id>0  ).select(db.gender.ALL)
    categories = db(  (db.category.id>0) & (db.category.gender_id == gender_default)  ).select(db.category.ALL)
    subcategories = db( (db.subcategory.id>0) & (db.subcategory.category_id==cat_id) ).select(db.subcategory.ALL)
    
    max_phase = db.fight.phase.max()
    qry=( (db.fight.subcategory_id==subcat_default )   )
    max_phase = db(qry).select(max_phase).first()[max_phase] or 0


    fights = db.executesql ("""
     select coalesce(b2.name,'.') as red, coalesce(b1.name,'.') as blue 
     from fight a 
     left join athlete b1 on a.athlete_blue_id = b1.id 
     left join athlete b2 on a.athlete_red_id = b2.id
     where a.subcategory_id=%s and phase=1 order by a.id limit 32

     """%str(subcat_default)
     ,as_dict=True)


    results = db.executesql ("""
   select
     a.id,
     phase,
     fight_num,coalesce(athlete_red_id,0) as red_id,coalesce(b1.name,'') as blue_name, 
     coalesce(athlete_blue_id,0) as blue_id,coalesce(b2.name,'') as red_name,
     finished,
     coalesce(athlete_win_id) as athlete_win_id,
     coalesce(w1.name,'') as win_name,
     coalesce(red_score) as red, 

     coalesce(blue_score) as blue 
     from fight a 
     left join athlete b1 on a.athlete_blue_id = b1.id 
     left join athlete b2 on a.athlete_red_id = b2.id
     left join athlete w1 on a.athlete_win_id = w1.id
     where a.subcategory_id=%s order by 1,2
    """%str(subcat_default)
    ,as_dict=True)

    #return str(fights)
    return dict(fights=fights,genders= genders , gender_default=gender_default, categories = categories, cat_id=cat_id, results=results,max_phase = max_phase,subcategories = subcategories, subcat_default = subcat_default)
@auth.requires_login()
def generate():
    import math
    import random
    mensaje=[]
    subcat_default = request.vars.subid or 0
    genders = db(db.gender.id>0).select(db.gender.ALL)
    for gender in genders:
        #categories_count = db( (db.category.id>0) ).count()
        subcategories = db((db.subcategory.id>0) 
                        & (db.subcategory.id==subcat_default)
                        & (db.subcategory.category_id==db.category.id) 
                        & (db.category.gender_id == gender.id)).select(db.category.ALL, db.subcategory.ALL)
        #gender =  db(db.gender.id>0).select(db.gender.ALL)
        perfect_match = [2,4,8,16,32,64]
        

        for rscat in subcategories:
            phase = 1
            athletes_count = db((db.athlete.gender_id==gender.id  ) & (db.athlete.id>0 ) & (db.athlete.subcategory_id == rscat.subcategory.id) ).count()
            athlete_by_dojo=dict()
            for athlete in db((db.athlete.gender_id==gender.id  )& (db.athlete.id>0  )& (db.athlete.subcategory_id == rscat.subcategory.id)).select(db.athlete.id, db.athlete.dojo_id, orderby='<random>'):
                if not athlete_by_dojo.has_key(athlete.dojo_id):
                    athlete_by_dojo[ athlete.dojo_id ] = [athlete.id]
                else:
                    athlete_by_dojo[ athlete.dojo_id ].append(athlete.id)
            matchs_count = math.ceil(athletes_count/2.0)
            
            val_ = 0 # Calculo de las rondas
            for v in perfect_match:
                val_ = matchs_count / v
                if val_ == 1:

                 val_ =v
                 break
                elif val_ <1:

                 val_ = v
                 break   
            print val_
            diff_ = val_*2 - athletes_count
            for i in xrange(diff_):
                if not athlete_by_dojo.has_key(-1):
                    athlete_by_dojo[ -1 ] = [-1*(i+1)]
                else:
                    athlete_by_dojo[ -1 ].append(-1*(i+1))              

            print athlete_by_dojo
            athletes= []

            for did in athlete_by_dojo.keys():
                for idx,athlete in enumerate(athlete_by_dojo[did]):
                    athletes.append( (athlete,idx) )
            #return str(athletes)
            athletes.sort(key=lambda x:x[1])
            #return str(athletes)
            athletes = [ a[0] for a in athletes]

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

            def is_fight_empty(subcategory_id_):
                val = False
                val = db( (db.fight.subcategory_id == subcategory_id_ )  ).isempty() 
                return val
            
            def pick_athlete():
                val=None
                if len(athletes)>0:
                    idx = 0#random.randint(0,len(athletes)-1)
                    val= athletes[idx]
                    athletes.remove(val)
                return val
                
      


            if is_fight_empty(rscat.subcategory.id):
                if athletes_count>0:
                    for i in xrange(int(val_)):
                        db.fight.insert(
                            tournament_id = 1,
                            phase = phase,
                            fight_num = i+1,
                            athlete_blue_id =pick_athlete(),
                            athlete_red_id = pick_athlete(),
                            category_id = rscat.subcategory.category_id,
                            subcategory_id = rscat.subcategory.id,
                            gender_id = gender.id
                            
                        )

                    while val_%2 == 0 and val_>0:
                         val_ = val_/2
                         phase = phase+1
                         for i in xrange(int(val_)):
                            import math
                            next_combate = math.ceil(i+1/2.0)
                            db.fight.insert(
                                tournament_id = 1,
                                phase = phase,
                                fight_num = i+1,
                                athlete_blue_id =None,
                                athlete_red_id = None,
                                category_id = rscat.subcategory.category_id,
                                subcategory_id = rscat.subcategory.id,
                                gender_id = gender.id
                            
                             )
                         

                    mensaje.append( '<div class="alert alert-success" role="alert">'+ gender.name + " CARGA CATEGORIA %s (%s) OK, %s COMBATES CARGADOS </div>"% (str(B(rscat.category.name)), str(B(rscat.subcategory.name ) ) , str(matchs_count)))
                else:
                    mensaje.append( '<div class="alert alert-danger" role="alert">'+ gender.name + " CARGA CATEGORIA %s (%s) FALLO POR: NO HAY ATLETAS </div>"% (  str(B(rscat.category.name ) ), str(B(rscat.subcategory.name ) )   )  )
            else:
                mensaje.append( '<div class="alert alert-danger" role="alert">'+gender.name + " CARGA CATEGORIA %s (%s) FALLO POR: EXISTEN COMBATES  YA CARGADOS </div>"% (str(B(rscat.category.name) ), str(B(rscat.subcategory.name ) ) ))


    
    
    return dict(grid=mensaje)
def is_fight_empty(subcategory_id_):
    val = False
    val = db( (db.fight.subcategory_id == subcategory_id_ )  ).isempty() 
    return val
@auth.requires_login()
def generate_matchs():
    
    sql = """
    select e.name as circuito,d.name as genero,c.name as categoria, b.name as subcategoria,b.id as subcat_id,
  c.id as category_id,d.id as gender_id,
  count(*) as inscritos from athlete a
    left join subcategory b on (a.subcategory_id=b.id)
    left join category c on (a.category_id=c.id)
    left join gender d on (c.gender_id=d.id)
  left join circuit e on (a.circuit_id=e.id)
    group by 1,2 ,3,4,5,6,7
    order by 1,2 ,3 ,4  ,5,6,7
    """
    datos=[]
    registro=[ TR(TH('CIRCUITO'),TH('GENERO'),TH('CATEGORIA'),TH('SUBCATEGORIA'),TH('INSCRITOS'),TH('ACCION'),TH('TATAMI') ) ]

    rs = db.executesql(sql,as_dict=True)
    fila2=0


    for r in rs:
        
        btn1 = A('Generar Llave',_class="btn btn-primary btn-xs",_href=URL('fight','generate',vars=dict(subid=r['subcat_id'])))
        btn2 = A('Ver Llave',_class="btn btn-info btn-xs",_href=URL('fight','bracket',vars=dict(subcat_default=r['subcat_id'] , category_id= r['category_id'],gender_default=r['gender_id'])) )
        registro.append( TR (TD(r['circuito']),TD(r['genero']), TD(r['categoria']),TD(r['subcategoria']),TD(r['inscritos']), TD(    btn1 if is_fight_empty(r['subcat_id']) else btn2)   ) )
    datos.append(registro)
    return  dict(grid = TABLE(registro,_class="table"))
    
    
