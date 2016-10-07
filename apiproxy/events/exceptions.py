from rest_framework.exceptions import APIException

class LoggedDetailsAPIException(APIException):
	"""Exception that tells the API proxy user that an error has occurred and that details have been logged"""
	
	default_detail = "An error has occurred. Please contact the admin or, if you're the admin, check the log for details."