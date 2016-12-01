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
auth.settings.extra_fields['auth_user'] =[ Field('group_id', 'integer', label = T('Role')) , Field('tatami_id', 'integer', label = T('Tatami'))]
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
auth.settings.create_user_groups = None
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


db.define_table('grade',

               Field('name', label = T('name'),requires=IS_UPPER()),
               format = "%(name)s",
                )

db.define_table('gender',

               Field('name', label = T('name'),requires=IS_UPPER()),
               format = "%(name)s",
                )
db.define_table('school',
               Field('name', label = T('name'),requires=IS_UPPER()),
               format = "%(name)s",
               )
               
db.define_table('states',
               Field('code'),
               Field('name', label = T('name') ,requires=IS_UPPER()),
               format = "%(name)s",
               )
db.define_table('tournament',
               Field('name', label = T('name'),requires=[IS_NOT_EMPTY(), IS_UPPER()]),
               Field('description', label = T('descriptions'),requires=IS_NOT_EMPTY()),
               Field('date_start','datetime', label = T('date_start'), requires=IS_DATE(format = '%d/%m/%Y')),
               Field('bracket','boolean',writable=False,default=False),
               format = "%(name)s",
               )
db.define_table('dojo',
               Field('name', label = T('name') , requires = IS_UPPER() ),
               Field('school_id',db.school, label = T('school')),
               Field('state_id',db.states, label = T('state')),
               format = "%(name)s",
               )

db.define_table('tatami',
               Field('name', label = T('name')),
               Field('tournament_id',db.tournament, label = T('tournament')),
               format = "%(name)s",
               )
db.define_table('circuit',
               Field('name', label = T('name')),
               #Field('tournament_id',db.tournament, label = T('tournament')),
               format = "%(name)s",
               )
db.define_table('category_type',
			 Field('name', label = T('name'), requires = IS_UPPER()),
			format="%(name)s"
			)
db.define_table('category',
               Field('name', label = T('name'), requires = IS_UPPER()),
               Field('category_type_id',db.category_type),
               Field('tournament_id',db.tournament, label = T('tournament')),
               Field('gender_id',db.gender,label=T('gender')),
               Field('age_min','integer',label=T('age_min')),
               Field('age_max','integer',label=T('age_max')),
               Field('minutes','integer',label=T('Duracion Pelea (mins)')),
               Field('circuit_id',db.circuit,label=T('circuit') ),
               format = "%(name)s",
               #format = lambda r: "%s-%s" % (db( (db.gender.id==r.gender_id) ).select(db.gender.name).first().name,
               #                             r.name )
               )
db.define_table('subcategory',
               Field('name', label = T('name'), requires = IS_UPPER()),
               Field('category_id',db.category, label = T('category')),
               #Field('gender_id',db.gender,label=T('gender')),
               Field('grade_min_id',db.grade,label=T('grade_min')),
               Field('grade_max_id',db.grade,label=T('grade_max')),
               Field('weight_min','integer',label=T('weight_min')),
               Field('weight_max','integer',label=T('weight_max')),               
               format = "%(name)s",
               #format = lambda r: "%s-%s-%s" % (db( (db.category.id==r.category_id) & (db.category.gender_id==db.gender.id) ).select(db.gender.name).first().name,
               #                             db(db.category.id==r.category_id).select(db.category.name).first().name, 
               #                             r.name )
               )               
def calculate_age(birth):
    import datetime
    diff = (datetime.date.today() - birth).days
    years = int(diff/365)
    return years               
               

def set_category( birth_date_ , gender_, circuit_, type_):
    age = calculate_age(birth_date_)
    category_id = db( (db.category.gender_id== gender_ ) & (db.category.category_type_id== type_ ) & (db.category.age_max>= age ) & (db.category.age_min<= age) ).select(db.category.id).first().as_dict()['id']
    if circuit_==2:
        category_id = db( (db.category.gender_id== gender_ ) & (db.category.category_type_id== type_ ) & (db.category.circuit_id== circuit_ ) & (db.category.age_max>= age ) & (db.category.age_min<= age) ).select(db.category.id).first().as_dict()['id']
    return category_id 

