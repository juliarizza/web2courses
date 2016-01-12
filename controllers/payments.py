# -*- coding: utf-8 -*-

def shopping_cart():
	
	"""
	This is the user's shopping cart. All courses that
	the user will buy (free or not) are recorded in a
	session until the Buy Now action.
	"""

	classes = []
	amount = 0
	for class_id in session.cart:
		cart_class = Class(id=class_id)
		classes.append(cart_class)
		amount += cart_class.course.price-cart_class.course.discount

	return dict(classes=classes,
				amount=amount)

def remove_from_shopping_cart():
	
	"""
	Just a delete function to remove items from
	the shopping cart.
	"""

	class_id = request.args(0, cast=int)
	session.cart.remove(class_id)
	redirect(URL('shopping_cart'))

@auth.requires_login()
def register_order():
	
	"""
	This function will register the user's shopping cart
	in a database record. This record is a order that
	contains payment info and will serve as a history
	of the user transactions.

	After the order is recorded, the session of the 
	shopping cart will be clean.
	"""

	## if the user were not logged in when it selected classes to enroll
	## then it can select classses it is already enrolled
	## and the classes will be in the shopping cart.
	## to avoid that:
	for class_id in session.cart:
		cart_class = Class(id=int(class_id))
		if not can_enroll(cart_class):
			session.flash = T('You are already enrolled in this class to %s, so we removed it from your shopping cart.') % cart_class.course.title
			session.cart.remove(class_id)
			redirect(URL('shopping_cart'))

	order = Order.insert(
						user_id = auth.user.id,
						order_date = request.now,
						products = [Class(id=cart_class) for cart_class in session.cart],
						status = 1
						)
	session.order = order
	session.cart = []

	message = T("We just received your order number %s:") % order.token
	for product in order.products:
		message += '\n'
		message += T("- %s from %s to %s") % (product.course.title, product.start_date, product.end_date)
	message += '\n'
	message += T("Amount: R$%.2f") % order.amount
	message += '\n\n'
	message += T("We will wait and let you know when your payment is confirmed.")
	message += '\n'
	message += T("Thank you for your purchase!")

	mail.send(to=order.user_id.email,
			subject=T("We received your order!"),
			message=message
			)
	redirect(URL('pay_courses'))

@auth.requires_login()
def pay_courses():

	"""
	This function is responsible to redirect the user
	to the payment method it chose and process if
	the amount to be paid is free. In this case, it will
	enroll the student to the class. Other way, the user
	will be redirected to pay.
	"""

	order = Order(id=session.order)
	if order.amount == 0:
		pending = Pending.insert(
								order_id = session.order,
								confirmed = True
								)
		confirmed = Confirmed.insert(
									order_id=order.id,
									pending_id=pending.id,
									confirmation_time=request.now
									)
		order.update_record(status=2)
		session.pending = pending
		redirect(URL('success'))

		message = T('We just confirmed your payment for order number %s.') % order.token
		message += '\n'
		message += T('The total amount was R$%.2f.') % order.amount
		message += '\n'
		message += T('You can check your payment history after login in to your profile.')
		message += '\n\n'
		message += T('Thank you!')
		mail.send(to=order.user_id.email,
				subject=T("Payment confirmed!"),
				message = message
				)
	else:
		pending = Pending.insert(order_id = order.id)
		session.pending = pending
		redirect(URL('paypal'))

@auth.requires_login()
def paypal():

	"""
	This is a function to submit the user's shopping cart
	to PayPal to proceed with the payment.

	The view of	this function contain a form that 
	passes the values of each product in the shopping
	cart and submit them so PayPal can deal with them.
	"""

	if not session.pending:
		raise HTTP(404)
	pending = Pending(id=session.pending)
	return dict(pending=pending)

