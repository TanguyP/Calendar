"""Utility class for reading tokens from the Calendar42 API token file"""

import ConfigParser
import os

from django.conf import settings

from apiproxy import constants

class ApiTokenReader():

	@classmethod
	def getUserToken(cls, username):
		"""Returns the token for a given username"""
		token_file_path = os.path.join(settings.BASE_DIR, 'events', constants.TOKEN_FILE_NAME)
		parser = ConfigParser.ConfigParser()
		parser.read(token_file_path)
		
		try:
			token = parser.get(constants.TOKEN_SECTION_NAME, constants.SAMPLE_USER)
		except ConfigParser.NoSectionError as e:
			raise ConfigParser.NoSectionError("Missing %s section in %s configuration file" % (constants.TOKEN_SECTION_NAME, constants.TOKEN_FILE_NAME))
		except ConfigParser.NoOptionError as e:
			raise ConfigParser.NoOptionError("Missing token for user %s in %s configuration file" % (constants.SAMPLE_USER, constants.TOKEN_FILE_NAME))
		
		return token