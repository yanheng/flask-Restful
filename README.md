# flask-Restful
flask实现Restful接口
在控制台测试
GET 获取资源
$curl -i http://localhost:5000/todo/api/v1.0/tasks
GET 获取某个特定的资源信息
$curl -i http://localhost:5000/todo/api/v1.0/tasks/id
POST 创建资源
$curl -i -H "Content-type:application/json" -X POST -d '{"title":"hello world","description":""}'  http://localhost:5000//todo/api/v1.0/tasks
PUT 跟新资源
$curl -i -H "Content-type:application/json" -X PUT -d '{"title":"hello world","description":""}'   http://localhost:5000//todo/api/v1.0/tasks/id
DELETE 删除资源
$curl -i -H "Content-type:application/json" -X DELETE   http://localhost:5000//todo/api/v1.0/tasks/id
