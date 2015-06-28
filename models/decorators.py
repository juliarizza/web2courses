# -*- coding: utf-8 -*-

def enrolled_in_class(record_id, record_type):
	if db((Student.class_id == class_id)\
		&(Student.student == auth.user.id)).count():
		return True
	else:
		return False