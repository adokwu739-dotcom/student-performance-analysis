from flask import Flask

from database import init_data
from dashboard import dashboard
from students import students


def create_app():
    app = Flask(__name__)
    app.secret_key = "local-development-only-change-me"

    init_data()
    app.register_blueprint(dashboard)
    app.register_blueprint(students)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