def set_subcategory( birth_date_ , gender_, grade_id, circuit_,type_, weight_):
    import logging
    logger = logging.getLogger(request.application)
    logger.setLevel(logging.DEBUG)
    
    
    age = calculate_age(birth_date_)
    logger.debug('CDSM1')
    logger.debug(circuit_)
    
    category_id = None
    subcategory_id = None
    if circuit_==2:
      category_id = db( (db.category.gender_id== gender_ ) & (db.category.category_type_id== type_ ) & (db.category.circuit_id== circuit_ ) & (db.category.age_max>= age ) & (db.category.age_min<= age)
                      ).select(db.category.id).first().as_dict()['id']
      subcategory_id = db (  (db.subcategory.category_id==category_id) & 
                             (db.subcategory.grade_max_id>=grade_id) & 
                             (db.subcategory.grade_min_id<=grade_id) &
                             (db.subcategory.weight_min<=weight_) &
                             (db.subcategory.weight_max>=weight_) 
                      ).select(db.subcategory.id).first().as_dict()['id']
    else:
      category_id = db( (db.category.gender_id== gender_ ) & (db.category.category_type_id== type_ ) & (db.category.age_max>= age ) & (db.category.age_min<= age)
                      ).select(db.category.id).first().as_dict()['id']
      subcategory_id = db (  (db.subcategory.category_id==category_id) & (db.subcategory.grade_max_id>=grade_id) & (db.subcategory.grade_min_id<=grade_id)
                      ).select(db.subcategory.id).first().as_dict()['id']
    logger = logging.getLogger(request.application)
    logger.setLevel(logging.DEBUG)
    logger.debug('CDSM3')
    
    return subcategory_id  
KUMITE_ID=1
db.define_table('athlete',
               Field('tournament_id',db.tournament, label = T('tournament'),default=1),
               Field('photo','upload',requires=IS_NULL_OR(IS_IMAGE())),
               Field('identity_number','string', label = T('identity_number'),default="NA" ),
               Field('gender_id', db.gender,label = T('gender')),
               Field('name', label = T('name') ,requires = IS_UPPER()),
               Field('grade_id',db.grade, label = T('grade') , requires = IS_IN_DB(db, 'grade.id', db.grade._format,orderby=db.grade.id)) ,
               Field('birth_date','date', label = T('birth_date'), requires = IS_DATE(format = '%d/%m/%Y')),
               Field('age', 'integer',label = T('age'), compute = lambda r: calculate_age(r['birth_date'])  ),
               Field('weight', 'integer',label = T('weight'), default=0),
               Field('dojo_id',db.dojo, label = T('dojo')),
               Field('circuit_id',db.circuit, label = T('circuit'), default=1),
	             Field('disability','boolean',label=T('Alguna Discapacidad'),default=False),
	             Field('kumite','boolean',label=T('kumite')),
               Field('payment_kumite','boolean',label=T('Pago')),
	             Field('kata_individual','boolean',label=T('kata_individual')),
	             Field('kata_team','boolean',label=T('kata_equipo')),
               Field('category_id',db.category, compute = lambda r: set_category(r['birth_date'], r['gender_id'], r['circuit_id'],KUMITE_ID)),
               Field('subcategory_id',db.subcategory, compute = lambda r: set_subcategory( r['birth_date'], r['gender_id'] , r['grade_id'],  r['circuit_id'],KUMITE_ID, r['weight']))
               )



