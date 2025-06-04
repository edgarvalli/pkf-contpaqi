from flask import Flask

app = Flask(__name__, static_folder="public", static_url_path="/public")

app.secret_key = "p4ssw0rd"

app.register_blueprint(
    __import__("blueprints", fromlist=["approute"]).approute
)
app.register_blueprint(
    __import__("blueprints.login", fromlist=["login_blueprint"]).login_blueprint
)

app.register_blueprint(
    __import__("blueprints.api", fromlist=["api"]).api
)


@app.route("/")
def hello_world():
    return "Application is running!"