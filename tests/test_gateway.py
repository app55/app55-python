
from app55 import config, dao, gateway
from http import urlopener, httperror

gateway = gateway.Gateway(config.Environment('127.0.0.1', '0', False, 1), 'API_KEY', 'API_SECRET')

def test_create_card():	
	def callback(request):
		assert request.get_method() == 'POST'
		assert request.get_full_url() == 'http://127.0.0.1:0/v1/card'
		assert request.get_data() == 'card.country=GB&card.street=Street'
		return '{"a":1,"api_key":"API_KEY","sig":"F4cz8QVndl1MfC-MiBD6MXAyleM=","ts":"20130101000000"}'
	gateway.url_opener.open = urlopener(callback)
	response = gateway.create_card(
		card = dao.Card(
			street = 'Street',
			country = dao.Country.GBR
		)
	).send()
	assert response.a == 1


def test_delete_card():	
	def callback(request):
		assert request.get_method() == 'DELETE'
		assert request.get_full_url() == 'http://127.0.0.1:0/v1/card/fGFdD'
		assert request.get_data() == 'user.id=1'
		return '{"a":1,"api_key":"API_KEY","sig":"F4cz8QVndl1MfC-MiBD6MXAyleM=","ts":"20130101000000"}'
	gateway.url_opener.open = urlopener(callback)
	response = gateway.delete_card(
		user = dao.User(
			id = 1
		),
		card = dao.Card(
			token = 'fGFdD'
		)
	).send()
	assert response.a == 1

def test_list_cards():	
	def callback(request):
		assert request.get_method() == 'GET'
		assert request.get_full_url() == 'http://127.0.0.1:0/v1/card?user.id=1'
		assert request.get_data() is None 
		return '{"a":1,"cards":[{"token":1},{"token":2}],"api_key":"API_KEY","sig":"F4cz8QVndl1MfC-MiBD6MXAyleM=","ts":"20130101000000"}'
	gateway.url_opener.open = urlopener(callback)
	response = gateway.list_cards(
		user = dao.User(
			id=1
		)
	).send()
	assert response.cards[0].token == 1
	assert response.cards[1].token == 2

def test_create_transaction():	
	def callback(request):
		assert request.get_method() == 'POST'
		assert request.get_full_url() == 'http://127.0.0.1:0/v1/transaction'
		assert request.get_data() == 'user.id=1' 
		return '{"a":1,"api_key":"API_KEY","sig":"F4cz8QVndl1MfC-MiBD6MXAyleM=","ts":"20130101000000"}'
	gateway.url_opener.open = urlopener(callback)
	response = gateway.create_transaction(
		user = dao.User(
			id=1
		)
	).send()
	assert response.a == 1

def test_commit_transaction():	
	def callback(request):
		assert request.get_method() == 'POST'
		assert request.get_full_url() == 'http://127.0.0.1:0/v1/transaction/1'
		assert request.get_data() == 'user.id=1' 
		return '{"a":1,"api_key":"API_KEY","sig":"F4cz8QVndl1MfC-MiBD6MXAyleM=","ts":"20130101000000"}'
	gateway.url_opener.open = urlopener(callback)
	response = gateway.commit_transaction(
		user = dao.User(
			id=1
		),
		transaction = dao.Transaction(
			id=1
		)
	).send()
	assert response.a == 1

def test_create_user():	
	def callback(request):
		assert request.get_method() == 'POST'
		assert request.get_full_url() == 'http://127.0.0.1:0/v1/user'
		assert request.get_data() == 'user.email=example%40app55.com' 
		return '{"a":1,"api_key":"API_KEY","sig":"F4cz8QVndl1MfC-MiBD6MXAyleM=","ts":"20130101000000"}'
	gateway.url_opener.open = urlopener(callback)
	response = gateway.create_user(
		user = dao.User(
			email='example@app55.com'
		),
	).send()
	assert response.a == 1

def test_authenticate_user():	
	def callback(request):
		assert request.get_method() == 'POST'
		assert request.get_full_url() == 'http://127.0.0.1:0/v1/user/authenticate'
		assert request.get_data() == 'user.id=1' 
		return '{"a":1,"api_key":"API_KEY","sig":"F4cz8QVndl1MfC-MiBD6MXAyleM=","ts":"20130101000000"}'
	gateway.url_opener.open = urlopener(callback)
	response = gateway.authenticate_user(
		user = dao.User(
			id=1
		),
	).send()
	assert response.a == 1

def test_update_user():	
	def callback(request):
		assert request.get_method() == 'POST'
		assert request.get_full_url() == 'http://127.0.0.1:0/v1/user/1'
		assert request.get_data() == 'user.email=example%40app55.com' 
		return '{"a":1,"api_key":"API_KEY","sig":"F4cz8QVndl1MfC-MiBD6MXAyleM=","ts":"20130101000000"}'
	gateway.url_opener.open = urlopener(callback)
	response = gateway.update_user(
		user = dao.User(
			id=1,
			email='example@app55.com'
		),
	).send()
	assert response.a == 1