db.define_table('fight',
               Field('tournament_id',db.tournament, label = T('tournament_id')),
               Field('phase','integer', label = T('phase'),writable =False ),
               Field('fight_num','integer',label = T('fight_num'), writable =False ),
               Field('tatami_id',db.tatami, label = T('tatami')),
               Field('athlete_blue_id','integer', label = T('athlete_blue'),requires=IS_NULL_OR(IS_IN_DB(db,db.athlete.id,'%(name)s'))), 
               Field('athlete_red_id','integer', label = T('athlete_red'),requires=IS_NULL_OR(IS_IN_DB(db,db.athlete.id,'%(name)s'))), 
               Field('athlete_win_id','integer', label = T('athlete_win'),requires=IS_NULL_OR(IS_IN_DB(db,db.athlete.id,'%(name)s'))), 
               Field('red_score','integer', label = T('red_score'), writable =False ),
               Field('blue_score','integer', label = T('blue_score'), writable =False ),
               
               Field('finished','boolean', label = T('finished'), writable =False ),              
               Field('referee_id','integer', label = T('referee'), writable =False ),
               Field('category_id',db.category, label = T('category') , writable =False  ) ,
               Field('gender_id',db.gender, label = T('gender')  , writable =False  ) ,
               Field('subcategory_id',db.subcategory, label = T('subcategory') , writable =False   ) ,
               Field('blue_c1','integer', label = T('blue_penalty_c1') , writable =False   ) ,
               Field('blue_c2','integer', label = T('blue_penalty_c2') , writable =False   ) ,
               Field('red_c1','integer', label = T('red_penalty_c1') , writable =False   ) ,
               Field('red_c2','integer', label = T('red_penalty_c2') , writable =False   ) ,
	       
               
               
               )

db.define_table('fight_score_detail',
               Field('fight_id',db.fight, label = T('fight')),
               Field('athlete_id',db.athlete, label = T('athlete')),
               Field('textevent','string', label = T('event')),
               Field('val','integer', label = T('name')),
               Field('cronometer_secs','integer', label = T('secs')),
               Field('cronometer_mins','integer', label = T('mins')),                              
               )

db.define_table('fight_fault_detail',
               Field('fight_id',db.fight, label = T('fight')),
               Field('athlete_id',db.athlete, label = T('athlete')),
               Field('event_id','text', label = T('event')),
               Field('val','integer', label = T('name')),
               Field('cronometer_secs','integer', label = T('secs')),
               Field('cronometer_mins','integer', label = T('mins')),                              
               )

db.define_table('fight_json',
               Field('fight_id',db.fight, label = T('fight')),
               Field('data_log','text', label = T('json_data')),
               
               )


def auto_create_membership(field_,id_):
    db.auth_membership.insert(user_id=id_,group_id=field_['group_id'])
    
def auto_update_membership(set_,field_): # set object represent  (db.table.id==1)
    user = set_.select(db.auth_user.id).first()
    user_member = db(db.auth_membership.user_id==user.id).update(group_id=field_['group_id'])
           
db.auth_user._after_insert.append(lambda field,id: auto_create_membership(field,id))
db.auth_user._before_update.append(lambda set_, field_: auto_update_membership(set_, field_))




"""
def auto_create_athlete_set_category(field_,id_):

    age = calculate_age(field_['birth_date'])
    category_id = db( (db.category.age_max>= age ) & (db.category.age_min<= age) ).select(db.category.id).first().as_dict()['id']
    db(db.athlete.id==id_).update(category_id=category_id)
    
def auto_update_athlete_set_category( set_, field_): # set object represent  (db.table.id==1)
    pass
           
db.athlete._after_insert.append(lambda field,id: auto_create_athlete_set_category(field,id))
db.athlete._before_update.append(lambda set_, field_: auto_update_athlete_set_category(set_, field_))
"""
#db.auth_user.group

T.force('es-es')

