# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A( IMG(_src=URL('static','images/logo.jpg'), _alt='', _width="40px"),
                  _class="navbar-brand", _href=URL('index'),
                  _id="web2py-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
    (T('Athletes'), False, URL('athlete', 'index'), []),
    (T('Matchs'), False, URL('fight', 'index'), [
        (T('By category'), False, URL('fight', 'index'), []),
        (T('By Brackets'), False, URL('fight', 'bracket'), []),
        (T('By Tatami'), False, URL('fight', 'tatami'), []),
        (T('By Dojo'), False, URL('fight', 'dojo'), []),

    ]),
    (T('Configuration'), False, URL('config', 'index'), [
       (T('Tournament'), False, URL('config', 'index'), []),
        (T('Tatamis'), False, URL('config', 'tatami'), []), 

       (T('Categories'), False, URL('config', 'category'), []),  
       (T('State'), False, URL('config', 'state'), []), 
       (T('Schools'), False, URL('config', 'school'), []), 
      
       (T('Dojo'), False, URL('config', 'dojo'), []), 

        (T('Users'), False, URL('config', 'users'), []), 
        (T('Athletes'), False, URL('athlete', 'index'), []), 
        (T('Generate Matchs'), False, URL('fight', 'generate_matchs'), []), 
    ]),

    (T('Stats'), False, URL('monitor', 'index'), [
        (T('By Dojo'), False, URL('monitor', 'index'), []),
        (T('By Dojo '), False, URL('fight', 'bracket'), []),
        (T('By Tatami'), False, URL('fight', 'tatami'), []),

    ]),
    (T('Reports'), False, URL('fight', 'index'), [
        (T('Athletes'), False, URL('report', 'athlete'), []),
        (T('Matchs'), False, URL('report', 'index'), []),

    ]),
]

DEVELOPMENT_MENU = False


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    app = request.application
    ctr = request.controller
    # ------------------------------------------------------------------------------------------------------------------
    # useful links to internal and external resources
    # ------------------------------------------------------------------------------------------------------------------
    response.menu += [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
        (T('This App'), False, '#', [
            (T('Design'), False, URL('admin', 'default', 'design/%s' % app)),
            LI(_class="divider"),
            (T('Controller'), False,
             URL(
                 'admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr))),
            (T('View'), False,
             URL(
                 'admin', 'default', 'edit/%s/views/%s' % (app, response.view))),
            (T('DB Model'), False,
             URL(
                 'admin', 'default', 'edit/%s/models/db.py' % app)),
            (T('Menu Model'), False,
             URL(
                 'admin', 'default', 'edit/%s/models/menu.py' % app)),
            (T('Config.ini'), False,
             URL(
                 'admin', 'default', 'edit/%s/private/appconfig.ini' % app)),
            (T('Layout'), False,
             URL(
                 'admin', 'default', 'edit/%s/views/layout.html' % app)),
            (T('Stylesheet'), False,
             URL(
                 'admin', 'default', 'edit/%s/static/css/web2py-bootstrap3.css' % app)),
            (T('Database'), False, URL(app, 'appadmin', 'index')),
            (T('Errors'), False, URL(
                'admin', 'default', 'errors/' + app)),
            (T('About'), False, URL(
                'admin', 'default', 'about/' + app)),
        ]),
        ('web2py.com', False, '#', [
            (T('Download'), False,
             'http://www.web2py.com/examples/default/download'),
            (T('Support'), False,
             'http://www.web2py.com/examples/default/support'),
            (T('Demo'), False, 'http://web2py.com/demo_admin'),
            (T('Quick Examples'), False,
             'http://web2py.com/examples/default/examples'),
            (T('FAQ'), False, 'http://web2py.com/AlterEgo'),
            (T('Videos'), False,
             'http://www.web2py.com/examples/default/videos/'),
            (T('Free Applications'),
             False, 'http://web2py.com/appliances'),
            (T('Plugins'), False, 'http://web2py.com/plugins'),
            (T('Recipes'), False, 'http://web2pyslices.com/'),
        ]),
        (T('Documentation'), False, '#', [
            (T('Online book'), False, 'http://www.web2py.com/book'),
            LI(_class="divider"),
            (T('Preface'), False,
             'http://www.web2py.com/book/default/chapter/00'),
            (T('Introduction'), False,
             'http://www.web2py.com/book/default/chapter/01'),
            (T('Python'), False,
             'http://www.web2py.com/book/default/chapter/02'),
            (T('Overview'), False,
             'http://www.web2py.com/book/default/chapter/03'),
            (T('The Core'), False,
             'http://www.web2py.com/book/default/chapter/04'),
            (T('The Views'), False,
             'http://www.web2py.com/book/default/chapter/05'),
            (T('Database'), False,
             'http://www.web2py.com/book/default/chapter/06'),
            (T('Forms and Validators'), False,
             'http://www.web2py.com/book/default/chapter/07'),
            (T('Email and SMS'), False,
             'http://www.web2py.com/book/default/chapter/08'),
            (T('Access Control'), False,
             'http://www.web2py.com/book/default/chapter/09'),
            (T('Services'), False,
             'http://www.web2py.com/book/default/chapter/10'),
            (T('Ajax Recipes'), False,
             'http://www.web2py.com/book/default/chapter/11'),
            (T('Components and Plugins'), False,
             'http://www.web2py.com/book/default/chapter/12'),
            (T('Deployment Recipes'), False,
             'http://www.web2py.com/book/default/chapter/13'),
            (T('Other Recipes'), False,
             'http://www.web2py.com/book/default/chapter/14'),
            (T('Helping web2py'), False,
             'http://www.web2py.com/book/default/chapter/15'),
            (T("Buy web2py's book"), False,
             'http://stores.lulu.com/web2py'),
        ]),
        (T('Community'), False, None, [
            (T('Groups'), False,
             'http://www.web2py.com/examples/default/usergroups'),
            (T('Twitter'), False, 'http://twitter.com/web2py'),
            (T('Live Chat'), False,
             'http://webchat.freenode.net/?channels=web2py'),
        ]),
    ]


if DEVELOPMENT_MENU:
    _()

if "auth" in locals():
    auth.wikimenu()
    
    
    
def print_admin_menu( default_ ):
     
     
    list_options_html=""
    str_active =""
    for idx,m in enumerate(response.menu[3][3]):
        str_active = 'active' if  m[2] in request.env['request_uri'] else ''
            
        list_options_html+='<li class="list-group-item '+str_active+'" >'+str(A( m[0], _href=m[2] ))+'</li>'
    
    
    html="""
     <div class="panel panel-info">
  <div class="panel-heading"><h3 class="panel-title"><a class="btn-block"
      href="URL('admin','default','index')}}">
      <i class="glyphicon glyphicon-cog"></i>
      {{=T("admin")}}
    </a></h3></div>
  <div class="panel-body">
   
  </div>
  <ul class="list-group">
  %s
  </ul>
</div>
    """ % list_options_html
    return XML(html)
