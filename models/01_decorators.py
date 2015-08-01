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
		lesson = Lesson(id=record_id)
		if db((Student.class_id == lesson.lesson_module.class_id)\
			&(Student.student == auth.user.id)).count()\
			|is_course_owner(lesson.lesson_module.class_id):
			return True
		else:
			return False
	elif record_type == 3:
		topic = Forum(id=record_id)
		if db((Student.class_id == topic.class_id)\
			&(Student.student == auth.user.id)).count()\
			|is_course_owner(topic.class_id):
			return True
		else:
			return False

def is_course_owner(class_id):
	class_record = db(Class.id == class_id).select().first()
	if Course(id=class_record.course).course_owner == auth.user.id:
		return True
	else:
		return False

def is_user_order(order_id):
	if Order(id=order_id).user_id == auth.user.id:
		return True
	else:
		return False