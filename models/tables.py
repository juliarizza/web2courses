# -*- coding: utf-8 -*-

## courses table
Course = db.define_table("courses",
               Field("title"),
               Field("short_description", "text"),
               Field("description", "text", widget=ckeditor.widget),
               Field("price", "float", default=0),
               Field("discount", "float", default=0),
               Field("max_students", "integer", default=0),
               Field("total_hours", "integer", default=10),
               Field("image", "upload"),
               Field("course_owner", "reference auth_user")
              )

## classes table
Class = db.define_table("classes",
                        Field("course", "reference courses"),
                        Field("start_date", "date"),
                        Field("end_date", "date"),
                        Field("status")
                       )

## students table
Student = db.define_table("students",
                Field("student", "reference auth_user"),
                Field("class_id", "reference classes")
               )

## modules table
Module = db.define_table("modules",
               Field("title"),
               Field("description", "text", widget=ckeditor.widget),
               Field("place", "integer"),
               Field("class_id", "reference classes")
              )

## single lesson table
Lesson = db.define_table("lessons",
                Field("title"),
                Field("lesson_module", "reference modules"),
                Field("place", "integer"),
                Field("start_date", "date")
               )

## video lesson table
Video = db.define_table("videos",
              Field("video_url"),
              Field("video_upload", "upload"),
              Field("place", "integer"),
              Field("lesson", "reference lessons"),
              Field("lesson_type", "integer", default=1)
             )

## text lesson table
Text = db.define_table("texts",
             Field("body", "text", widget=ckeditor.widget),
             Field("place", "integer"),
             Field("lesson", "reference lessons"),
             Field("lesson_type", "integer", default=2)
            )

## exercise lesson table
Exercise = db.define_table("exercises",
                 Field("question", "text", widget=ckeditor.widget),
                 Field("alternative_a"),
                 Field("alternative_b"),
                 Field("alternative_c"),
                 Field("alternative_d"),
                 Field("correct", "integer"),
                 Field("place", "integer"),
                 Field("lesson", "reference lessons"),
                 Field("lesson_type", "integer", default=3)
                )

## track lesson table
Track = db.define_table("tracks",
            Field("user_id", "reference auth_user"),
            Field("user_class", "reference classes"),
            Field("lesson", "reference lessons")
            )

## calendar table
Date = db.define_table("dates",
             Field("title"),
             Field("marked_date", "date"),
             Field("class_id", "reference classes")
            )

## forum table
Forum = db.define_table("forum",
              Field("title"),
              Field("body", "text", widget=ckeditor.widget),
              Field("author", "reference auth_user"),
              Field("created_on", "date", default=request.now),
              Field("class_id", "reference classes")
             )

## forum comments table
Comment = db.define_table("comments",
                Field("body", "text", widget=ckeditor.widget),
                Field("author", "reference auth_user"),
                Field("post", "reference forum")
               )

## Course interest table
Interest = db.define_table("interests",
             Field("email"),
             Field("course", "reference courses")
             )

Announcement = db.define_table("announcements",
             Field("title"),
             Field("body", "text", widget=ckeditor.widget),
             Field("class_id", "reference classes")
             )