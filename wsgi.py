from my_app.api import create_app
from my_app.api.exceptions.BusinessException import BusinessException
from my_app.api.exceptions.NotFoundException import NotFoundException

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')


@app.errorhandler(NotFoundException)
def handle_exception(e):
    return {
        'error:': 'resource not found',
        'message': e.message
    }, 400


@app.errorhandler(BusinessException)
def handle_exception(e):
    return {
        'error:': 'business_error',
        'message': e.message
    }, 500
