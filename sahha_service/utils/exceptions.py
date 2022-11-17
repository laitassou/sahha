from rest_framework import status
from sahha_service.utils import constants
class CustomException(Exception):

    def __init__(self, message="Something went wrong.", status=status.HTTP_400_BAD_REQUEST, code=constants.ERRORS.INTERNAL_ERROR):
        super().__init__()
        self.message = message
        self.status = status
        self.code = code


    def missingFields(missings):
	    return CustomException(
	        message='Missing [' + '] or ['.join([', '.join(x) for x in missings]) + ']',
	        status=status.HTTP_400_BAD_REQUEST,
	        code=constants.ERRORS.MISSING_DATA
	    )
