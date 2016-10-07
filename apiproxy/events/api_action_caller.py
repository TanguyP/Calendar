import logging
import requests

from apiproxy import constants
from .exceptions import LoggedDetailsAPIException

logger = logging.getLogger(__name__)

class APIActionCaller():
	
	def __init__(self, token):
		self._token = token
	
	def call(self, *args, **kwargs):
		"""Calls the Calendar42 API and returns the response
		
		@return	{dict}	The JSON API response
		"""
		
		# Call the Calendar42 API
		full_url = constants.CALENDAR42_API_BASE_URL + self.get_relative_url(*args, **kwargs)
		
		headers = {
			'Accept': 'application/json',
			'Content-type': 'application/json',
			'Authorization': 'Token %s' % self._token,
		}
		response = requests.get(full_url, headers=headers)
		
		# Parse response as JSON
		try:
			json_data = response.json()
		except ValueError as e:
			logger.exception(e)
			logger.error("URL called: %s\nHere's the body of the response which couldn't get parsed to JSON: %s" % (full_url, response.text))
			raise LoggedDetailsAPIException()
		
		# Extract desired information
		try:
			if 'error' in json_data:
				# Forward error from Calendar42 API to client
				raise LoggedDetailsAPIException(json_data['error']['message'])
				
			return self.extract_data(json_data)
		except (KeyError, ValueError, AttributeError) as e:
			logger.exception(e)
			logger.error("URL called: %s\nHere's the JSON data which didn't fit the expected format: %s" % (full_url, json_data))
			raise LoggedDetailsAPIException()
	
	def extract_data(self, json_data):
		"""ABSTRACT METHOD - TO BE IMPLEMENTED IN CHILD CLASS
		
		Extracts the desired information from the JSON data returned by the Calendar42 API
		@param {dict} json_data
		@return {dict}	The extracted data
		"""
		logger.exception(NotImplementedError())
		raise LoggedDetailsAPIException()
	
	def get_relative_url(self, *args, **kwargs):
		"""ABSTRACT METHOD - TO BE IMPLEMENTED IN CHILD CLASS
		
		Returns the end of the URL, corresponding to the API action to call
		"""
		logger.exception(NotImplementedError())
		raise LoggedDetailsAPIException()


class EventDetailsAPIActionCaller(APIActionCaller):
	"""Gets details (ID and title) of an event"""

	def get_relative_url(self, event_id):
		return constants.CALENDAR42_API_EVENT.format(event_id)

	def extract_data(self, json_data):
		raw_details = json_data['data'][0]
		details = {
			'id': raw_details['id'],
			'title': raw_details['title'],
		}
		return details

		
class EventParticipantsAPIActionCaller(APIActionCaller):
	"""Gets list of participants to an event"""

	def get_relative_url(self, event_id):
		return constants.CALENDAR42_API_PARTICIPANTS.format(event_id)

	def extract_data(self, json_data):
		return [item['subscriber']['first_name'] for item in json_data['data']]