def init_data():
  k10,k9,k8,k7,k6,k5,k4,k3,k2,k1,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,sdan = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21)
  if db(db.auth_group.id>0).isempty():
    admin_id= db.auth_group.insert(role = 'admin', description= 'Administrator')
    db.auth_group.insert(role = 'referee', description= 'Referee')
    db.commit()
  if db(db.auth_user.id>0).isempty():
    user_id = db.auth_user.bulk_insert([{'first_name' : 'admin', 
                              'group_id':admin_id,
                               'last_name' : 'admin', 
                               'email' : 'admin@karateapp.com', 
                               'password' : db.auth_user.password.validate('1q2w3e.')[0]}])
  if db(db.circuit.id>0).isempty():
    db.circuit.insert(name="Normal") #1
    db.circuit.insert(name="Dorado") #2
  if db(db.grade.id>0).isempty():
    k10 = db.grade.insert(name="10° kyu") #1
    k9 = db.grade.insert(name="9° kyu") #2
    k8 = db.grade.insert(name="8° kyu") #3
    k7 = db.grade.insert(name="7° kyu") #4
    k6 = db.grade.insert(name="6° kyu") #5
    k5 = db.grade.insert(name="5° kyu") #6
    k4 = db.grade.insert(name="4° kyu") #7
    k3 = db.grade.insert(name="3° kyu") #8
    k2 = db.grade.insert(name="2° kyu") #9
    k1 = db.grade.insert(name="1° kyu") #10
    d1 = db.grade.insert(name="1° dan") #11   
    d2 = db.grade.insert(name="2° dan") #12
    d3 = db.grade.insert(name="3° dan") #13
    d4 = db.grade.insert(name="4° dan") #14
    d5 = db.grade.insert(name="5° dan") #15     
    d6 = db.grade.insert(name="6° dan") #16
    d7 = db.grade.insert(name="7° dan") #17
    d8 = db.grade.insert(name="8° dan") #18
    d9 = db.grade.insert(name="9° dan") #19
    d10 = db.grade.insert(name="10° dan") #20


  if db(db.category.id>0).isempty():     
    tmp_id = db.category.insert(name='04 AÑOS',age_max=4,age_min=4,gender_id=1)
    db.subcategory.insert(name="Todos",category_id=tmp_id,grade_min_id =k10, grade_max_id=d10)

    tmp_id = db.category.insert(name='05 AÑOS',age_max=5,age_min=5,gender_id=1 )
    db.subcategory.insert(name="Todos",category_id=tmp_id,grade_min_id =k10, grade_max_id=d10)

    tmp_id = db.category.insert(name='06 a 07 AÑOS',age_max=07,age_min=06,gender_id=1 )
    db.subcategory.insert(name="10mo-9no Kyu",category_id=tmp_id,grade_min_id =k10, grade_max_id=k9)
    db.subcategory.insert(name="8vo-7mo Kyu",category_id=tmp_id,grade_min_id =k8, grade_max_id=k7)
    db.subcategory.insert(name="6to Kyu +  ",category_id=tmp_id,grade_min_id =k6, grade_max_id=d10)

    tmp_id = db.category.insert(name='08 a 09 AÑOS',age_max=9,age_min=8,gender_id=1)
    db.subcategory.insert(name="10mo-9no Kyu",category_id=tmp_id,grade_min_id = k10 , grade_max_id=k9)
    db.subcategory.insert(name="8vo-7mo Kyu",category_id=tmp_id,grade_min_id =k8, grade_max_id=k7)
    db.subcategory.insert(name="6to-4to Kyu  ",category_id=tmp_id,grade_min_id =k6, grade_max_id=k4)
    db.subcategory.insert(name="3er Kyu +  ",category_id=tmp_id,grade_min_id =k3, grade_max_id=d10)

    tmp_id = db.category.insert(name='10 a 11 AÑOS',age_max=11,age_min=10,gender_id=1)
    db.subcategory.insert(name="10mo-9no Kyu",category_id=tmp_id,grade_min_id = k10 , grade_max_id=k9)
    db.subcategory.insert(name="8vo-7mo Kyu",category_id=tmp_id,grade_min_id =k8, grade_max_id=k7)
    db.subcategory.insert(name="6to-4to Kyu  ",category_id=tmp_id,grade_min_id =k6, grade_max_id=k4)
    db.subcategory.insert(name="3er Kyu +  ",category_id=tmp_id,grade_min_id =k3, grade_max_id=d10)

    tmp_id = db.category.insert(name='12 a 13 AÑOS',age_max=13,age_min=12,gender_id=1)
    db.subcategory.insert(name="10mo-9no Kyu",category_id=tmp_id,grade_min_id = k10 , grade_max_id=k9)
    db.subcategory.insert(name="8vo-7mo Kyu",category_id=tmp_id,grade_min_id =k8, grade_max_id=k7)
    db.subcategory.insert(name="6to-4to Kyu",category_id=tmp_id,grade_min_id =k6, grade_max_id=k4)

    tmp_id = db.category.insert(name='14 a 15 AÑOS',age_max=15,age_min=14,gender_id=1)
    db.subcategory.insert(name="10mo-9no Kyu",category_id=tmp_id,grade_min_id = k10 , grade_max_id=k9)
    db.subcategory.insert(name="8vo-7mo Kyu",category_id=tmp_id,grade_min_id =k8, grade_max_id=k7)
    db.subcategory.insert(name="6to-4to Kyu",category_id=tmp_id,grade_min_id =k6, grade_max_id=k4)

    tmp_id = db.category.insert(name='16 a 17 AÑOS',age_max=17,age_min=16,gender_id=1)
    db.subcategory.insert(name="10mo-9no Kyu",category_id=tmp_id,grade_min_id = k10 , grade_max_id=k9)
    db.subcategory.insert(name="8vo-7mo Kyu",category_id=tmp_id,grade_min_id =k8, grade_max_id=k7)
    db.subcategory.insert(name="6to-4to Kyu",category_id=tmp_id,grade_min_id =k6, grade_max_id=k4)

    tmp_id = db.category.insert(name='18 a 34 AÑOS',age_max=34,age_min=18,gender_id=1)
    db.subcategory.insert(name="10mo-9no Kyu",category_id=tmp_id,grade_min_id = k10 , grade_max_id=k9)
    db.subcategory.insert(name="8vo-7mo Kyu",category_id=tmp_id,grade_min_id =k8, grade_max_id=k7)
    db.subcategory.insert(name="6to-4to Kyu",category_id=tmp_id,grade_min_id =k6, grade_max_id=k4)

    tmp_id = db.category.insert(name='35 a 40 AÑOS',age_max=40,age_min=35,gender_id=1)
    db.subcategory.insert(name="10mo-7no Kyu",category_id=tmp_id,grade_min_id =k10, grade_max_id=k7)
    db.subcategory.insert(name="6to-4to Kyu",category_id=tmp_id,grade_min_id =k6, grade_max_id=k4)

    tmp_id = db.category.insert(name='41 a 50 AÑOS',age_max=50,age_min=41,gender_id=1)
    db.subcategory.insert(name="10mo-7no Kyu",category_id=tmp_id,grade_min_id =k10, grade_max_id=k7)
    db.subcategory.insert(name="6to Kyu +",category_id=tmp_id,grade_min_id =k6, grade_max_id=d10)    
    
    tmp_id = db.category.insert(name='mas 50 AÑOS',age_max=99,age_min=51,gender_id=1)
    db.subcategory.insert(name="10mo-7no Kyu",category_id=tmp_id,grade_min_id =k10, grade_max_id=k7)
    db.subcategory.insert(name="6to Kyu +",category_id=tmp_id,grade_min_id =k6, grade_max_id=d10)  

    #CARGA DE FEMENINO / LOAD WOMEN DATA
    tmp_id = db.category.insert(name='04 a 05 AÑOS',age_max=5,age_min=4,gender_id=2)
    db.subcategory.insert(name="Todos",category_id=tmp_id,grade_min_id =k10, grade_max_id=d10)


    tmp_id = db.category.insert(name='06 a 07 AÑOS',age_max=07,age_min=06,gender_id=2 )
    db.subcategory.insert(name="10mo-9no Kyu",category_id=tmp_id,grade_min_id =k10, grade_max_id=k9)
    db.subcategory.insert(name="8vo-7mo Kyu",category_id=tmp_id,grade_min_id =k8, grade_max_id=k7)
    db.subcategory.insert(name="6to Kyu +  ",category_id=tmp_id,grade_min_id =k6, grade_max_id=d10)

    tmp_id = db.category.insert(name='08 a 09 AÑOS',age_max=9,age_min=8,gender_id=2)
    db.subcategory.insert(name="10mo-9no Kyu",category_id=tmp_id,grade_min_id = k10 , grade_max_id=k9)
    db.subcategory.insert(name="8vo-7mo Kyu",category_id=tmp_id,grade_min_id =k8, grade_max_id=k7)
    db.subcategory.insert(name="6to-4to Kyu  ",category_id=tmp_id,grade_min_id =k6, grade_max_id=k4)
    db.subcategory.insert(name="3er Kyu +  ",category_id=tmp_id,grade_min_id =k3, grade_max_id=d10)

    tmp_id = db.category.insert(name='10 a 11 AÑOS',age_max=11,age_min=10,gender_id=2)
    db.subcategory.insert(name="10mo-9no Kyu",category_id=tmp_id,grade_min_id = k10 , grade_max_id=k9)
    db.subcategory.insert(name="8vo-7mo Kyu",category_id=tmp_id,grade_min_id =k8, grade_max_id=k7)
    db.subcategory.insert(name="6to-4to Kyu  ",category_id=tmp_id,grade_min_id =k6, grade_max_id=k4)
    db.subcategory.insert(name="3er Kyu +  ",category_id=tmp_id,grade_min_id =k3, grade_max_id=d10)

    tmp_id = db.category.insert(name='12 a 13 AÑOS',age_max=13,age_min=12,gender_id=2)
    db.subcategory.insert(name="10mo-9no Kyu",category_id=tmp_id,grade_min_id = k10 , grade_max_id=k9)
    db.subcategory.insert(name="8vo-7mo Kyu",category_id=tmp_id,grade_min_id =k8, grade_max_id=k7)
    db.subcategory.insert(name="6to-4to Kyu",category_id=tmp_id,grade_min_id =k6, grade_max_id=k4)

    tmp_id = db.category.insert(name='14 a 15 AÑOS',age_max=15,age_min=14,gender_id=2)
    db.subcategory.insert(name="10mo-9no Kyu",category_id=tmp_id,grade_min_id = k10 , grade_max_id=k9)
    db.subcategory.insert(name="8vo-7mo Kyu",category_id=tmp_id,grade_min_id =k8, grade_max_id=k7)
    db.subcategory.insert(name="6to-4to Kyu",category_id=tmp_id,grade_min_id =k6, grade_max_id=k4)

    tmp_id = db.category.insert(name='16 a 17 AÑOS',age_max=17,age_min=16,gender_id=2)
    db.subcategory.insert(name="10mo-9no Kyu",category_id=tmp_id,grade_min_id = k10 , grade_max_id=k9)
    db.subcategory.insert(name="8vo-7mo Kyu",category_id=tmp_id,grade_min_id =k8, grade_max_id=k7)
    db.subcategory.insert(name="6to-4to Kyu",category_id=tmp_id,grade_min_id =k6, grade_max_id=k4)

    tmp_id = db.category.insert(name='18 a 29 AÑOS',age_max=29,age_min=18,gender_id=2)
    db.subcategory.insert(name="10mo-9no Kyu",category_id=tmp_id,grade_min_id = k10 , grade_max_id=k9)
    db.subcategory.insert(name="8vo-7mo Kyu",category_id=tmp_id,grade_min_id =k8, grade_max_id=k7)
    db.subcategory.insert(name="6to-4to Kyu",category_id=tmp_id,grade_min_id =k6, grade_max_id=k4)

    tmp_id = db.category.insert(name='30 a 40 AÑOS',age_max=40,age_min=30,gender_id=2)
    db.subcategory.insert(name="10mo-7no Kyu",category_id=tmp_id,grade_min_id =k10, grade_max_id=k7)
    db.subcategory.insert(name="6to Kyu +",category_id=tmp_id,grade_min_id =k6, grade_max_id=d10) 

    tmp_id = db.category.insert(name='mas 40 AÑOS',age_max=99,age_min=40,gender_id=2)
    db.subcategory.insert(name="10mo-7no Kyu",category_id=tmp_id,grade_min_id =k10, grade_max_id=k7)
    db.subcategory.insert(name="6to Kyu +",category_id=tmp_id,grade_min_id =k6, grade_max_id=d10) 


    tmp_id = db.category.insert(name='Dorado 12 a 13 Años',age_max=13,age_min=12,gender_id=2)
    db.subcategory.insert(name="3er Kyu + (-45kg)",category_id=tmp_id,grade_min_id =k6, grade_max_id=d10)
    db.subcategory.insert(name="3er Kyu + (+45kg)",category_id=tmp_id,grade_min_id =k6, grade_max_id=d10)      

  if db(db.gender.id>0).isempty():
    db.gender.insert(name="Masculino")
    db.gender.insert(name="Femenino")
  if db(db.tatami.id>0).isempty():
    db.tatami.insert(name="Cancha 1")
    db.tatami.insert(name="Cancha 2")    
    db.tatami.insert(name="Cancha 3")
    db.tatami.insert(name="Cancha 4") 
    db.tatami.insert(name="Cancha 5")
    db.tatami.insert(name="Cancha 6")         
    db.tatami.insert(name="Cancha 7")
    db.tatami.insert(name="Cancha 8") 
    db.tatami.insert(name="Cancha 9")
    db.tatami.insert(name="Cancha 10")
    db.tatami.insert(name="Cancha 11")
    db.tatami.insert(name="Cancha 12") 
    db.tatami.insert(name="Cancha 13")
    db.tatami.insert(name="Cancha 14")
    db.tatami.insert(name="Cancha 15")
    db.tatami.insert(name="Cancha 16")        
  if db(db.states.id>0).isempty():
    db.states.insert(name="DISTRITO CAPITAL")
    
    db.states.insert(name="APURE")
    db.states.insert(name="ARAGUA")   
    db.states.insert(name="BARINAS")
  
    db.states.insert(name="BOLIVAR")
    db.states.insert(name="CARABOBO")   

    db.states.insert(name="COJEDES")
  
    db.states.insert(name="FALCON")
    db.states.insert(name="GUARICO")   
    db.states.insert(name="LARA")
    db.states.insert(name="MERIDA")   
    db.states.insert(name="MIRANDA")
    db.states.insert(name="MONAGAS")   
    db.states.insert(name="NUEVA ESPARTA")
    db.states.insert(name="PORTUGUESA")   
    db.states.insert(name="SUCRE")
    db.states.insert(name="TACHIRA")   
    db.states.insert(name="TRUJILLO")
    db.states.insert(name="YARACUY")
    db.states.insert(name="ZULIA")   
    db.states.insert(name="AMAZONAS") 
    db.states.insert(name="DELTA AMACURO") 
    db.states.insert(name="VARGAS") 
  if db(db.category_type.id>0).isempty():
    db.category_type.insert(name="KUMITE")
    db.category_type.insert(name="KATA INDIVIDUAL")
    db.category_type.insert(name="KATA EQUIPO")
                                                                    
