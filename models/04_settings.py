# -*- coding: utf-8 -*-

## create a shopping cart
session.cart = session.cart or []

## set this to your paypal id
## or your sandbox paypal id
paypal_id = "your@email.com"

## default urls
ipn_handler = URL('payments', 'ipn', host=True, scheme=True)
paypal_return_url = URL('payments', 'success', args='paypal', host=True, scheme=True)