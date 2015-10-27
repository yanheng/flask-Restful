#encoding=utf-8
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask.ext.httpauth import HTTPBasicAuth
from flask import url_for
from flask.ext.restful import Resource, Api
from flask.ext.restful import reqparse, fields, marshal  #reqparse资源参数定义及验证 field资源字段类型,marshal

auth = HTTPBasicAuth()

app = Flask(__name__)
api = Api(app)

task_fields = {
    'title':fields.String,
    'description':fields.String,
    'done':fields.Boolean,
    'uri':fields.Url('task')
} #task_fields 结构用于作为 marshal 函数的模板
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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


class TaskListAPI(Resource):
    decorators = [auth.login_required] #因为 Resouce 类是继承自 Flask 的 MethodView，它能够通过定义 decorators 变量并且把装饰器赋予给它:
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
            help='No task title provided', location='json')
        self.reqparse.add_argument('description', type=str, default="",
            location='json')
        super(TaskAPI, self).__init__()

    def get(self):
        pass

    def post(self):
        pass

class TaskAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        pass

    def put(self, id):
        task = filter(lambda t: t['id']==id, tasks)
        if (len(task)) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v != None:
                task[k] = v
        return { 'task': marshal(task, task_fields) } #flask-RESTful自动转为json格式

    def delete(self, id):
        pass

api.add_resource(TaskListAPI, '/todo/api/v2.0/tasks', endpoint='tasks')
api.add_resource(TaskListAPI, '/todo/api/v2.0/tasks/<int:id>', endpoint='task')


if __name__ == '__main__':
    app.run(debug=True)
