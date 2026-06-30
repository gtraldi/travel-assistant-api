from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from src.main.routes.trips_routes import trips_routes_bp

app = Flask(__name__)

app.register_blueprint(trips_routes_bp)

@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for any unhandled Exception."""
    if isinstance(e, HTTPException):
        response = {
            "error": e.name,
            "message": e.description
        }
        return jsonify(response), e.code

    response = {
        "error": "Internal Server Error",
        "message": str(e)
    }
    return jsonify(response), 500