# -*- coding: utf-8 -*-
# try something like
def index(): 
    db.athlete.photo.represent = lambda r,i: IMG( _width="80px",_heigth="80px",_src= URL('default', 'download', args=[i.photo]),_alt="de" )
    #links=[lambda r: IMG( _width="80px",_heigth="80px",_src= URL('default', 'download', args=[r.photo]),_alt="de" )]
    grid=SQLFORM.grid(db.athlete)
    return dict(grid=grid)
