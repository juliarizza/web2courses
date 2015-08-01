# -*- coding: utf-8 -*-
import datetime
from uuid import uuid4

## tells if the user can enroll or not in a class
def can_enroll(record):
	student_qty = db(Student.class_id == record.id).count()
	query_1 = (student_qty < record.course.max_students)
	query_2 = (int(record.status) == 3)
	query_3 = (record.start_date >= request.now.date())
	query_4 = ((auth.user and not Student(class_id=record.id, student=auth.user.id)) or not auth.user)
	if query_1 and query_2 and query_3 and query_4:
		return True
	else:
		## even if there is more than one error
		## the button of enrollment will show
		## only if the error is of query_1 or query_4

		## if the course date has passed or it's status
		## is not open for enrollment, there is no need
		## to show any button
		session.errors = {"max_qty": False, "student": False}
		if not query_1:
			session.errors["max_qty"] = True
		if not query_4:
			session.errors["student"] = True
		return False

## calculates the total ammount of a order
def total_amount(record):
	total = 0
	for cart_class in record.products:
		total += cart_class.course.price - cart_class.course.discount
	return total

## generate a random token that is not in the Orders table
def generate_token():
	token = None
	while not token or Order(token=token):
		token = str(uuid4())[:8]
	return token


## creates a log file in the appointed path
def log_in_file(msg, path='/tmp/ipngenerallog.txt'):
	with open(path, "a") as log:
		now = datetime.datetime.now()
		log.write("\n" + now.strftime("%Y-%m-%d %H:%M:%S") + "\n" + msg + "\n")

## writes the log message and generate the file
def write_logs(request):
	message = "-"*80
	message += "\nIPN Received\n"
	message += "ARGS: \n" + str(request.args) + "\n"
	message += "VARS: \n" + str(request.vars) + "\n"
	log_in_file(message)
