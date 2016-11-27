# -*- coding: utf-8 -*-
# try something like
def index(): 

    def get_photo_blue(i,r):
      dojo = ''
      try:
         rs = db( db.athlete.id == r.athlete_blue_id).select(db.athlete.dojo_id).render(0) 
         dojo = rs.dojo_id
      except:
         pass      
      txt = db( db.athlete.id == r.athlete_blue_id).select(db.athlete.name).first().as_dict()['name'] if db( db.athlete.id == r.athlete_blue_id).select(db.athlete.name).first() else '..'
      url_photo = db( db.athlete.id == r.athlete_blue_id).select(db.athlete.photo).first().as_dict()['photo'] if db( db.athlete.id == r.athlete_blue_id).select(db.athlete.name).first() else None
      photo =   IMG( _width="60px",_heigth="60px",_src= URL('default', 'download', args=[url_photo]),_alt=txt )
      if url_photo is None:
       photo =   IMG( _width="60px",_heigth="60px",_src= URL('static', 'images/nophoto.jpg', args=[url_photo]),_alt=txt)

      return txt

    def get_photo_red(i,r):
      dojo = ''
      try:
         rs = db( db.athlete.id == r.athlete_red_id).select(db.athlete.dojo_id).render(0) 
         dojo = rs.dojo_id
      except:
         pass

      
      txt = db( db.athlete.id == r.athlete_red_id).select(db.athlete.name).first().as_dict()['name'] if db( db.athlete.id == r.athlete_red_id).select(db.athlete.name).first() else '..'
      url_photo = db( db.athlete.id == r.athlete_red_id).select(db.athlete.photo).first().as_dict()['photo'] if db( db.athlete.id == r.athlete_red_id).select(db.athlete.name).first() else None
      photo = IMG( _width="60px",_heigth="60px",_src= URL('default', 'download', args=[url_photo]),_alt=txt )
      if url_photo is None:
       photo =   IMG( _width="60px",_heigth="60px",_src= URL('static', 'images/nophoto.jpg', args=[url_photo]),_alt=txt)
      return txt       
    #db.athlete.photo.represent = lambda r,i: IMG( _width="80px",_heigth="80px",_src= URL('default', 'download', args=[i.photo]),_alt="de" )
    db.fight.athlete_blue_id.represent = lambda i,r: get_photo_blue(i,r)
    db.fight.athlete_red_id.represent = lambda i,r: get_photo_red(i,r)
    db.fight.athlete_win_id.represent = lambda i,r: db( db.athlete.id == r.athlete_win_id).select(db.athlete.name).first().as_dict()['name'] if db( db.athlete.id == r.athlete_win_id).select(db.athlete.name).first() else '..'

    qry=( (db.fight.id>0) )

    fields = (
              db.fight.phase, 
              db.fight.fight_num,
              db.fight.gender_id,
              db.fight.category_id,
              db.fight.subcategory_id,

              db.fight.tatami_id,
              db.fight.athlete_blue_id, 
              db.fight.athlete_red_id,
              db.fight.athlete_win_id, 
              db.fight.finished,

              )

    grid = SQLFORM.grid(qry,showbuttontext=False, fields = fields, deletable=False, create=False)
    return dict(grid=grid)

def athlete():

    qry=( (db.athlete.id>0) & (db.dojo.id==db.athlete.dojo_id))
    grid=SQLFORM.grid(qry,showbuttontext=False, deletable=False, create=False)
    return dict(grid=grid)