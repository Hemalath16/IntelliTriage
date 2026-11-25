from flask import Flask, jsonify

from routes.health import health_bp
from routes.patients import patients_bp
from routes.nurse import nurse_bp
from routes.clinical_records import clinical_records_bp
from routes.staff import staff_bp
from routes.auth import auth_bp

app = Flask(__name__)

# Register API routes
app.register_blueprint(health_bp)
app.register_blueprint(patients_bp)
app.register_blueprint(nurse_bp)
app.register_blueprint(clinical_records_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(auth_bp)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project": "IntelliTriage",
        "message": "Backend is running"
    })


if __name__ == "__main__":
    app.run(debug=True)