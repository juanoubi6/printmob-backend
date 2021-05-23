from my_app.api.controllers import TestController
from my_app.api.repositories import TestRepository
from my_app.api.services import TestService


def inject_controllers(app, db):
    app.test_controller = build_test_controller(db)


def build_test_controller(db):
    test_repository = TestRepository(db)
    test_service = TestService(test_repository)

    return TestController(test_service)
