from app.db.models.user import User
from app.services.base import BaseService


class UserService(BaseService):
    def __init__(self, model):
        super().__init__(model)


user_service = UserService(User)
