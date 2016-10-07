import datetime
import pytz

from django.db import models

from apiproxy import constants

class Event(models.Model):
	"""Cached information about an event, retrieved from the Calendar42 API"""
	id = models.CharField(primary_key=True, db_index=True, max_length=80, help_text='ID of the event (same as in Calendar42 API)')
	title = models.CharField(max_length=150, help_text='Event title')
	names = models.CharField(max_length=1500, help_text='List of participants to the event')
	cache_date = models.DateTimeField(auto_now_add=True, help_text='Datetime at which the event\'s data were last retrieved from the Calendar42 API')
	
	def is_outdated(self):
		"""Checks whether the cache is stale
		
		@return {bool}
		"""
		return (self.cache_date + constants.CACHE_DURATION) < datetime.datetime.now(pytz.utc)
	
	def get_as_serializable(self):
		return {
			'id': self.id,
			'title': self.title,
			'names': self.names.split(constants.PARTICIPANT_SEPARATOR),
		}