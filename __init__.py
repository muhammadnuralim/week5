from flask import Flask, render_template
from .task import task
from .user import user


def create_app():
    # create instance flask
    app = Flask(__name__)
    
    #register blueprint here
    app.register_blueprint(task.taskBp, url_prefix="/tasks")
    app.register_blueprint(user.userBp, url_prefix="/users")
    
    #route default
    @app.route('/')
    def index():
        return render_template('index.html')
    return app

