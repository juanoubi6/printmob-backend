from my_app.api.exceptions.not_found_exception import NotFoundException
from my_app.api.exceptions.base import BusinessException, ServerException
from my_app.api.exceptions.unprocessable_entity_exception import UnprocessableEntityException


def register_error_handlers(app):
    app.register_error_handler(NotFoundException, handle_not_found_errors)
    app.register_error_handler(UnprocessableEntityException, handle_unprocessable_entity_errors)
    app.register_error_handler(BusinessException, handle_business_errors)
    app.register_error_handler(ServerException, handle_server_errors)
    app.register_error_handler(Exception, handle_unhandled_errors)


def handle_not_found_errors(error: NotFoundException):
    return {
               'error:': 'An element was not found',
               'message': error.message
           }, 404


def handle_unprocessable_entity_errors(error: UnprocessableEntityException):
    return {
               'error:': 'Unprocessable entity error',
               'message': error.message
           }, 422


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
