from app55 import messages

def urlopener(callback):
	class Response(object):
		def __init__(self, response):
			self.response = response

		def read(self):
			return self.response

	def open(request):
		return Response(callback(request))
	return open

def httperror(response):
	error = messages.urllib2.HTTPError(None, None, None, None, None)
	error.read = lambda: response
	return error	
