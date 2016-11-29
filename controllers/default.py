# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

@auth.requires_login()
def index():

    #cat_min = db.category.id.min()
    #cat_id= request.vars.category_id or db(db.category.gender_id==gender_default).select(cat_min).first()[cat_min]
    tatami_default = request.vars.tatami_default or '0'
    

    tatamis = db(  db.tatami.id>0  ).select(db.tatami.ALL)


    cat_min = db.category.id.min()
    subcat_min = db.subcategory.id.min()
    gender_default = request.vars.gender_default or 0
    
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
      photo =   IMG( _width="60px",_heigth="60px",_src= URL('default', 'download', args=[url_photo]),_alt=url_photo )
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
      photo = IMG( _width="60px",_heigth="60px",_src= URL('default', 'download', args=[url_photo]),_alt=url_photo )
      if url_photo is None or len(url_photo)<1:
       photo =   IMG( _width="60px",_heigth="60px",_src= URL('static', 'images/nophoto.jpg', args=[url_photo]),_alt='')
      return DIV(photo, txt,BR(),STRONG(dojo) ,_style="color:#ff0000;")       
    #db.athlete.photo.represent = lambda r,i: IMG( _width="80px",_heigth="80px",_src= URL('default', 'download', args=[i.photo]),_alt="de" )
    db.fight.athlete_blue_id.represent = lambda i,r: get_photo_blue(i,r)
    db.fight.athlete_red_id.represent = lambda i,r: get_photo_red(i,r)
    db.fight.athlete_win_id.represent = lambda i,r: db( db.athlete.id == r.athlete_win_id).select(db.athlete.name).first().as_dict()['name'] if db( db.athlete.id == r.athlete_win_id).select(db.athlete.name).first() else '..'
 
    qrys = []
    if  tatami_default!='0':
      qrys=[ db.fight.tatami_id==tatami_default ]
    else:
      qrys=[ db.fight.tatami_id==None ]


    if  gender_default!='0':
      qrys.append(db.fight.gender_id==gender_default )

    if  cat_id!='0':
      qrys.append(db.fight.category_id==cat_id )      
    if  subcat_default!='0':
      qrys.append(db.fight.subcategory_id==subcat_default ) 
       
    qrys.append( db.fight.finished == None )
    qrys.append(  (db.fight.athlete_red_id != None) |  (db.fight.athlete_blue_id != None) )
    qrys.append( db.fight.athlete_win_id == None )

    """qry=( (db.fight.tatami_id==tatami_default) & (db.fight.finished == None)  
        & ( (db.fight.athlete_red_id != None) |  (db.fight.athlete_blue_id != None) )
        & (db.fight.athlete_win_id == None)  )
    if tatami_default == '0':
       qry=( (db.fight.tatami_id==None) & (db.fight.finished == None)  
        & ( (db.fight.athlete_red_id != None) |  (db.fight.athlete_blue_id != None) )
        & (db.fight.athlete_win_id == None)  )
    """
    qry = reduce(lambda a, b:(a & b), qrys)

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
    #<a type="button" target="_blank"  href="{{=URL('dashboard','index',vars=dict(match_id=record.fight.id)) }}" class="btn btn-primary btn-xs">Tablero de Control</a>
    links = [lambda row: A('Tablero',_href=URL('dashboard','index',vars=dict(match_id=row.id)), _class="btn btn-primary btn-xs" )] 
    grid = SQLFORM.grid(qry,showbuttontext=False, fields = fields , links=links, deletable=False, create=False)
    
    tatamis = db.executesql("""select count(b.id) as peleas, coalesce(a.name,'SINF.') as tatami ,coalesce(a.id,0) as id from tatami a
                                        FULL outer join fight b on a.id= b.tatami_id
                                        where finished is null 

                                        group by 2,3 order by 3 """,as_dict=True)

    return dict(grid=grid,tatamis=tatamis, tatami_default = tatami_default,genders= genders , gender_default=gender_default, categories = categories, cat_id=cat_id,subcategories = subcategories, subcat_default = subcat_default)

@auth.requires_login()
def matchs():
    Athlete_red  =  db.athlete.with_alias('athlete_red')
    Athlete_blue  =  db.athlete.with_alias('athlete_blue')
    matchs = db(  (db.fight.id>0 ) & (db.fight.finished == None)  
        & ( (db.fight.athlete_red_id != None) |  (db.fight.athlete_blue_id != None) )
        & (db.fight.athlete_win_id == None) 
        ) .select( db.fight.ALL, Athlete_red.ALL, Athlete_blue.ALL,db.tatami.ALL,db.category.ALL, db.gender.ALL,
                                                            left=(  Athlete_red.on(Athlete_red.id == db.fight.athlete_red_id),
                                                                      Athlete_blue.on(Athlete_blue.id == db.fight.athlete_blue_id ),
                                                                    db.tatami.on(  db.fight.tatami_id == db.tatami.id ), 
                                                                    db.category.on(  db.fight.category_id == db.category.id ),   
                                                                    db.gender.on(  db.fight.gender_id == db.gender.id ), 
                                                            ),orderby=(db.fight.phase,db.fight.id))
    
    matchs_by_tatami = db.executesql("""select count(*),coalesce(tatami_id,0) from fight group by 2 """,as_dict=True)
    return dict(matchs=matchs,matchs_by_tatami= matchs_by_tatami)
    
def users():

    objs = SQLFORM.grid(db.auth_user)
    return dict(objs=objs)
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
def carga_atleta():
  from gluon.contrib.populate import populate
  populate(db.athlete,1000)
