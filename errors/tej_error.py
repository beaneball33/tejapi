class TejError(RuntimeError):
    GENERIC_ERROR_MESSAGE = '發生錯誤，請再測試一次，若持續發生問題，請聯絡 api@tej.com.tw'

    def __init__(self, tej_message=None, http_status=None, http_body=None, http_headers=None,
                 tej_error_code=None, response_data=None):
        self.http_status = http_status
        self.http_body = http_body
        self.http_headers = http_headers if http_headers is not None else {}

        self.tej_error_code = tej_error_code
        self.tej_message = tej_message if tej_message is not None \
            else self.GENERIC_ERROR_MESSAGE
        self.response_data = response_data

    def __str__(self):
        if self.http_status is None:
            status_string = ''
        else:
            status_string = "(Status %(http_status)s) " % {"http_status": self.http_status}
        if self.tej_error_code is None:
            tej_error_string = ''
        else:
            tej_error_string = "(Tej Error %(tej_error_code)s) " % {
                "tej_error_code": self.tej_error_code}
        return "%(ss)s%(tes)s%(tm)s" % {
            "ss": status_string, "tes": tej_error_string, "tm": self.tej_message
        }


class AuthenticationError(TejError):
    pass


class InvalidRequestError(TejError):
    pass


class LimitExceededError(TejError):
    pass


class NotFoundError(TejError):
    pass


class ServiceUnavailableError(TejError):
    pass


class InternalServerError(TejError):
    pass


class ForbiddenError(TejError):
    pass


class InvalidDataError(TejError):
    pass


class ColumnNotFound(TejError):
    pass
