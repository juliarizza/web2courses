# -*- coding: utf-8 -*-

## courses table
Course = db.define_table("courses",
               Field("title", label=T('Title')),
               Field("short_description", "text", label=T('Short Description')),
               Field("description", "text", widget=ckeditor.widget, label=T('Description')),
               Field("price", "float", default=0, label=T('Price')),
               Field("discount", "float", default=0, label=T('Discount')),
               Field("max_students", "integer", default=10, label=T('Max Students')),
               Field("total_hours", "integer", default=10, label=T('Total Hours')),
               Field("banner", "upload", label=T('Banner')),
               Field("icon", "upload", label=T('Icon')),
               Field("course_owner", "reference auth_user", label=T('Owner'))
              )

## classes table
Class = db.define_table("classes",
                        Field("course", "reference courses", label=T('Course')),
                        Field("start_date", "date", label=T('Start Date')),
                        Field("end_date", "date", label=T('End Date')),
                        Field("available_until", "date", label=T('Available Until')),
                        Field("status", label=T('Status'))
                       )

## students table
Student = db.define_table("students",
                Field("student", "reference auth_user", label=T('Student')),
                Field("class_id", "reference classes", label=T('Class Id'))
               )

## modules table
Module = db.define_table("modules",
               Field("title", label=T('Title')),
               Field("description", "text", widget=ckeditor.widget, label=T('Description')),
               Field("place", "integer", label=T('Place')),
               Field("course_id", "reference courses", label=T('Course Id'))
              )

## single lesson table
Lesson = db.define_table("lessons",
                Field("title", label=T('Title')),
                Field("lesson_module", "reference modules", label=T('Module')),
                Field("place", "integer", label=T('Place'))
               )

## schedule lessons table
Schedule_Lesson = db.define_table("schedule_lessons",
                Field("lesson_id", "reference lessons", label=T('Lesson Id')),
                Field("class_id", "reference classes", label=T('Class Id')),
                Field("release_date", "date", label=T('Release Date'))
              )

## video lesson table
Video = db.define_table("videos",
              Field("video_url", label=T('Video URL')),
              Field("video_upload", "upload",label=T('Upload Video')),
              Field("place", "integer", label=T('Place')),
              Field("lesson", "reference lessons", label=T('Lesson')),
              Field("lesson_type", "integer", default=1, label=T('Lesson Type'))
             )

## text lesson table
Text = db.define_table("texts",
             Field("body", "text", widget=ckeditor.widget, label=T('Body')),
             Field("place", "integer", label=T('Place')),
             Field("lesson", "reference lessons", label=T('Lesson')),
             Field("lesson_type", "integer", default=2, label=T('Lesson Type'))
            )

## exercise lesson table
Exercise = db.define_table("exercises",
                 Field("question", "text", widget=ckeditor.widget, label=T('Question')),
                 Field("alternative_a", label=T('Alternative A')),
                 Field("alternative_b", label=T('Alternative B')),
                 Field("alternative_c", label=T('Alternative C')),
                 Field("alternative_d", label=T('Alternative D')),
                 Field("correct", "integer", label=T('Correct Alternative')),
                 Field("place", "integer", label=T('Place')),
                 Field("lesson", "reference lessons", label=T('Lesson')),
                 Field("lesson_type", "integer", default=3, label=T('Lesson Type'))
                )

## track lesson table
Track = db.define_table("tracks",
            Field("user_id", "reference auth_user", label=T('User Id')),
            Field("user_class", "reference classes", label=T('User Class')),
            Field("lesson", "reference lessons", label=T('User Lesson'))
            )

## calendar table
Date = db.define_table("dates",
             Field("title", label=T('Title')),
             Field("marked_date", "date", label=T('Date')),
             Field("class_id", "reference classes", label=T('Class Id'))
            )

## forum table
Forum = db.define_table("forum",
              Field("title", label=T('Title')),
              Field("body", "text", widget=ckeditor.widget, label=T('Body')),
              Field("class_id", "reference classes", label=T('Class Id')),
              auth.signature
             )

## forum comments table
Comment = db.define_table("comments",
                Field("body", "text", widget=ckeditor.widget, label=T('Body')),
                Field("post", "reference forum", label=T('Post')),
                auth.signature
               )

## course interest table
Interest = db.define_table("interests",
             Field("email", label=T('E-mail')),
             Field("course", "reference courses", label=T('Course')),
             auth.signature
             )

## teacher's announcement table
Announcement = db.define_table("announcements",
             Field("title", label=T('Title')),
             Field("body", "text", widget=ckeditor.widget, label=T('Body')),
             Field("class_id", "reference classes", label=T('Class Id'))
             )

## certificates' info
Certificate = db.define_table("certificates",
             Field("bg_template", "upload", label=T('Template')),
             Field("class_id", "reference classes", label=T('Class Id')),
             Field("teacher_signature", "upload", label=T('Signature'))
             )

######################
### PAYMENT TABLES ###
######################

## register user's orders
Order = db.define_table('orders',
            Field('user_id', 'reference auth_user', label=T('User Id')),
            Field('order_date', 'datetime', label=T('Order Date')),
            Field('products', 'list:reference classes', label=T('Products')),
            Field('amount', 'double', label=T('Amount')),
            Field('status', label=T('Status')),
            Field('token', label=T('Token'))
            )

## stores pending transactions to connect to payment services
Pending = db.define_table('pending_transactions',
            Field('order_id', 'reference orders', label=T('Order Id')),
            Field('confirmed', 'boolean', default=False, label=T('Confirmed')),
            auth.signature
            )

## stores confirmed transactions to register user's payments
Confirmed = db.define_table('confirmed_transactions',
            Field('order_id', 'reference orders', label=T('Order Id')),
            Field('pending_id', 'reference pending_transactions', ondelete='SET NULL', label=T('Pending Id')),
            Field('confirmation_time', 'datetime', label=T('Confirmation Time')),
            auth.signature
            )