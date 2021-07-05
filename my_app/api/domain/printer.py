from my_app.api.domain.user import User, UserType, UserPrototype


class Printer(User):
    def __init__(self, user: User):
        super().__init__(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            user_name=user.user_name,
            date_of_birth=user.date_of_birth,
            email=user.email,
            user_type=UserType.PRINTER,
            created_at=user.created_at,
            updated_at=user.updated_at,
            deleted_at=user.deleted_at
        )

    def to_json(self):
        return User.to_json(self)


class PrinterPrototype:
    def __init__(self, user_prototype: UserPrototype):
        self.user_prototype = user_prototype
