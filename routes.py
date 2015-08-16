# -*- coding: utf-8 -*-

#  This is an app-specific example router
#
#  This simple router is used for setting languages from app/languages directory
#  as a part of the application path:  app/<lang>/controller/function
#  Language from default.py or 'en' (if the file is not found) is used as
#  a default_language
#
# See <web2py-root-dir>/router.example.py for parameter's detail
#-------------------------------------------------------------------------------------
# To enable this route file you must do the steps:
#
# 1. rename <web2py-root-dir>/router.example.py to routes.py
# 2. rename this APP/routes.example.py to APP/routes.py
#    (where APP - is your application directory)
# 3. restart web2py (or reload routes in web2py admin interfase)
#
# YOU CAN COPY THIS FILE TO ANY APPLICATION'S ROOT DIRECTORY WITHOUT CHANGES!

from fileutils import abspath
from languages import read_possible_languages

possible_languages = read_possible_languages(abspath('applications', app))
#NOTE! app - is an application based router's parameter with name of an
#            application. E.g.'welcome'

routers = {
    app: dict(
        default_controller='default',
        default_function={'default': 'index', 'manage': 'courses', 'payments': 'shopping_cart'},
        controllers='DEFAULT',
        functions={
            'default': ['index', 'user', 'download', 'call', 'courses', 
                        'course', 'enroll', 'my_courses', 'my_class', 'lesson',
                        'forum', 'topic', 'new_topic', 'calendar', 'announcements'],
            'manage': ['courses', 'classes', 'lessons', 'pick_type',
                        'new', 'edit', 'delete', 'generate_certificate',
                        'send_certificate', 'preview_certificate', 'download_pdf',
                        'calendar', 'new_date', 'schedule_lesson', 'edit_lesson_date',
                        'interests'],
            'payments': ['shopping_cart', 'remove_from_shopping_cart', 
                        'register_order', 'pay_courses', 'paypal', 'ipn',
                        'success', 'history', 'details']
            }
    ),
}

#NOTE! To change language in your application using these rules add this line
#in one of your models files:
#   if request.uri_language: T.force(request.uri_language)
