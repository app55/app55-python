# -*- coding: latin-1 -*-
import os, sys, time, urllib2
sys.path.insert(0, os.path.dirname(__file__)) 

import app55
from datetime import datetime, timedelta

gateway = app55.Gateway(getattr(app55.Environment, os.environ.get('APP55_API_ENVIRONMENT', 'Development')), os.environ.get('APP55_API_KEY', 'cHvG680shFTaPWhp8RHhGCSo5QbHkWxP'), os.environ.get('APP55_API_SECRET', 'zMHzGPF3QAAQQzTDoTGtGz8f5WFZFjzM')) 

def create_user(email=lambda: 'example.%s@app55.com' % datetime.utcnow().strftime('%Y%m%d%H%M%S'), phone=lambda: '0123 456 7890', password=lambda: 'pa55word', confirm_password=None, first_name=lambda: 'APPFIVEFIVE', last_name=lambda: 'USER'):
	email = email() if callable(email) else email
	phone = phone() if callable(phone) else phone
	password = password() if callable(password) else password
	confirm_password = confirm_password if callable(confirm_password) else confirm_password
	confirm_password = confirm_password or password
	first_name = first_name() if callable(first_name) else first_name
	last_name = last_name() if callable(last_name) else last_name

	print "Creating user %s..." % email,
	
	response = gateway.create_user(
		user = app55.User(
			email = email,
			phone = phone,
			password = password,
			password_confirm = confirm_password,
			name = app55.Name( 
				first = first_name,
				last = last_name
			)
		)
	).send()
	print "DONE (user-id %s)" % response.user.id
	return response

def get_user(id):
	print "Getting user %s..." % id,

	response = gateway.get_user(
		user = app55.User(
			id = id
		)
	).send()
	print "DONE"
	return response

def create_card(user, number='4111111111111111', ip_address=None, threeds=False):
	print "Creating card...",
	response = gateway.create_card(
		ip_address = ip_address,
		user = app55.User(
			id = user.id
		),
		card = app55.Card(
			holder_name = 'App55 User',
			number = number,
			expiry = (datetime.utcnow() + timedelta(days=90)).strftime('%m/%Y'),
			security_code = '111',
			address = app55.Address(
				street = '8 Exchange Quay',
				city = 'Manchester',
				postal_code = 'M5 3EJ',
				country = 'GB',
			),
		),
		threeds=threeds
	).send()
	print "DONE (card-token %s)" % response.card.token
	return response

def list_cards(user):
	print "Listing cards...",
	response = gateway.list_cards(
		user = app55.User(
			id = user.id
		)
	).send()
	print "DONE (%s cards)" % len(response.cards)
	return response

def delete_card(user, card):
	print "Deleting card %s..." % card.token,
	response = gateway.delete_card(
		user = app55.User(
			id = user.id
		),
		card = app55.Card(
			token = card.token,
		)
	).send()
	print "DONE"
	return response

def create_transaction(user, card, id=None, commit=False, source=None, type=None, ip_address=None, threeds=False):
	print "Creating transaction...",
	response = gateway.create_transaction(
		ip_address = ip_address,
		user = app55.User(
			id = user.id,
		),
		card = app55.Card(
			token = card.token,
		),
		transaction = app55.Transaction(
			id = id,
			source = source,
			type = type,
			amount = "0.10",
			currency = 'EUR',
			commit = commit
		),
		threeds=threeds,
	).send()
	print "DONE (transaction-id %s)" % response.transaction.id
	return response

def create_anonymous_transaction(card = None, id=None, source=None, type=None, ip_address=None, email=None, threeds=False):
	print "Creating anonymous transaction...",
	response = gateway.create_transaction(
		ip_address = ip_address,
		threeds = threeds,
		user = app55.User(
			email = email,
		),
		card = card or app55.Card(
			holder_name = 'App55 User',
			number = '4111111111111111',
			expiry = (datetime.utcnow() + timedelta(days=90)).strftime('%m/%Y'),
			security_code = '111',
			address = app55.Address(
				street = '8 Exchange Quay',
				city = 'Manchester',
				postal_code = 'M5 3EJ',
				country = 'GB',
			),
		),
		transaction = app55.Transaction(
			id = id,
			source = source,
			type = type,
			amount = '0.10',
			currency = 'EUR',
		),
	).send()
	print "DONE (transaction-id %s)" % response.transaction.id
	return response

