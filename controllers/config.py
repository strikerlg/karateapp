# -*- coding: utf-8 -*-
# try something like
def index(): 
    grid = SQLFORM.smartgrid(db.tournament)
    return dict(grid = grid)

def category(): 
    grid = SQLFORM.smartgrid(db.category)
    return dict(grid = grid)

def dojo(): 
    grid = SQLFORM.smartgrid(db.dojo)
    return dict(grid = grid)

def state(): 
    grid = SQLFORM.smartgrid(db.states)
    return dict(grid = grid)
def users():
    db.auth_group.format='%(role)s'
    db.auth_user.group_id.requires = IS_IN_DB(db,db.auth_group.id,'%(role)s')
    grid = SQLFORM.grid(db.auth_user)
    return dict(grid = grid)