init_data()


"""
truncate grade cascade;
ALTER SEQUENCE grade_id_seq MINVALUE 0;
SELECT setval('public.grade_id_seq', 0, true);

ALTER SEQUENCE fight_id_seq MINVALUE 0;
SELECT setval('public.fight_id_seq', 0, true);

truncate category cascade;
ALTER SEQUENCE category_id_seq MINVALUE 0;
SELECT setval('public.category_id_seq', 0, true);

ALTER SEQUENCE subcategory_id_seq MINVALUE 0;
ALTER SEQUENCE subcategory_id_seq MINVALUE 0;
SELECT setval('public.subcategory_id_seq', 0, true);


truncate tatami cascade;
ALTER SEQUENCE tatami_id_seq MINVALUE 0;
SELECT setval('public.tatami_id_seq', 0, true);

truncate fight cascade;
ALTER SEQUENCE fight_id_seq MINVALUE 0;
SELECT setval('public.fight_id_seq', 0, true);
truncate states cascade;
ALTER SEQUENCE states_id_seq MINVALUE 0;
SELECT setval('public.states_id_seq', 0, true);

truncate athlete cascade;
ALTER SEQUENCE athlete_id_seq MINVALUE 0;
SELECT setval('public.athlete_id_seq', 0, true);

truncate dojo cascade;
ALTER SEQUENCE dojo_id_seq MINVALUE 0;
SELECT setval('public.dojo_id_seq', 0, true);

truncate school cascade;
ALTER SEQUENCE school_id_seq MINVALUE 0;
SELECT setval('public.school_id_seq', 0, true);

"""