def commit_transaction(transaction):
	print "Committing transaction...",
	response = gateway.commit_transaction(
		transaction = app55.Transaction(
			id = transaction.id
		)
	).send()
	print "DONE"
	return response

def create_schedule(user, card, amount='0.10'):
	print "Creating schedule...",
	response = gateway.create_schedule(
		user = app55.User(
			id = user.id
		),
		card = app55.Card(
			token = card.token
		),
		transaction = app55.Transaction(
			amount = amount,
			currency = 'GBP',
			description = 'Scheduled Transaction for £' + str(amount)
		),
		schedule = app55.Schedule(
			time_unit = 'daily',
			start = datetime.utcnow().strftime('%Y-%m-%d'),
		),
	).send()
	print "DONE (schedule %s)" % response.schedule.id
	return response

def get_schedule(user, schedule):
	print "Getting schedule...",
	response = gateway.get_schedule(
		user = app55.User(
			id = user.id
		),
		schedule = app55.Schedule(
			id = schedule.id
		)
	).send()
	print "DONE"
	return response

def update_schedule(user, card, schedule):
	print "Updating schedule...",
	response = gateway.update_schedule(
		user = app55.User(
			id = user.id
		),
		schedule = app55.Schedule(
			id = schedule.id,
			end = schedule.end
		),
		card = app55.Card(
			token = card.token,
		)
	).send()
	print "DONE"
	return response

def list_schedules(user, active=None):
	print "Listing schedules...",
	response = gateway.list_schedules(
		user = app55.User(
			id = user.id,
		),
		active=active
	).send()
	print "DONE (%s schedules)" % len(response.schedules)
	return response

def delete_schedule(user, schedule):
	print "Deleting schedule...",
	response  = gateway.delete_schedule(
		user = app55.User(
			id = user.id,
		),
		schedule = app55.Schedule(
			id = schedule.id,
		),
	).send()
	print "DONE"
	return response

def multiple_transactions(user, card, *types):
	print "Testing transactions of types", types
	transaction = app55.Transaction(id=None)
	for type in types:
		transaction = create_transaction(user, card, id=transaction.id, type=type, ip_address='127.0.0.1').transaction
		commit_transaction(transaction)
	return transaction

def duplicate_transactions(user, card, *types):
	try:
		multiple_transactions(user, card, *types)
		raise AssertionError()
	except app55.RequestException, e:
		assert str(e) == 'Duplicate transaction.', e

def multiple_anonymous_transactions(*types):
	print "Testing anonymous transactions of types", types
	transaction = app55.Transaction(id=None)
	for type in types:
		transaction = create_anonymous_transaction(id=transaction.id, type=type, ip_address='127.0.0.1', email='example@app55.com').transaction
		commit_transaction(transaction)
	return transaction

def duplicate_anonymous_transactions(*types):
	try:
		multiple_anonymous_transactions(*types)
		raise AssertionError()
	except app55.RequestException, e:
		assert str(e) == 'Duplicate transaction.', e

