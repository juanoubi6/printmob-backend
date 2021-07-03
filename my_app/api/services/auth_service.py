from my_app.api.repositories import GoogleRepository


class AuthService:
    def __init__(self, google_repository: GoogleRepository):
        self.google_repository = google_repository

    def get_user_login_data(self, auth_token: str) -> dict:
        google_user_data = self.google_repository.retrieve_token_data(auth_token)


        return {"user_data": "some_user_data"}
