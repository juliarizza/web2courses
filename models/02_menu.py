# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
                  _class="navbar-brand",_href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
    (T('Courses'), False, URL('default', 'courses'), []),
    (T('Shopping Cart'), False, URL('payments', 'shopping_cart'), [])
]

if auth.user:
	response.menu.extend([
		(T('My courses'), False, URL('default', 'my_courses'), []),
		(T('Payment History'), False, URL('payments', 'history'), [])
		])

if auth.has_membership('Teacher') or auth.has_membership('Admin'):
	response.menu.extend([
		(T('Manage courses'), False, URL('manage', 'courses'), []),
		(T('My Calendar'), False, URL('manage', 'calendar'), [])
		])

if "auth" in locals(): auth.wikimenu() 
