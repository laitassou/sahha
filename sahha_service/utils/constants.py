class GENERAL:
    PAGE_SIZE = 5
    DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
    DATE_FORMAT = "%d/%m/%Y"
    FROM_EMAIL = 'Do not Reply <do_not_reply@gmail.com>'


class STATUS:
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    ERROR = "ERROR"


class ROLE:
    ADMIN = "ADMIN"
    ORGANIZER = "ORGANIZER"
    OPTIONS = (ADMIN, ORGANIZER, )
