from distutils.core import setup, Command

class PyTest(Command):
	user_options = []
	def initialize_options(self):
		pass
	def finalize_options(self):
		pass
	def run(self):
		import os, sys, subprocess
		errno = subprocess.call([sys.executable, 'runtests.py'])
		raise SystemExit(errno)

setup(
	name = 'app55',
	version = '0.8.3',
	description = 'App55 API Client for Python',
	author = 'App55',
	author_email = 'support@app55.com',
	url = 'https://docs.app55.com/api/python',
	license = 'MIT',
	packages = ['app55'],
	cmdclass = { 'test': PyTest },
	package_data = { 'app55': [ 'thawte.pem' ] }
)
