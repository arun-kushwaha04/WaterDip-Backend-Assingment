from flask import Blueprint, jsonify, request
from bson import ObjectId
from bson.errors import InvalidId
from ..extension import mongo
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

@main.route('/v1/tasks', methods=['GET','POST','DELETE'])
def taskCreater():
  try:
    data = request.get_json()
    if request.method == 'POST':
      tasks = mongo.db.tasks
      if "tasks" in data:
        taskList = data["tasks"]
        for i in taskList:
          i['complete'] = i['is_completed']
          del i['is_completed']
        insertResult = tasks.insert_many(taskList)
        
        for idx,i in enumerate(insertResult.inserted_ids):
          taskList[idx]['_id'] = str(i)
        response = {
          "success": True,
          "payload":{
            'data': taskList,
            'message': 'Added new task'
          },
          "error": False
        }
        
        return jsonify(response), 201
      
      else:        
        newTaskId = tasks.insert_one({'title': data['title'], 'complete': False})
        newTaskId = str(newTaskId.inserted_id)
        response = {
          "success": True,
          "payload":{
            'data': {'_id': newTaskId,'title': data['title'], 'complete': False},
            'message': 'Added new task'
          },
          "error": False
        }
        
        return jsonify(response), 201
    
    if request.method == 'GET':
      tasks = mongo.db.tasks.find()
      tasksList = []
      for task in tasks:
        task['_id'] = str(task['_id'])
        tasksList.append(task)
      response = {
        "success": True,
        "payload":{
          'data': tasksList,
          'message': 'Added new task'
        },
        "error": False
      }
      
      return jsonify(response), 200
    
    else:
      data = request.get_json()
      taskList = []
      for i in data['tasks']:
        taskList.append(ObjectId(i['id']))
      tasks = mongo.db.tasks
      deleteResult = tasks.delete_many({'_id':{ '$in' : taskList}})
      response = {
        "success": True,
        "payload":{
          'data': data['tasks'],
          'message': 'Deleted Successfully'
        },
        "error": False
      }
      return jsonify(response), 200
      
      
  except KeyError:
    response = {
      "success": False,
      "payload":{
        'data': None,
        'message': 'Pass correct data'
      },
      "error": True
    }
    return jsonify(response), 400
  except Exception as e:
    print("Error : Adding task", str(e))
    response = {
      "success": False,
      "payload":{
        'data': None,
        'message': 'Internal Server Error'
      },
      "error": True
    }
    return jsonify(response), 500