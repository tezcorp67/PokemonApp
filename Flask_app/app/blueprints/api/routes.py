# from . import api
from flask import request, jsonify, Blueprint
from app.models import Post


api = Blueprint('api',__name__, url_prefix='/api')




@api.post('create_post')
def create_post_api():
    data = request.get_json


    new_post = Post(img_url= data['img_url'], caption= data['caption'])