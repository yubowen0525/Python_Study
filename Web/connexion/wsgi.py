from src import create_app

app = create_app()

# calling our middleware

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80)
    app.run(port=5000)
