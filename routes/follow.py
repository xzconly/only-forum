from routes import *
from flask_login import login_required

from models.follow import Follow


main = Blueprint('follow', __name__)


@main.route('/follow', methods=['POST'])
@login_required
def follow():
    import json
    follow_ids = request.get_json()
    result = Follow.handle_follow(follow_ids)
    if result == 1:
        response = dict(
            status=1,
            msg='关注成功',
        )
    elif result == 2:
        response = dict(
            status=2,
            msg='取消关注成功',
        )
    elif result == 0:
        response = dict(
            status=0,
            msg='操作失败',
        )
    return json.dumps(response)
