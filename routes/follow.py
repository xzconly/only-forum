from routes import *
from flask_login import login_required

from models.follow import Follow


main = Blueprint('follow', __name__)


@main.route('/follow', methods=['POST'])
@login_required
def follow():
    import json
    form = request.form
    Follow.new(form)
    response = dict(
        status=1,
        msg='关注成功',
    )
    return json.dumps(response)


@main.route('/unfollow', methods=['POST'])
@login_required
def unfollow():
    import json
    form = request.form
    follow_id = int(form.get('follow_id', 0))
    unfollow_id = int(form.get('unfollow_id', 0))
    Follow.delete(follow_id, unfollow_id)

    response = dict(
        status=1,
        msg='关注成功',
    )
    return json.dumps(response)
