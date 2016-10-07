import logging
import os

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from . import constants

class StartupManager():

	@classmethod
	def startup(cls):
		# Create sample user
		sample_user, _ = User.objects.get_or_create(username=constants.SAMPLE_USER)
		token, _ = Token.objects.get_or_create(user=sample_user)
		file_name = constants.SAMPLE_USER_FILE_NAME
		
		with open(file_name, 'w') as f:
			f.write(token.key)
		
		print('Token key "%s" for a sample user has been written to %s - please use it' % (token.key, file_name))
		
		# Configure log file
		log_file_name = os.path.join(settings.BASE_DIR, 'server.log')
		logging.basicConfig(filename=log_file_name)