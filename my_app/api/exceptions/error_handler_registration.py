from my_app.api.exceptions import BusinessException, ServerException


def register_error_handlers(app):
    app.register_error_handler(BusinessException, handle_business_errors)
    app.register_error_handler(ServerException, handle_server_errors)
    app.register_error_handler(Exception, handle_unhandled_errors)


def handle_business_errors(error: BusinessException):
    return {
               'error:': 'Business error',
               'message': error.message
           }, 400


def handle_server_errors(error: ServerException):
    return {
               'error:': 'Server error',
               'message': error.message
           }, 500


def handle_unhandled_errors(error: Exception):
    return {
               'error:': 'Unhandled error',
               'message': str(error)
           }, 500
