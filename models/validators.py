# -*- coding: utf-8 -*-

class_status = {1: T("In Progress"), 2: T("Closed"), 3: T("Open Enrollment")}


## courses table
Course.title.requires = IS_NOT_EMPTY()
Course.price.requires = IS_NOT_EMPTY()
Course.discount.requires = IS_NOT_EMPTY()
Course.max_students.requires = IS_NOT_EMPTY()
Course.total_hours.requires = IS_NOT_EMPTY()
Course.image.requires = IS_EMPTY_OR(IS_IMAGE())
Course.course_owner.requires = IS_IN_DB(db, 'auth_user.id', "%(email)s")

## classes table
Class.start_date.requires = IS_DATE()
Class.end_date.requires = IS_DATE()
Class.course.requires = IS_IN_DB(db, "courses.id", "%(title)s")
Class.status.requires = IS_IN_SET(class_status)

## students table
Student.student.requires = IS_IN_DB(db, "auth_user.id", "%(first_name)s %(last_name)s")
Student.class_id.requires = IS_IN_DB(db, "classes.id", "%(course)s - %(id)d")

## modules table
Module.class_id.requires = IS_IN_DB(db, "classes.id", "%(course)s - %(start_date)s")
Module.class_id.writable = Module.class_id.readable = False
Module.place.writable = Module.place.readable = False

## single lessons table
Lesson.title.requires = IS_NOT_EMPTY()
Lesson.start_date.requires = IS_DATE()
Lesson.lesson_module.requires = IS_IN_DB(db, "modules.id", "%(title)s")
Lesson.lesson_module.writable = Lesson.lesson_module.readable = False
Lesson.place.writable = Lesson.place.readable = False

## video lessons table
Video.lesson.requires = IS_IN_DB(db, "lessons.id", "%(title)s")
Video.lesson_type.writable = Video.lesson_type.readable = False
Video.place.writable = Video.place.readable = False
Video.lesson.writable = Video.lesson.readable = False

## text lessons table
Text.lesson.requires = IS_IN_DB(db, "lessons.id", "%(title)s")
Text.lesson_type.writable = Text.lesson_type.readable = False
Text.place.writable = Text.place.readable = False
Text.lesson.writable = Text.lesson.readable = False

## exercise lessons table
Exercise.lesson.requires = IS_IN_DB(db, "lessons.id", "%(title)s")
Exercise.correct.requires = IS_IN_SET({1:"A",2:"B",3:"C",4:"D"})
Exercise.lesson_type.writable = Exercise.lesson_type.readable = False
Exercise.place.writable = Exercise.place.readable = False
Exercise.lesson.writable = Exercise.lesson.readable = False

## track lessons table
Track.user_id.requires = IS_IN_DB(db, "auth_user.id", "%(first_name)s %(last_name)s")
Track.user_class.requires = IS_IN_DB(db, "classes.id", "%(course)s")
Track.lesson.requires = IS_IN_DB(db, "lessons.id", "%(title)s")

## calendar table
Date.marked_date.requires = IS_DATE()
Date.class_id.requires = IS_EMPTY_OR(IS_IN_DB(db, "classes.id", "%(course)s - %(start_date)s"))

## forum table
Forum.author.requires = IS_IN_DB(db, "auth_user.id", "%(first_name)s %(last_name)s")
Forum.created_on.requires = IS_DATE()
Forum.class_id.requires = IS_IN_DB(db, "classes.id", "%(course)s - %(id)d")
Forum.created_on.readable = Forum.created_on.writable = False

## forum comments table
Comment.author.requires = IS_IN_DB(db, "auth_user.id", "%(first_name)s %(last_name)s")
Comment.post.requires = IS_IN_DB(db, "forum.id", "%(title)s")

## courses interest table
Interest.email.requires = IS_EMAIL()
Interest.course.requires = IS_IN_DB(db, 'courses.id', '%(title)s')

## announcements table
Announcement.class_id.requires = IS_IN_DB(db, "classes.id", "%(course)s - %(start_date)s")
Announcement.class_id.writable = Announcement.class_id.readable = False

def check_if_exists(form):
    q1 = (Interest.email == form.vars.email)
    q2 = (Interest.course == form.vars.course)
    if db(q1&q2).count():
        form.errors.email = T("You are already on the list for this course!")
