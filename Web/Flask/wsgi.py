from src import create_app
from src.middleware.middleware import middleware

app = create_app()

# calling our middleware
app.wsgi_app = middleware(app.wsgi_app)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80)
    app.run(port=5000)
