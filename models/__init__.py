from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()


def utc():
    utc = int(time.time())
    return utc


class ModelMixin(object):
    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m

    @classmethod
    def update(cls, model_id, form):
        m = cls.query.get(model_id)
        m._update(form)

    @classmethod
    def delete(cls, model_id):
        m = cls.query.get(model_id)
        m.remove()

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n {1}\n>'.format(class_name, '\n '.join(properties))

    def save(self):
        db.session.add(self)
        db.commit()

    def remove(self):
        # 逻辑删除
        self.deleted = True
        self.save()
