import os, sys
sys.path.insert(0, os.path.dirname(__file__)) 

import app55
from datetime import datetime, timedelta

gateway = app55.Gateway(app55.Environment.Sandbox, os.environ.get('APP55_API_KEY'), os.environ.get('APP55_API_SECRET')) 

def create_user(email=lambda: 'example.%s@app55.com' % datetime.utcnow().strftime('%Y%m%d%H%M%S'), phone=lambda: '0123 456 7890', password=lambda: 'pa55word', confirm_password=None):
	email = email() if callable(email) else email
	phone = phone() if callable(phone) else phone
	password = password() if callable(password) else password
	confirm_password = confirm_password if callable(confirm_password) else confirm_password
	confirm_password = confirm_password or password

	print "Creating user %s..." % email,
	
	response = gateway.create_user(
		user = app55.User(
			email = email,
			phone = phone,
			password = password,
			password_confirm = confirm_password
		)
	).send()
	print "DONE (user-id %s)" % response.user.id
	return response

def create_card(user):
	print "Creating card...",
	response = gateway.create_card(
		user = app55.User(
			id = user.id
		),
		card = app55.Card(
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

def create_transaction(user, card):
	print "Creating transaction...",
	response = gateway.create_transaction(
		user = app55.User(
			id = user.id,
		),
		card = app55.Card(
			token = card.token,
		),
		transaction = app55.Transaction(
			amount = "0.10",
			currency = 'GBP',
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

if __name__ == '__main__':
	print "App55 Sandbox - API Key <%s>" % gateway.api_key
	print
	user = create_user().user
	card1 = create_card(user).card
	transaction = create_transaction(user, card1).transaction
	commit_transaction(transaction)

	card2 = create_card(user).card
	transaction = create_transaction(user, card2).transaction
	commit_transaction(transaction)

	card3 = create_card(user).card
	transaction = create_transaction(user, card3).transaction
	commit_transaction(transaction)

	cards = [card.token for card in list_cards(user).cards] 
	assert card1.token in cards
	assert card2.token in cards
	assert card3.token in cards
	assert len(cards) == 3

	for card in [card1, card2, card3]:
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
	
