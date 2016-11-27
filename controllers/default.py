# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():

    tournaments = db(db.tournament.id>0).select()
    return dict(tournaments=tournaments)

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
    return dict(matchs=matchs)
    
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