if __name__ == '__main__':

	print "App55 %s - API Key <%s>" % (os.environ.get('APP55_API_ENVIRONMENT', 'Development'), gateway.api_key)
	print
	
	transaction = create_anonymous_transaction(ip_address='127.0.0.1').transaction
	commit_transaction(transaction)

	user = create_user().user
	user_check = get_user(user.id).user
	assert user.id == user_check.id
	assert user.email == user_check.email
	assert user.name.first == user_check.name.first
	assert user.name.last == user_check.name.last

	card1 = create_card(user, ip_address='127.0.0.1').card
	transaction = create_transaction(user, card1, ip_address='127.0.0.1').transaction
	commit_transaction(transaction)

	card2 = create_card(user, ip_address='127.0.0.1').card
	transaction = create_transaction(user, card2, ip_address='127.0.0.1').transaction
	commit_transaction(transaction)

	card3 = create_card(user, ip_address='127.0.0.1').card
	transaction = create_transaction(user, card3, ip_address='127.0.0.1').transaction
	commit_transaction(transaction)

	transaction = create_anonymous_transaction(ip_address='127.0.0.1').transaction
	commit_transaction(transaction)


	transaction = create_transaction(user, card3, commit=True, ip_address='127.0.0.1').transaction
	assert transaction.code == 'succeeded'
	assert transaction.auth_code == '06603'
	
	response = create_card(user, ip_address='127.0.0.1', threeds=True)

	assert response.threeds
	response = gateway.url_opener.open(urllib2.Request('%s&next=http://dev.app55.com/v1/echo' % response.threeds, headers={'Accept': 'application/json'})).read()
	response = gateway.response(json=response)
	card_3ds = response.card
	print(response.form_data)
	transaction = create_transaction(user, card_3ds, ip_address='127.0.0.1').transaction
	commit_transaction(transaction)

	card_3ds_ne1 = create_card(user, ip_address='127.0.0.1', number='4543130000001116', threeds=True).card
	transaction = create_transaction(user, card_3ds_ne1, ip_address='127.0.0.1').transaction
	commit_transaction(transaction)


	transaction = create_transaction(user, card1, ip_address='127.0.0.1', threeds=True)
	assert not transaction.transaction.code
	response = gateway.url_opener.open(urllib2.Request('%s&next=http://dev.app55.com/v1/echo' % transaction.threeds, headers={'Accept': 'application/json'})).read()
	response = gateway.response(json=response)
	transaction = gateway.commit_transaction(data=response.form_data, transaction=app55.Transaction(id=transaction.transaction.id)).send().transaction
	assert transaction.code == 'succeeded', transaction.code
	assert transaction.auth_code == '06603', transaction.auth_code

	transaction = create_transaction(user, card1, commit=True, ip_address='127.0.0.1', threeds=True)
	assert not transaction.transaction.code
	response = gateway.url_opener.open(urllib2.Request('%s&next=http://dev.app55.com/v1/echo' % transaction.threeds, headers={'Accept': 'application/json'})).read()
	response = gateway.response(json=response)
	assert response.transaction.code == 'succeeded', response.transaction.code
	assert response.transaction.auth_code == '06603', response.transaction.auth_code

	card_3ds_ne = create_card(user, number='4543130000001116', ip_address='127.0.0.1').card
	transaction = create_transaction(user, card_3ds_ne, ip_address='127.0.0.1', threeds=True, commit=True)
	assert not transaction.threeds, transaction.threeds
	assert transaction.transaction.code == 'succeeded', transaction.transaction.code
	assert transaction.transaction.auth_code == '06603', transaction.transaction.auth_code

	transaction = create_transaction(user, card_3ds_ne, ip_address='127.0.0.1', threeds=True, commit=False)
	assert not transaction.threeds, transaction.threeds
	transaction = commit_transaction(transaction.transaction)
	assert transaction.transaction.code == 'succeeded', transaction.transaction.code
	assert transaction.transaction.auth_code == '06603', transaction.transaction.auth_code


	multiple_transactions(user, card3, 'auth', 'capture', 'void')
	multiple_transactions(user, card3, 'auth', 'void')
	multiple_transactions(user, card3, 'sale', 'void')
	duplicate_transactions(user, card3, 'sale', 'sale')
	duplicate_transactions(user, card3, 'sale', 'auth')
	duplicate_transactions(user, card3, 'sale', 'capture')
	duplicate_transactions(user, card3, 'auth', 'sale')
	duplicate_transactions(user, card3, 'auth', 'auth')
	duplicate_transactions(user, card3, 'auth', 'capture', 'sale')
	duplicate_transactions(user, card3, 'auth', 'capture', 'auth')
	duplicate_transactions(user, card3, 'auth', 'capture', 'capture')
	duplicate_transactions(user, card3, 'sale', 'void', 'void')
	duplicate_transactions(user, card3, 'auth', 'void', 'void')
	duplicate_transactions(user, card3, 'auth', 'capture', 'void', 'void')
	try:
		multiple_transactions(user, card3, 'capture')
		raise AssertionError()
	except app55.CardException, e:
		assert str(e) == 'The payment could not be processed.', e
	try:
		multiple_transactions(user, card3, 'void')
		raise AssertionError()
	except app55.CardException, e:
		assert str(e) == 'The payment could not be processed.', e

	multiple_anonymous_transactions('auth', 'capture', 'void')
	multiple_anonymous_transactions('auth', 'void')
	multiple_anonymous_transactions('sale', 'void')
	duplicate_anonymous_transactions('sale', 'sale')
	duplicate_anonymous_transactions('sale', 'auth')
	duplicate_anonymous_transactions('sale', 'capture')
	duplicate_anonymous_transactions('auth', 'sale')
	duplicate_anonymous_transactions('auth', 'auth')
	duplicate_anonymous_transactions('auth', 'capture', 'sale')
	duplicate_anonymous_transactions('auth', 'capture', 'auth')
	duplicate_anonymous_transactions('auth', 'capture', 'capture')
	duplicate_anonymous_transactions('sale', 'void', 'void')
	duplicate_anonymous_transactions('auth', 'void', 'void')
	duplicate_anonymous_transactions('auth', 'capture', 'void', 'void')
	try:
		multiple_anonymous_transactions('capture')
		raise AssertionError()
	except app55.CardException, e:
		assert str(e) == 'The payment could not be processed.', e
	try:
		multiple_anonymous_transactions('void')
		raise AssertionError()
	except app55.CardException, e:
		assert str(e) == 'The payment could not be processed.', e


	



	schedule1 = create_schedule(user, card1).schedule
	time.sleep(5)
	schedule = get_schedule(user, schedule1).schedule
	assert schedule.end is None
	assert schedule.next == (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d'), schedule.next
	assert schedule.units == 1
	update_schedule(user, card2, app55.Schedule(
		id = schedule.id,
		end = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d'),
	))
	response = get_schedule(user, schedule)
	assert response.schedule.end == (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')
	assert response.card.token == card2.token
	schedule2 = create_schedule(user, card1, amount='0.11').schedule
	schedule3 = create_schedule(user, card3, amount='0.12').schedule
	schedules = list_schedules(user).schedules
	schedules = [schedule.id for schedule in schedules]
	assert schedule1.id in schedules
	assert schedule2.id in schedules
	assert schedule3.id in schedules
	assert len(schedules) == 3
	delete_schedule(user, schedule1)
	delete_schedule(user, schedule2)
	delete_schedule(user, schedule3)
	assert len(list_schedules(user).schedules) == 3
	assert len(list_schedules(user, active=True).schedules) == 0 
	
	
	

	cards = [card.token for card in list_cards(user).cards] 
	assert card1.token in cards
	assert card2.token in cards
	assert card3.token in cards
	assert card_3ds_ne.token in cards
	assert card_3ds.token in cards
	assert card_3ds_ne1.token in cards
	assert len(cards) == 6

	for card in [card1, card2, card3, card_3ds_ne, card_3ds, card_3ds_ne1]:
		delete_card(user, card)

	assert len(list_cards(user).cards) == 0

	email = 'example.%s@app55.com' % datetime.utcnow().strftime('%Y%m%d%H%M%S')
	print "Updating user...",
	gateway.update_user(
		user = app55.User(
			id = user.id,
			email = email,
			password = 'password01',
			password_confirm = 'password01',
		)
	).send()
	print "DONE"

	print "Authenticating user...",	
	user2 = gateway.authenticate_user(
		user = app55.User(
			email = email,
			password = 'password01',
		)
	).send().user
	print "DONE"

	assert user.id == user2.id
	
