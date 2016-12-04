from routes import *


main = Blueprint('index', __name__)


@main.route('/')
@login_required
def index():
    return render_template('index.html')
