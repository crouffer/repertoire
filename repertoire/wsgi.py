from repertoire.application import create_app, start_dev_server

DEBUG = True

app = create_app()

if __name__ == '__main__' and __package__ is None:
    if DEBUG:
        start_dev_server(app)
    else:
        app.run()
