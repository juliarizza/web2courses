# -*- coding: utf-8 -*-
from gluon.scheduler import Scheduler

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    sch_db = DAL(myconf.take('sch_db.uri'), pool_size=myconf.take('sch_db.pool_size', cast=int), check_reserved=['all'])
else:
	sch_db = db

def check_classes_status():
	classes = db(Class.status != 2).select()
	log_in_file('Checking for open classes...', path='/tmp/scheduler.log')
	for course_class in classes:
		if int(course_class.status) == 1 and course_class.end_date < request.now.date():
			log_in_file('Course %s being closed.' % course_class.course.id, path='/tmp/scheduler.log')
			course_class.update_record(status=2)
		elif int(course_class.status) == 3 and course_class.start_date <= request.now.date():
			log_in_file('Course %s in progress.' % course_class.course.id, path='/tmp/scheduler.log')
			course_class.update_record(status=1)
	db.commit()
	log_in_file('All status updated!', path='/tmp/scheduler.log')


scheduler = Scheduler(sch_db, tasks=dict(check_classes_status=check_classes_status))

if sch_db(sch_db.scheduler_task).count() == 0:
	## do check_classes_status once by day (86400 seconds = 24 hours)
	## repeats = 0 means it will repeat forever
	## it starts at midnight after you have created it
	import datetime
	today_midnight = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
	start_time = today_midnight+datetime.timedelta(days=1)
	sched = scheduler.queue_task('check_classes_status', start_time=start_time, period=86400, repeats=0)
	log_in_file('New scheduler created: ID %d'%sched.id, path='/tmp/scheduler.log')