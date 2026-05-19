from flask import Flask
from config import Config
from database import init_db
from routes.auth import auth_bp
from routes.applications import applications_bp

app = Flask(__name__)
app.config.from_object(Config)

init_db()

app.register_blueprint(auth_bp)
app.register_blueprint(applications_bp)


@app.route("/")
def home():
    return {"message": "Job Tracker API is running"}

if __name__ == "__main__":
    app.run(debug=True)