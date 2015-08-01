# web2courses
A manager system for a teacher to sell/provide courses and manage classes.

**Live demo:** [http://juliarizza.pythonanywhere.com/web2courses](http://juliarizza.pythonanywhere.com/web2courses)

**username/email:** admin@admin.com **password:** admin

## Features
* Let teachers provide online courses
* Lessons with 3 diferent types of content: video, text and questions
* Forum for student's questions
* Calendar for each class

## TODOs
* Configure authorization system with 2 main user categories: student and teacher **DONE**
* Integrate with payment systems (paypal, PagSeguro, etc) **PAYPAL DONE**
* Track students completion of courses 
* Make a .pdf certificate generator **DONE**
* Make a billboard for teacher announcement **DONE**
* Implement a beautiful theme
* Configure routes **DONE**
* Remove extra css, js and images that are not being used **DONE**

## Install
1. Download web2py: [http://web2py.com](http://web2py.com)
2. Clone this repository inside web2py applications folder: `git clone https://github.com/juliarizza/web2courses.git`
3. Configure routes:

	3.1 Create a file called `routes.py` inside web2py root directory.

	3.2 Copy this code in your `routes.py` created:
	```
	routers = dict(

    # base router
    BASE=dict(
	        default_application='web2courses',
	    ),
	)
	```
4. Run web2py: `python web2py.py`
5. Access `http://localhost:8000`
6. To activate the classes scheduler to change classes status automatically, do:
	
	6.1 Run scheduler in another instance, alongside the server: `python web2py/web2py.py -K web2courses`

	6.2 Or run scheduler alongside the server in the embedded webserver: 'python web2py/web2py.py -a your_password -K web2courses -X' (This is only used when you run web2py without the web2py start window)

### Contribute!
Copyright (c) 2015 Júlia Rizza & licensed under The MIT License (MIT)
