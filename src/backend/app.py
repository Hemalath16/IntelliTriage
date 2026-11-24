
from flask import Flask, jsonify

from routes.health import health_bp
from routes.patients import patients_bp
from routes.nurse import nurse_bp

app = Flask(__name__)

# Register API routes
app.register_blueprint(health_bp)
app.register_blueprint(patients_bp)
app.register_blueprint(nurse_bp)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project": "IntelliTriage",
        "message": "Backend is running"
    })

if __name__ == "__main__":
    app.run(debug=True)
