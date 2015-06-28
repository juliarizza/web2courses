# -*- coding: utf-8 -*-

##################################################################################
####                                                                          ####
####                              TEACHER PAGES                               ####
####                                                                          ####
##################################################################################

@auth.requires_login()
def courses():
    courses = db(Course).select()
    return dict(courses=courses)

@auth.requires_login()
def classes():
    if request.vars.course:
        course_id = int(request.vars.course)
        classes = db(Class.course == course_id).select(orderby=~Class.start_date)
    else:
        classes = db(Class).select(orderby=Class.course|~Class.start_date)
    return dict(classes=classes)

@auth.requires_login()
def lessons():
    import itertools

    try:
        class_id = request.args(0,cast=int)
    except:
        redirect(URL('default', 'index'))

    modules = db(Module.class_id == class_id).select()

    all_lessons = {}
    for module in modules:
        for lesson in module.lessons.select():
            videos = lesson.videos.select()
            texts = lesson.texts.select()
            exercises = lesson.exercises.select()
            merged_records = itertools.chain(videos, texts, exercises)
            contents = sorted(merged_records, key=lambda record: record['place'])
            all_lessons["m%d_l%d" % (module.id, lesson.id)] = contents

    return dict(modules=modules,
                all_lessons=all_lessons)

@auth.requires_login()
def pick_type():
    form = SQLFORM.factory(
        Field('type', requires=IS_IN_SET({4: T('Video'), 5: T('Text'), 6: T('Question')}))
        )
    if form.process().accepted:
        redirect(URL('new', args=[int(form.vars.type), request.args(0)], vars=request.vars))
    elif form.errors:
        response.flash(T('Form has errors!'))
    return dict(form=form)

##################################################################################
####                                                                          ####
####                   CRUD PAGES FOR COURSES, CLASSES, ETC                   ####
####                                                                          ####
##################################################################################

@auth.requires_login()
def new():
    tables = [Course, Class, Module, Lesson, Video, Text, Exercise]
    table_type = request.args(0,cast=int)

    if table_type == 2:
        Module.class_id.default = request.args(1,cast=int)
        Module.place.default = db(Module.class_id == request.args(1,cast=int)).count()
    elif table_type == 3:
        Lesson.lesson_module.default = request.args(1,cast=int)
        Lesson.place.default = db(Lesson.lesson_module == request.args(1,cast=int)).count()
    elif table_type in [4, 5, 6]:
        lesson = db(Lesson.id == request.args(1,cast=int)).select().first()
        counter = lesson.videos.count() + lesson.texts.count() + lesson.exercises.count()
        if table_type == 4:
            Video.place.default = counter
            Video.lesson.default = request.args(1,cast=int)
        elif table_type == 5:
            Text.place.default = counter
            Text.lesson.default = request.args(1,cast=int)
        elif table_type == 6:
            Exercise.place.default = counter
            Exercise.lesson.default = request.args(1,cast=int)

    form = SQLFORM(tables[table_type]).process(next=request.vars.next)
    return dict(form=form)

@auth.requires_login()
def edit():
    tables = [Course, Class, Module, Lesson, Video, Text, Exercise]
    table_type = request.args(0,cast=int)
    record_id = request.args(1,cast=int)

    form = SQLFORM(tables[table_type], record_id).process(next=request.vars.next)
    return dict(form=form)

@auth.requires_login()
def delete():
    tables = [Course, Class, Module, Lesson, Video, Text, Exercise]
    table_type = request.args(0,cast=int)
    record_id = request.args(1,cast=int)
    db(tables[table_type]==record_id).delete()
    redirect(request.vars.next)

