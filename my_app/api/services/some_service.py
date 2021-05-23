class TestService:
    def __init__(self, test_repository):
        self.test_repository = test_repository

    def get_test_data_from_service(self):
        return self.test_repository.get_test_data_from_db()
