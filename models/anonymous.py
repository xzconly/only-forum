from flask_login import AnonymousUserMixin


class Anonymous(AnonymousUserMixin):
    __tablename__ = 'anonymous'

    def __init__(self):
        self.id = 0
        self.username = 'Guest'

    def get_follow_status(self, user_id):
        status = 0
        return status
