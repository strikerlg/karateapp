# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] =[ Field('group_id', 'integer', label = T('Role')) ]
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

db.define_table('school',
               Field('name', label = T('name')),
               format = "%(name)s",
               )
               
db.define_table('states',
               Field('code'),
               Field('name', label = T('name')),
               format = "%(name)s",
               )
db.define_table('tournament',
               Field('name', label = T('name'),requires=IS_NOT_EMPTY()),
               Field('date_start','datetime', label = T('date_start')),
               format = "%(name)s",
               )
db.define_table('dojo',
               Field('name', label = T('name')),
               Field('school_id',db.school, label = T('school')),
               Field('state_id',db.states, label = T('state')),
               format = "%(name)s",
               )

db.define_table('tatami',
               Field('name', label = T('name')),
               Field('tournament_id',db.tournament, label = T('tournament')),
               format = "%(name)s",
               )

db.define_table('category',
               Field('name', label = T('name')),
               Field('tournament_id',db.tournament, label = T('tournament')),
               format = "%(name)s",
               )
db.define_table('athlete',
               Field('tournament_id',db.tournament, label = T('tournament')),
               Field('photo','upload',requires=IS_IMAGE()),
               Field('identity_number','string', label = T('identity_number'),requires=IS_NOT_EMPTY() ),
               Field('name', label = T('name')),
               Field('birth_date','date', label = T('birth_date')),
               Field('age', 'integer',label = T('age')),
               Field('dojo_id',db.dojo, label = T('dojo')),
               Field('category_id',db.category, label = T('category'))                            
               )

db.define_table('fight',
               Field('tournament_id',db.tournament, label = T('tournament_id')),
               Field('tatami_id',db.tatami, label = T('tatami')),
               Field('athlete_blue_id', label = T('athlete_blue'),requires=IS_NULL_OR(IS_IN_DB(db,db.athlete.id,'%(name)s'))), 
               Field('athlete_red_id', label = T('athlete_red'),requires=IS_NULL_OR(IS_IN_DB(db,db.athlete.id,'%(name)s'))), 
               Field('athlete_win_id', label = T('athlete_win'),requires=IS_NULL_OR(IS_IN_DB(db,db.athlete.id,'%(name)s'))),
               Field('red_score','integer', label = T('red_score')),
               Field('blue_score','integer', label = T('blue_score')),
               Field('start_date','datetime', label = T('start_date')),
               Field('fight_status','integer', label = T('fight_status')),
               Field('phase','integer', label = T('phase'))
               
               )

db.define_table('fight_balance',
               Field('fight_id',db.fight, label = T('fight')),
               Field('athlete_id',db.athlete, label = T('athlete')),
               Field('event_id','text', label = T('event')),
               Field('blue_score','integer', label = T('name')),
               Field('cronometer_secs','integer', label = T('name')),
               Field('cronometer_mins','integer', label = T('name')), 
               Field('phase','integer', label = T('name'))
               
               )

db.define_table('fight_json',
               Field('fight_id',db.fight, label = T('fight')),
               Field('data_log',db.athlete, label = T('json_data')),
               
               )

T.force('es-es')
