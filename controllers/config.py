# -*- coding: utf-8 -*-
# try something like
def index(): 
    grid = SQLFORM.grid(db.tournament)
    return dict(grid = grid)

def category(): 
    grid = SQLFORM.grid(db.category)
    return dict(grid = grid)


def school(): 
    grid = SQLFORM.grid(db.school)
    return dict(grid = grid)
    
def dojo(): 
    grid = SQLFORM.grid(db.dojo)
    return dict(grid = grid)

def state(): 
    grid = SQLFORM.grid(db.states)
    return dict(grid = grid)


def tatami(): 
    grid = SQLFORM.grid(db.tatami)
    return dict(grid = grid)


def users():
    db.auth_group.format='%(role)s'
    db.auth_user.group_id.requires = IS_IN_DB(db,db.auth_group.id,'%(role)s')
    db.auth_user.group_id.represent = lambda id, row: db(db.auth_group.id==row.group_id).select(db.auth_group.role).first().as_dict()['role']
    grid = SQLFORM.grid(db.auth_user)
    return dict(grid = grid)
