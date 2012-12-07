from app55 import config, dao, errors, gateway, messages
import pytest
from http import urlopener, httperror

messages.Message._timestamp = lambda self: '20130101000000'
gateway = gateway.Gateway(config.Environment('127.0.0.1', '0', False, 1), 'API_KEY', 'API_SECRET')


def test_attrdict():
	assert messages.attrdict(a=1).a == 1
	assert messages.attrdict(a=messages.attrdict(b=1)).a.b == 1
	assert messages.attrdict().a is None

def test_to_dotted():
	assert messages.to_dotted({ 'a': { 'b': { 'c': 1 } } }) == { 'a.b.c': 1 }
	assert messages.to_dotted({ 'a': 1, 'b': { 'c': { 'd': 2 }, 'e': 3 } }) == { 'a': 1, 'b.c.d': 2, 'b.e': 3 }

def test_message_kwargs():
	message = messages.Message(a=1, b=2, c=3, d=4)
	assert message.a == 1
	assert message.b == 2
	assert message.c == 3
	assert message.d == 4	
	assert message.e is None

def test_message_to_dict():
	assert messages.Message(a=1, b=2, c=3, d=4)._to_dict(False, False) == { 'a': 1, 'b': 2, 'c': 3, 'd': 4 }	
	assert messages.Message(a=dao.User(a=1, b=2, c=3), b=2, c=3, d=4)._to_dict(False, False) == { 'a': { 'a': 1, 'b': 2, 'c': 3 }, 'b': 2, 'c': 3, 'd': 4 }

def test_message_api_key_to_dict():
	assert messages.Message(a=1, b=2)._to_dict(api_key='API_KEY') == { 'a': 1, 'b': 2, 'api_key': 'API_KEY' }

def test_message_signed_to_dict():
	assert messages.Message(a=1, b=2)._to_dict(api_key='API_KEY', api_secret='API_SECRET') == { 'a': 1, 'b': 2, 'api_key': 'API_KEY', 'sig': 'TeOkjK9jnbB-4XsoWlNQRCqyQhQ=', 'ts': '20130101000000' }
	assert messages.Message(a=1, b=2)._to_dict(api_secret='API_SECRET') == { 'a': 1, 'b': 2, 'sig': 'UnEAw6frTUSki3bOrPSjB6uR0Dw=', 'ts': '20130101000000' }
	assert messages.Message(a=1, b=2, sig='SIGNATURE')._to_dict() == { 'a': 1, 'b': 2, 'sig': 'SIGNATURE' }
	message = messages.Message(a=1, b=2, sig='SIGNATURE', ts='TIMESTAMP')
	message._to_dict(api_secret='API_SECRET')
	assert message.sig == 'SIGNATURE'
	assert message.ts == 'TIMESTAMP'

def test_request_kwargs():
	message = messages.Request(gateway, a=1, b=2, c=3, d=4)
	assert message.a == 1
	assert message.b == 2
	assert message.c == 3
	assert message.d == 4	
	assert message.e is None

def test_request_form_data():
	assert messages.Request(gateway).form_data == 'api_key=API_KEY&sig=ywyvXd9Rs8doknlrTaGmqY94rLc%3D&ts=20130101000000'
	assert messages.Request(gateway, a=1, b=2, c=dao.Address(street='Street')).form_data == 'a=1&api_key=API_KEY&b=2&c.street=Street&sig=LyD-z6Fa9yF_qMeM9frKMrXRNV4%3D&ts=20130101000000'

def test_request_endpoint():
	assert messages.Request(gateway).endpoint == 'http://127.0.0.1:0/v1%s'

def test_request_method():
	assert messages.Request(gateway).method == 'GET'

def test_request_send_get():	
	def callback(request):
		assert request.get_method() == 'GET'
		assert request.get_full_url() == 'http://127.0.0.1:0/v1%s?a=1&b=2'
		return '{"a":1,"api_key":"API_KEY","sig":"F4cz8QVndl1MfC-MiBD6MXAyleM=","ts":"20130101000000"}'
	gateway.url_opener.open = urlopener(callback)
	response = messages.Request(gateway, a=1, b=2).send()
	assert response.a == 1
	assert response.api_key == 'API_KEY'
	assert response.sig == 'F4cz8QVndl1MfC-MiBD6MXAyleM='
	assert response.ts == '20130101000000'

def test_request_send_post():	
	def callback(request):
		assert request.get_method() == 'POST'
		assert request.get_full_url() == 'http://127.0.0.1:0/v1%s'
		assert request.get_data() == 'a=1&b=2'
		return '{"a":1,"api_key":"API_KEY","sig":"F4cz8QVndl1MfC-MiBD6MXAyleM=","ts":"20130101000000"}'
	gateway.url_opener.open = urlopener(callback)
	messages.Request.method = property(lambda self: 'POST')
	request = messages.Request(gateway, a=1, b=2)
	response = request.send()
	assert response.a == 1
	assert response.api_key == 'API_KEY'
	assert response.sig == 'F4cz8QVndl1MfC-MiBD6MXAyleM='
	assert response.ts == '20130101000000'

def test_request_send_error():
	def callback(request):
		raise httperror('{"error":{"type":"server-error"}}')
	gateway.url_opener.open = urlopener(callback)
	request = messages.Request(gateway, a=1, b=2)
	with pytest.raises(errors.ServerException):
		response = request.send()
		
def test_response():
	response = gateway.response('api_key=API_KEY&card.address.street=Street&next=%2Fhello&sig=_ozIgc1H_EUfEH_4FmsjzbJAVX0%3D&ts=20121011232300')
	assert response.api_key == 'API_KEY'
	assert response.card.address.street == 'Street'
	assert response.next == '/hello'


def test_response_invalid_signature():
	with pytest.raises(errors.InvalidSignatureException):
		gateway.response('api_key=API_KEY&card.address.street=Street&next=%2Fhello&sig=_ozIgc1H_EUfEH_4FmsjzbJAVX0%3D&ts=20121011232301')
	
	with pytest.raises(errors.InvalidSignatureException):
		gateway.response('api_key=API_KEY&card.address.street=Street&next=%2Fhello')

def test_response_error():
	with pytest.raises(errors.ServerException) as excinfo:	
		gateway.response('error.type=server-error&error.message=Error+Message')

	assert excinfo.value.type == 'server-error'
	assert excinfo.value.message == 'Error Message'
