from flask import request, Blueprint
from flaskapp.auth import token_required
from flaskapp.services import ks_service

ks = Blueprint('ks', __name__)


@ks.route('/add-ks', methods=['POST'])
@token_required
def add_ks(current_user):
    data = request.get_json()

    return ks_service.add_ks(data)