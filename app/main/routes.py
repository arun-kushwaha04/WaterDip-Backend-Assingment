from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/v1')
def index():
  response = {
    "success": True,
    "payload":{
      'data': None,
      'message': 'Task manager version 1.0'
    },
    "error": None
  }
  return jsonify(response)