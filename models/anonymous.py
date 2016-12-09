from flask_login import AnonymousUserMixin


class Anonymous(AnonymousUserMixin):
    __tablename__ = 'anonymous'

    def __init__(self):
        self.id = ''
        self.username = 'Guest'
