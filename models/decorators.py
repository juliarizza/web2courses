# -*- coding: utf-8 -*-

def enrolled_in_class(record_id, record_type):
	if record_type == 1:
		if db((Student.class_id == record_id)\
			&(Student.student == auth.user.id)).count()\
			|is_course_owner(record_id):
			return True
		else:
			return False
	elif record_type == 2:
		lesson = db(Lesson.id == record_id).select().first()
		if db((Student.class_id == lesson.lesson_module.class_id)\
			&(Student.student == auth.user.id)).count()\
			|is_course_owner(lesson.lesson_module.class_id):
			return True
		else:
			return False
	elif record_type == 3:
		topic = db(Comment.id == record_id).select().first()
		if db((Student.class_id == topic.post.class_id)\
			&(Student.student == auth.user.id)).count()\
			|is_course_owner(topic.post.class_id):
			return True
		else:
			return False

def is_course_owner(class_id):
	class_record = db(Class.id == class_id).select().first()
	if db(Course.id == class_record.course).select().first().course_owner == auth.user.id:
		return True
	else:
		return False