def ipn():
	
	"""
	The IPN is the method that PayPal uses to
	return information about the payment.

	This function will receive this info and
	validate it, marking the user's order as
	confirmed or not.

	PayPal only confirm the receipt of this
	information if you return the same info
	it passed to you. So, we return the
	request.vars at the end of the function.
	"""

	import json
	write_logs(request)

	pending = Pending(id=int(request.vars.invoice), confirmed=False)
	if not pending:
		raise HTTP(404)

	already_confirmed = Confirmed(pending_id=pending.id)
	if already_confirmed:
		return dict(status="Already Confirmed", data=already_confirmed)

	if request.vars.payment_status == 'Completed':
		confirmed = Confirmed.insert(
									order_id=pending.order_id,
									pending_id=pending.id,
									confirmation_time=request.now
									)

		pending.update_record(confirmed=True)
		Order(id=pending.order_id).update_record(status=2)

		message = T('We just confirmed your payment for order number %s.') % pending.order_id.token
		message += '\n'
		message += T('The total amount was R$%.2f.') % pending.order_id.amount
		message += '\n'
		message += T('You can check your payment history after login in to your profile.')
		message += '\n\n'
		message += T('Thank you!')
		mail.send(to=pending.order_id.user_id.email,
				subject=T("Payment confirmed!"),
				message = message
				)
	else:
		if request.is_local:
			path = '/tmp/ipn_not_completed.txt'
		else:
			## common path for logs
			path = '/var/log/ipn_not_completed.txt'
		message = '-'*80
		message += '\nIPN NOT COMPLETED\n'
		message += str(request.vars)
		message += '\n'
		log_in_file(message, path)
		Order(id=pending.order_id).update_record(status=3)
		mail_message = T('There was a problem with your payment!')
		mail_message += '\n\n'
		mail_message += T("Something happened and we couldn't verify your payment.")
		mail_message += '\n'
		mail_message += T("If you're sure you paid the order, please contact us. Otherwise, try to pay again later.")
		mail_message += '\n\n'
		mail_message += T("Thank you.")
		mail.send(to=pending.order_id.user_id.email,
				subject=T('Something went wrong!'),
				message = mail_message
				)
	return json.dumps(request.vars)

@auth.requires_login()
def success():
	
	"""
	This function is supposed to show a success or error message
	depending of what PayPal IPN returns.

	Since in localhost we receive no return of PayPal, we can
	hack a little bit in order to make the app continuous.
	"""

	if request.is_local:
		log_in_file(str(request.vars), '/tmp/paypalreturn.txt')
	else:
		log_in_file(str(request.vars), '/var/log/paypalreturn.txt')

	pending = Pending(id=session.pending)
	if request.is_local:
		## do what ipn was supposed to do
		## just for continuity purposes
		confirmed = Confirmed.insert(
									order_id=pending.order_id,
									pending_id=pending.id,
									confirmation_time=request.now
									)
		pending.update_record(confirmed=True)
		Order(id=pending.order_id).update_record(status=2)
		mail_message = T('We just confirmed your payment for order number %s.') % pending.order_id.token
		mail_message += '\n'
		mail_message += T('The total amount was R$%.2f.') % pending.order_id.amount
		mail_message += '\n'
		mail_message += T('You can check your payment history after login in to your profile.')
		mail_message += '\n\n'
		mail_message += T('Thank you!')
		mail.send(to=pending.order_id.user_id.email,
				subject=T("Payment confirmed!"),
				message = mail_message
				)

	if pending.confirmed or request.is_local:
		message = T('Payment completed! Congratulations for your purchase!')
		for cart_class in pending.order_id.products:
			Student.insert(student = auth.user.id, class_id = cart_class)
	else:
		message = T('Sorry! Something bad happened!')
	return dict(message=message)

@auth.requires_login()
def history():
	
	"""
	This function exposes to the user it's
	orders and payment history.
	"""

	history = db(Order.user_id == auth.user.id).select()
	return dict(history=history)

@auth.requires(lambda: is_user_order(order_id=request.args(0, cast=int)))
def details():

	"""
	This function exposes details of the
	user's orders.
	"""

	order = Order(id=request.args(0, cast=int))
	return dict(order=order)