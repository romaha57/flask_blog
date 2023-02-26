from flask_login import LoginManager
from flask_login import UserMixin

from .models import User


class UserLogin(UserMixin):
    def get_user(self, user_id):
        self.user = User.query.get(user_id)
        return self

    def create(self, user):
        self.user = user
        return self

    def get_user_from_db(self):
        if self.user:
            return User.query.get(self.user.id)

    def get_id(self):
        try:
            return str(self.user.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().get_user(user_id)