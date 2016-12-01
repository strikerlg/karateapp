# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
def index(): 
    grid = SQLFORM.grid(db.tournament)
    return dict(grid = grid, deletable=False)
@auth.requires_login()
def category(): 
    grid = SQLFORM.smartgrid(db.category, deletable=False)
    return dict(grid = grid)

@auth.requires_login()    
def subcategory(): 
    fields = (
        
db.category.gender_id,
db.subcategory.category_id,
db.subcategory.name,
db.subcategory.grade_min_id,    db.subcategory.grade_max_id,
db.subcategory.weight_min,  db.subcategory.weight_max


        )
    qry = ( (db.subcategory.id>0) & (db.subcategory.category_id==db.category.id) & (db.category.gender_id == db.gender.id)  )
    grid = SQLFORM.grid(qry, fields = fields, deletable=False)
    return dict(grid = grid)
@auth.requires_login()
def school(): 
    grid = SQLFORM.smartgrid(db.school, deletable=False)
    return dict(grid = grid)
@auth.requires_login()    
def dojo(): 
    grid = SQLFORM.grid(db.dojo, deletable=False)
    return dict(grid = grid)
@auth.requires_login()
def state(): 
    grid = SQLFORM.grid(db.states, deletable=False)
    return dict(grid = grid)

@auth.requires_login()
def tatami(): 
    grid = SQLFORM.grid(db.tatami, deletable=False)
    return dict(grid = grid)

@auth.requires_login()
def users():
    db.auth_group.format='%(role)s'
    db.auth_user.group_id.requires = IS_IN_DB(db,db.auth_group.id,'%(role)s')
    db.auth_user.tatami_id.requires = IS_NULL_OR( IS_IN_DB(db,db.tatami.id,'%(name)s'))
    db.auth_user.tatami_id.represent = lambda id, row: db(db.tatami.id==row.tatami_id).select(db.tatami.name).first().as_dict()['name'] if db(db.tatami.id==row.tatami_id).count()>0 else ''
    db.auth_user.group_id.represent = lambda id, row: db(db.auth_group.id==row.group_id).select(db.auth_group.role).first().as_dict()['role']
    grid = SQLFORM.grid(db.auth_user)
    return dict(grid = grid)
