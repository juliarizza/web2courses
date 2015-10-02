# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
import itertools

def index():
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """

    if request.args(0) == 'register':
        db.auth_user.bio.writable = db.auth_user.bio.readable = False
        db.auth_user.avatar.writable = db.auth_user.avatar.readable = False

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

##################################################################################
####                                                                          ####
####                               COURSE PAGES                               ####
####                                                                          ####
##################################################################################

def courses():
    courses = db(Course).select()
    return dict(courses=courses)

def course():
    course_id = request.args(0, cast=int)
    course = Course(id=course_id)
    open_classes = course.classes(Class.status == 3).select()
    
    Interest.course.default = course_id
    Interest.course.readable = Interest.course.writable = False
    interest_form = SQLFORM(Interest)
    if interest_form.process(onvalidation=check_if_exists).accepted:
        response.flash = T("Thank you!")
    elif interest_form.errors:
        response.flash = T("Erros no formulário!")
        
    return dict(
        course=course,
        open_classes=open_classes,
        interest_form=interest_form)

def enroll():
    class_id = request.args(0, cast=int)

    if not class_id in session.cart:
        session.cart.append(class_id)
    else:
        session.flash = T('This course is already on your shopping cart!')

    redirect(URL('payments', 'shopping_cart'))

@auth.requires_login()
def my_courses():
    class_ids = db(Student.student == auth.user.id).select()
    my_courses = db(Course.course_owner == auth.user.id).select()
    classes = db(Class.id.belongs([x.class_id for x in class_ids])|\
                Class.course.belongs([x.id for x in my_courses])).select()
    return dict(classes=classes)

@auth.requires(lambda: enrolled_in_class(record_id=request.args(0, cast=int), record_type=1) | auth.has_membership("Admin"))
def my_class():
    class_id = request.args(0, cast=int)
    my_class = Class(id=class_id)
    my_course = my_class.course
    modules = db(Module.course_id == my_course).select()
    return dict(my_class=my_class, 
                modules=modules)

@auth.requires(lambda: enrolled_in_class(record_id=request.args(0, cast=int), record_type=2) | auth.has_membership("Admin"))
def lesson():
    lesson_id = request.args(0, cast=int)
    class_id = request.args(1, cast=int)
    lesson = Lesson(id=lesson_id)
    if db(Schedule_Lesson.lesson_id == lesson_id).select().first().release_date > request.now.date():
        raise HTTP(404)

    page = int(request.vars.page or 1)

    videos = lesson.videos.select()
    texts = lesson.texts.select()
    exercises = lesson.exercises.select()

    merged_records = itertools.chain(videos, texts, exercises)
    contents = sorted(merged_records, key=lambda record: record['place'])

    if page <= 0 or page > len(contents):
        raise HTTP(404)

    is_correct = {}
    if request.vars:
        keys = request.vars.keys()
        for key in keys:
            if key != 'page':
                q_id = int(key.split('_')[1])
                question = Exercise(id=q_id)
                if question.correct == int(request.vars[key]):
                    is_correct[key] = True
                else:
                    is_correct[key] = False

    return dict(lesson=lesson,
                content=contents[page-1],
                total_pages=len(contents),
                is_correct=is_correct,
                class_id=class_id)

@auth.requires(lambda: enrolled_in_class(record_id=request.args(0, cast=int), record_type=1) | auth.has_membership("Admin"))
def forum():
    class_id = request.args(0, cast=int)
    topics = db(Forum.class_id == class_id).select(orderby=~Forum.created_on)
    return dict(topics=topics,
                class_id=class_id)

@auth.requires(lambda: enrolled_in_class(record_id=request.args(0, cast=int), record_type=3) | auth.has_membership("Admin"))
def topic():
    topic_id = request.args(0, cast=int)
    topic = Forum(id=topic_id)
    comments = db(Comment.post == topic_id).select()

    Comment.post.default = topic_id
    Comment.post.readable = Comment.post.writable = False
    form = crud.create(Comment, next=URL('topic', args=topic_id))

    return dict(topic=topic,
                comments=comments,
                form=form)

@auth.requires(lambda: enrolled_in_class(record_id=request.args(0, cast=int), record_type=1) | auth.has_membership("Admin"))
def new_topic():
    class_id = request.args(0, cast=int)
    Forum.class_id.default = class_id
    Forum.class_id.readable = Forum.class_id.writable = False
    form = SQLFORM(Forum)
    if form.process().accepted:
        redirect(URL('topic', args=form.vars.id))
    return dict(form=form)

@auth.requires(lambda: enrolled_in_class(record_id=request.args(0, cast=int), record_type=1) | auth.has_membership("Admin"))
def calendar():
    class_id = request.args(0, cast=int)
    dates = db((Date.class_id == class_id)|(Date.class_id == None)).select()
    my_class = Class(id=class_id)
    modules = db(Module.course_id == my_class.course).select()
    lessons = []
    for module in modules:
        for lesson in module.lessons.select():
            lessons.append(lesson)
    return dict(dates=dates,
                my_class=my_class,
                lessons=lessons)

@auth.requires(lambda: enrolled_in_class(record_id=request.args(0, cast=int), record_type=1) | auth.has_membership("Admin"))
def announcements():
    class_id = request.args(0, cast=int)
    announcements = db(Announcement.class_id == class_id).select()
    return dict(announcements=announcements,
                class_id=class_id)