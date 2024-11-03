"""
TP RATTRAPAGE ANDREAS FIVEL
"""

from flask import Flask, request, jsonify
from flask_cors import CORS 
from flask_expects_json import expects_json
import service

app = Flask(__name__)
CORS(app)

booking_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "string"},
        "start_date": {"type": "string"},
        "end_date": {"type": "string"},
        "is_cancelled": {"type": "boolean"},
        "is_paid": {"type": "boolean"},
        "price": {"type": "number", "minimum": 0},
        "room_type": {"type": "string", "enum": ["SINGLE", "DELUXE", "SUITE"]}
    },
    "required": ["user_id", "start_date", "end_date", "is_cancelled", "is_paid", "price", "room_type"],
    "additionalProperties": False
}

@app.route("/bookings", methods=["GET"])
def get_bookings():
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))
    return jsonify(service.get_all_bookings(offset, limit)), 200

@app.route("/booking/<string:booking_id>", methods=["GET"])
def get_booking(booking_id):
    booking = service.get_booking(booking_id)
    if booking:
        return jsonify(booking), 200
    return jsonify({"error": "Booking not found"}), 404

@app.route("/booking", methods=["POST"])
@expects_json(booking_schema)
def create_booking():
    data = request.json
    booking = service.create_booking(data)
    return jsonify(booking), 201

@app.route("/booking/<string:booking_id>", methods=["PUT"])
@expects_json(booking_schema)
def update_booking(booking_id):
    data = request.json
    updated_booking = service.update_booking(booking_id, data)
    if updated_booking:
        return jsonify(updated_booking), 200
    return jsonify({"error": "Booking not found"}), 404

@app.route("/booking/<string:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    if service.delete_booking(booking_id):
        return '', 204
    return jsonify({"error": "Booking not found"}), 404

@app.route("/statistics/room_type", methods=["GET"])
def room_type_statistics():
    return jsonify(service.get_room_type_statistics()), 200

if __name__ == "__main__":
    app.run(debug=True)
