
from flask import Flask, jsonify
from routes.health import health_bp

app = Flask(__name__)

# Register health API routes
app.register_blueprint(health_bp)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project": "IntelliTriage",
        "message": "Backend is running"
    })

if __name__ == "__main__":
    app.run(debug=True)
