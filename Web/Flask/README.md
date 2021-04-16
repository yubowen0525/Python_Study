- [1. Reference](#1-reference)
- [2. flask-restplus](#2-flask-restplus)
  - [2.1. Quick Start](#21-quick-start)
  - [2.2. 响应编组](#22-响应编组)
  - [2.3. 请求解析](#23-请求解析)
    - [2.3.1. 基础参数](#231-基础参数)
    - [2.3.2. 必要参数](#232-必要参数)
    - [2.3.3. 多个数值和列表](#233-多个数值和列表)
    - [2.3.4. 其他源（other destinations）](#234-其他源other-destinations)
    - [2.3.5. 参数位置](#235-参数位置)
    - [2.3.6. 高级类型处理](#236-高级类型处理)
    - [2.3.7. 文件上传](#237-文件上传)
    - [2.3.8. 错误处理](#238-错误处理)
    - [2.3.9. 错误信息](#239-错误信息)
  - [2.4. 异常处理](#24-异常处理)
    - [2.4.1. Http异常处理](#241-http异常处理)
    - [2.4.2. Flask终止助手](#242-flask终止助手)
    - [2.4.3. Flask-RESTPlus终止助手](#243-flask-restplus终止助手)
    - [2.4.4. `@api.errorhandler` 装饰器](#244-apierrorhandler-装饰器)
  - [2.5. 字段掩码](#25-字段掩码)
  - [2.6. Swagger文档](#26-swagger文档)
    - [2.6.1. Swagger中doc的记录](#261-swagger中doc的记录)
    - [2.6.2. 使用`@api.doc()`装饰器进行文档编辑](#262-使用apidoc装饰器进行文档编辑)
    - [2.6.3. 模型自动记录](#263-模型自动记录)
    - [2.6.4. wagger记录输入和输出模型](#264-wagger记录输入和输出模型)
    - [2.6.5. 头](#265-头)
    - [2.6.6. 隐藏文档](#266-隐藏文档)
    - [2.6.7. 文档安全](#267-文档安全)
  - [2.7. Postman](#27-postman)
  - [2.8. 项目扩展](#28-项目扩展)
- [3. flask-marshmallow](#3-flask-marshmallow)
  - [3.1. quick start](#31-quick-start)
  - [3.2. Flask-SQLAlchemy集成](#32-flask-sqlalchemy集成)
- [4. Marshmallow](#4-marshmallow)
  - [4.1. quick start](#41-quick-start)
  - [4.2. 定义Schema,用于序列化，反序列化](#42-定义schema用于序列化反序列化)
  - [4.3. validate](#43-validate)
  - [4.4. 对于未知字段的行为设定](#44-对于未知字段的行为设定)
  - [4.5. 序列化反序列化改变 字段名](#45-序列化反序列化改变-字段名)
    - [4.5.1. 维护字段有序](#451-维护字段有序)

# 1. Reference

Reference | 
---|
[flask-restplus中文文档](https://github.com/hanerx/flask-restplus-cn-doc) |
[flask-restplus官方文档](https://flask-restplus.readthedocs.io/en/stable/) | 
[flask-marshmallow官方文档](https://flask-marshmallow.readthedocs.io/en/latest/) | 
[marshmallow官方文档](https://marshmallow.readthedocs.io/en/stable/) | 

# 2. flask-restplus
Reference | 
---|
[flask-restplus中文文档](https://github.com/hanerx/flask-restplus-cn-doc) |
[flask-restplus官方文档](https://flask-restplus.readthedocs.io/en/stable/) | 

restful(接口) + swagger(文档)

## 2.1. Quick Start
和其他Flask扩展一样，你可以用 applicaiton 对象初始化它：
```python
from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == '__main__':
    app.run(debug=True)
```
## 2.2. 响应编组
建议使用marshmallow、flask-marshmallow的schema完成该部分

## 2.3. 请求解析
### 2.3.1. 基础参数
```python
from flask_restplus import reqparse

parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate cannot be converted')
parser.add_argument('name')
args = parser.parse_args()
```

### 2.3.2. 必要参数
required=True
```python
parser.add_argument('name', required=True, help="Name cannot be blank!")
```
### 2.3.3. 多个数值和列表
如果您希望一个键能以列表的形式接收多个值，可以像下面这样传递参数action='append'
```python
parser.add_argument('name', action='append')
```

请求：
```shell script
curl http://api.example.com -d "name=bob" -d "name=sue" -d "name=joe"
```

并且您的变量看上去会像下面这样
```python
args = parser.parse_args()
args['name']    # ['bob', 'sue', 'joe']
```

如果您希望用逗号分隔的字符串能被分割成列表，并作为一个键的值，可以像下面这样传递参数action='split'
```python
parser.add_argument('fruits', action='split')
```
这会让您的请求变得像下面这样
```shell script
curl http://api.example.com -d "fruits=apple,lemon,cherry"
```

并且您的变量看上去会像下面这样
```python
args = parser.parse_args()
args['fruits']    # ['apple', 'lemon', 'cherry']
```

### 2.3.4. 其他源（other destinations）
```python
parser.add_argument('name', dest='public_name')

args = parser.parse_args()
args['public_name']
```

### 2.3.5. 参数位置
RequestParser尝试解析来自flask.Request.values和flask.Request.json的值。

使用add_argument()的location参数来指定从哪些位置获取值。flask.Request上的任何变量都可以使用。例如

```python
# Look only in the POST body
parser.add_argument('name', type=int, location='form')

# Look only in the querystring
parser.add_argument('PageSize', type=int, location='args')

# From the request headers
parser.add_argument('User-Agent', location='headers')

# From http cookies
parser.add_argument('session_id', location='cookies')

# From file uploads
parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')
```

### 2.3.6. 高级类型处理
有时，您需要比基本数据类型更多的类型来处理输入验证。input模块提供一些常见的类型处理
- 用于更加广泛布尔处理的 boolean()
- 用于IP地址的 ipv4() 和 ipv6()
- 用于ISO8601日期和数据处理的date_from_iso8601() 和 datetime_from_iso8601()

你只需要把它们用在 type 参数上
```python
parser.add_argument('flag', type=inputs.boolean)
```

有关可用 input 的完整列表，请参阅 [input文档](https://flask-restplus.readthedocs.io/en/stable/api.html#module-flask_restplus.inputs)

您也可以像下面这样编写自己的数据类型:
```python
def my_type(value):
    '''Parse my type'''
    if not condition:
        raise ValueError('This is not my type')
    return parse(value)

# Swagger documntation
my_type.__schema__ = {'type': 'string', 'format': 'my-custom-format'}
```
### 2.3.7. 文件上传
要使用 RequestParser 处理文件上传，您需要使用 files 位置并将 type设置为FileStorage。

```python
from werkzeug.datastructures import FileStorage

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


@api.route('/upload/')
@api.expect(upload_parser)
class Upload(Resource):
    def post(self):
        uploaded_file = args['file']  # This is FileStorage instance
        url = do_something_with_file(uploaded_file)
        return {'url': url}, 201
```
请参阅专用的[Flask文档](https://flask.palletsprojects.com/en/master/patterns/fileuploads/)部分。
### 2.3.8. 错误处理
配置绑定错误，RequestParser所有出错的字段都会返回给客户端。
1. 方式一 `parser = reqparse.RequestParser(bundle_errors=True)`
2. 方式二 `app.config['BUNDLE_ERRORS'] = True`

### 2.3.9. 错误信息
help 参数可能包含一个插值标记（ interpolation token），就像 {error_msg} 这样，这个标记将会被错误类型的字符串表示替换。这允许您在保留原本的错误消息的同时定制消息，就像下面的例子这样
```python
from flask_restplus import reqparse


parser = reqparse.RequestParser()
parser.add_argument(
    'foo',
    choices=('one', 'two'),
    help='Bad choice: {error_msg}'
)

# If a request comes in with a value of "three" for `foo`:

{
    "message":  {
        "foo": "Bad choice: three is not a valid choice",
    }
}
```

##  2.4. 异常处理
### 2.4.1. Http异常处理
Werkzeug HTTP异常（Werkzeug HTTPException）将适当的自动重写描述（description）属性。
```python
from werkzeug.exceptions import BadRequest
raise BadRequest()
```
上述代码将会返回一个400状态码和输出：
```python
{
    "message": "The browser (or proxy) sent a request that this server could not understand."
}
```
你可以通过修改data属性值添加额外的参数到你的异常中：
```python
from werkzeug.exceptions import BadRequest
e = BadRequest('My custom message')
e.data = {'custom': 'value'}
raise e
```

```python
{
    "message": "My custom message",
    "custom": "value"
}
```
### 2.4.2. Flask终止助手
终止助手（abort helper） 适当的将错误封装成了一个 Http异常（ HTTPException ） ，因此它们表现几乎相同。
```python
from flask import abort
abort(400, 'My custom message')
```

```python
{
    "message": "My custom message"
}
```

###  2.4.3. Flask-RESTPlus终止助手
**errors.abort()** 与 **Namespace.abort()** 终止助手与原生**Flask Flask.abort()** 原理相似，但将会把关键字参数（keyword arguments）打包进响应中。

```python
from flask_restplus import abort
abort(400, 'My custom message', custom='value')
```
上述代码将会返回一个400状态码和输出：
```python
{
    "message": "My custom message",
    "custom": "value"
}
```
###  2.4.4. `@api.errorhandler` 装饰器
`@api.errorhandler`装饰器将为指定的异常（或继承于这个异常的任何异常）注册一个特别的处理机（handler），你也可以用同样的方法使用 `Flask/Blueprint 的 @errorhandler`装饰器。
```python
@api.errorhandler(RootException)
def handle_root_exception(error):
    '''Return a custom message and 400 status code'''
    return {'message': 'What you want'}, 400


@api.errorhandler(CustomException)
def handle_custom_exception(error):
    '''Return a custom message and 400 status code'''
    return {'message': 'What you want'}, 400


@api.errorhandler(AnotherException)
def handle_another_exception(error):
    '''Return a custom message and 500 status code'''
    return {'message': error.specific}


@api.errorhandler(FakeException)
def handle_fake_exception_with_header(error):
    '''Return a custom message and 400 status code'''
    return {'message': error.message}, 400, {'My-Header': 'Value'}


@api.errorhandler(NoResultFound)
def handle_no_result_exception(error):
    '''Return a custom not found error message and 404 status code'''
    return {'message': error.specific}, 404
```
## 2.5. 字段掩码

##  2.6. Swagger文档
### 2.6.1. Swagger中doc的记录
字段 | 内容
---| ---
description |  api的描述|
params | 请求参数|
response | 返回的状态码与返回值|
header| response的header|
deprecated | True/Flase 是否弃用|
id | operationId(缺省就是get_resource) |

### 2.6.2. 使用`@api.doc()`装饰器进行文档编辑
@api.doc() 修饰器使你可以为文档添加额外信息。

```python
@api.route('/my-resource/<id>', endpoint='my-resource')
@api.doc(params={'id': 'An ID'})
class MyResource(Resource):
    def get(self, id):
        return {}

    @api.doc(responses={403: 'Not Authorized'})
    def post(self, id):
        api.abort(403)
```
### 2.6.3. 模型自动记录
所有由 `model()` 、 `clone()` 和 `inherit()` 实例化的模型（model）都会被自动记录到Swagger文档中。
```python
parent = api.model('Parent', {
    'name': fields.String,
    'class': fields.String(discriminator=True)
})

child = api.inherit('Child', parent, {
    'extra': fields.String
})
```
上面的代码会生成下面的Swagger定义：
```python
{
    "Parent": {
        "properties": {
            "name": {"type": "string"},
            "class": {"type": "string"}
        },
        "discriminator": "class",
        "required": ["class"]
    },
    "Child": {
        "allOf": [
            {
                "$ref": "#/definitions/Parent"
            }, {
                "properties": {
                    "extra": {"type": "string"}
                }
            }
        ]
    }
}
```

### 2.6.4. wagger记录输入和输出模型
你可以通过 api.doc() 修饰器的 model 关键字指定序列化输出模型。

对于 PUT 和 POST 方法，使用 body 关键字指定输入模型。

1. 对于输入模型，可以使用@api.expect(parse)
2. 对于输出模型，@api.marsh_with(model) 或者 @api.doc(model='MyModel', body=Person)

###  2.6.5. 头
```python
@api.route('/with-headers/')
@api.header('X-Header', 'Some class header')
class WithHeaderResource(restplus.Resource):
    @api.header('X-Collection', type=[str], collectionType='csv')
    @api.response(200, 'Success', headers={'X-Header': 'Some header'})    
def get(self):
        pass
```
### 2.6.6. 隐藏文档
`@api.route('/resource1/', doc=False)`

`@api.hide`

### 2.6.7. 文档安全
authorizations 是以Python字典的形式表现Swagger securityDefinitions 的配置信息。
```python
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}
api = Api(app, authorizations=authorizations)
```

[个性化OAuth安全配置](https://github.com/hanerx/flask-restplus-cn-doc#%E4%B8%AA%E6%80%A7%E5%8C%96)

## 2.7. Postman

##  2.8. 项目扩展

#  3. flask-marshmallow
[flask-marshmallow官方文档](https://flask-marshmallow.readthedocs.io/en/latest/) 

dumps : object -> json 

loads : json -> object 

##  3.1. quick start
Create your app.
```python
from flask import Flask
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)
```

Write your models.
```python
from ..extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
```

Define your output format with marshmallow.
```python
from src.extensions import ma
from src.models.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = User
        fields = ("email", "date_created", "_links")
        # id = ma.auto_field()
        # email = ma.auto_field()
        # date_created = ma.auto_field()

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            # ma.URLFor(endpoint, url_key, external)
            "self": ma.URLFor("ns1_users_api", id="<id>"),
            "collection": ma.URLFor("ns1_users_all_api"),
        }
    )
```

Use: SQLAlchemy Object -> Json_Str
```python
from src.models.user import User
from src.schme.ns1_test1 import UserSchema

user_schema = UserSchema()
user = User.query.limit(1).all()
user_schema.dump(user)
```

##  3.2. Flask-SQLAlchemy集成
1. 需要保证以下依赖

    ```
    flask-marshmallow==0.14.0
    marshmallow==3.10.0
    marshmallow-sqlalchemy==0.24.2
    ```
2. 顺序初始化
    ```
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_marshmallow import Marshmallow
    
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
    
    # Order matters: Initialize SQLAlchemy before Marshmallow
    db = SQLAlchemy(app)
    ma = Marshmallow(app)
    ```
3. model init
    ```
    class Author(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255))
    
    
    class Book(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(255))
        author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
        author = db.relationship("Author", backref="books")
    ```
4. schema init
    SQLAlchemySchema:
    - 缺省SQLAlchemySchema使用Flask-SQLAlchemy的全部字段
    - SQLAlchemySchema是schema的子类
    ```
    class AuthorSchema(ma.SQLAlchemySchema):
        class Meta:
            model = Author
    
        id = ma.auto_field()
        name = ma.auto_field()
        books = ma.auto_field()
    
    
    class BookSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Book
            include_fk = True
    ```
5. use
    ```
    db.create_all()
    author_schema = AuthorSchema()
    book_schema = BookSchema()
    author = Author(name="Chuck Paluhniuk")
    book = Book(title="Fight Club", author=author)
    db.session.add(author)
    db.session.add(book)
    db.session.commit()
    author_schema.dump(author)
    # {'id': 1, 'name': 'Chuck Paluhniuk', 'books': [1]}
    ```


# 4. Marshmallow
[marshmallow官方文档](https://marshmallow.readthedocs.io/en/stable/) 

dumps : object -> json
loads : json -> object

## 4.1. quick start
```python
from datetime import date
from pprint import pprint

from marshmallow import Schema, fields


class ArtistSchema(Schema):
    name = fields.Str()


class AlbumSchema(Schema):
    title = fields.Str()
    release_date = fields.Date()
    artist = fields.Nested(ArtistSchema())


bowie = dict(name="David Bowie")
album = dict(artist=bowie, title="Hunky Dory", release_date=date(1971, 12, 17))

schema = AlbumSchema()
result = schema.dump(album)
pprint(result, indent=2)
# { 'artist': {'name': 'David Bowie'},
#   'release_date': '1971-12-17',
#   'title': 'Hunky Dory'}
```

总结下来，marshmallow schema 有三个用处：
- 校验输入数据
- 将输入数据反序列化到自定义对象 load
- 序列化自定义对象至原始的python类型 dump

重要的点：
1. `fields.Nested()` 解决嵌套object的问题
2. `Schema.from_dict(
    {"name": fields.Str(), "email": fields.Email(), "created_at": fields.DateTime()}
)` 可以使用dict方式创建schema
   
3. `schema = UserSchema(only=("name", "email"))   schema.dump(user)`  只会序列化only的field
4. `@post_load` 在schema.load() 时直接序列化为 自定义object  [demo](./src/schme/marshmallow/test2.py)
5. `many=True`参数解决可迭代对象
6. `field.Str(validate=...)` 加入校验器
7. `requied = True` 为必须存在该字段
8. `default = 1` 设置缺省值
9. `dump_only=True` 意味只读在dump时该字段才会使用。 `load_only=True` 意味只写在load时该字段才会使用

## 4.2. 定义Schema,用于序列化，反序列化
```python
class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

class AlbumSchema(Schema):
    title = fields.Str()
    release_date = fields.Date()
    artist = fields.Nested(ArtistSchema())
```

## 4.3. validate
```python
from pprint import pprint

from marshmallow import Schema, fields, validate, ValidationError


class UserSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1))
    permission = fields.Str(validate=validate.OneOf(["read", "write", "admin"]))
    age = fields.Int(validate=validate.Range(min=18, max=40))


in_data = {"name": "", "permission": "invalid", "age": 71}
try:
    UserSchema().load(in_data)
except ValidationError as err:
    pprint(err.messages)
```

也可自己实现校验器
```python
from marshmallow import Schema, fields, ValidationError


def validate_quantity(n):
    if n < 0:
        raise ValidationError("Quantity must be greater than 0.")
    if n > 30:
        raise ValidationError("Quantity must not be greater than 30.")


class ItemSchema(Schema):
    quantity = fields.Integer(validate=validate_quantity)


in_data = {"quantity": 31}
try:
    result = ItemSchema().load(in_data)
except ValidationError as err:
    print(err.messages)  # => {'quantity': ['Quantity must not be greater than 30.']}
```
装饰器注册实现
```python
class ItemSchema(Schema):
    quantity = fields.Integer()

    @validates("quantity")
    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError("Quantity must be greater than 0.")
        if value > 30:
            raise ValidationError("Quantity must not be greater than 30.")
```

## 4.4. 对于未知字段的行为设定
- RAISE (default): 若存在未知字段就会出现ValidationError

- EXCLUDE: 排除 未知的字段

- INCLUDE: 接收包括进 未知的字段

设置方式1：
```
from marshmallow import Schema, INCLUDE


class UserSchema(Schema):
    class Meta:
        unknown = INCLUDE
```
设置方式2：

`schema = UserSchema(unknown=INCLUDE)`  或者 `UserSchema().load(data, unknown=INCLUDE)`

##  4.5. 序列化反序列化改变 字段名
读时json -> object ，将 email -> emailAddress 。 写时object -> json  将  emailAddress -> email
```python
class UserSchema(Schema):
    name = fields.String()
    email = fields.Email(data_key="emailAddress")


s = UserSchema()

data = {"name": "Mike", "email": "foo@bar.com"}
result = s.dump(data)
# {'name': u'Mike',
# 'emailAddress': 'foo@bar.com'}

data = {"name": "Mike", "emailAddress": "foo@bar.com"}
result = s.load(data)
# {'name': u'Mike',
# 'email': 'foo@bar.com'}
```

###  4.5.1. 维护字段有序
meta下 ordered = True
```python
from collections import OrderedDict
from pprint import pprint

from marshmallow import Schema, fields


class UserSchema(Schema):
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()

    class Meta:
        ordered = True


u = User("Charlie", "Stones", "charlie@stones.com")
schema = UserSchema()
result = schema.dump(u)
assert isinstance(result, OrderedDict)
pprint(result, indent=2)
#  OrderedDict([('first_name', 'Charlie'),
#              ('last_name', 'Stones'),
#              ('email', 'charlie@stones.com')])
```