#encoding=utf-8
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask.ext.httpauth import HTTPBasicAuth
from flask import url_for

auth = HTTPBasicAuth()

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@auth.get_password
def get_password(username):#回调函数,获取给定用户的密码
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler#回调函数
def unauthorized():
    return make_response(jsonify({'error':'Unauthorized access'}), 403)


#目前 API 的设计的问题就是迫使客户端在任务标识返回后去构造 URIs。这对于服务##器是十分简单的，但是间接地迫使客户端知道这些 URIs 是如何构造的，这将会阻碍##我们以后变更这些 URIs。

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/todo/api/v1.0/tasks',  methods=(['GET']))
@auth.login_required
def get_tasks():
    return jsonify({'tasks':map(make_public_task, tasks)})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=(['GET']))
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'tasks':tasks[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
               'id':tasks[-1]['id']+1,
               'title':request.json['title'],
               'description':request.json.get('description',''),
               'done':False
           }
    tasks.append(task)
    return jsonify({'task':task}),201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = filter(lambda t: t['id']==task_id, tasks)
    if len(task) == 0:
        abort(400)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) != unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) != unicode:
        abort(400)
    task[0]['title'] = request.json.get('title',task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done',task[0]['done'])
    return jsonify({'task':task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = filter(lambda t:t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(400)
    tasks.remove(task[0])
    return jsonify({'result':True})

if __name__ == '__main__':
    app.run(debug=True)
