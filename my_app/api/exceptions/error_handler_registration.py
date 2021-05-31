from my_app.api.exceptions import BusinessException, ServerException


def register_error_handlers(app):
    app.register_error_handler(BusinessException, handle_business_errors)
    app.register_error_handler(ServerException, handle_server_errors)


def handle_business_errors(error: BusinessException):
    return {
               'error:': 'Business error',
               'message': error.message
           }, 400


def handle_server_errors(error: ServerException):
    return {
               'error:': 'Unexpected error',
               'message': error.message
           }, 500
