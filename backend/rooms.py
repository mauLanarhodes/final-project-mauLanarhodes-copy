from flask import Blueprint, request, jsonify
from config import get_db_connection

room_bp = Blueprint('room_bp', __name__)

# GET endpoint to retrieve all rooms
# This endpoint retrieves all rooms from the database and returns them as a JSON response.
## It uses a database connection to execute a SQL query that selects all records from the room table
# and returns the results in a JSON format.
@room_bp.route("/api/rooms", methods=["GET"])
def get_rooms():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM room")
    result = cursor.fetchall()
    conn.close()
    return jsonify(result)

# POST endpoint to add a new room
# This endpoint allows the addition of a new room to the database.
# It expects a JSON payload containing the room's details such as capacity, number, and floor.
# If the insertion is successful, it commits the transaction and returns a success message.
@room_bp.route("/api/rooms", methods=["POST"])
def add_room():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO room (capacity, number, floor) VALUES (%s, %s, %s)",
                   (data['capacity'], data['number'], data['floor']))
        conn.commit()
        return jsonify({"message": "Room added"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

# PUT endpoint to update an existing room
# This endpoint updates the details of an existing room identified by its ID.
# It expects a JSON payload containing the updated details such as capacity, number, and floor.
# If the update is successful, it commits the transaction and returns a success message.
@room_bp.route("/api/rooms/<int:room_id>", methods=["PUT"])
def update_room(room_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE room SET capacity = %s, number = %s, floor = %s WHERE id = %s",
                   (data['capacity'], data['number'], data['floor'], room_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Room updated"})


# DELETE endpoint to remove a room
# This endpoint deletes a room from the database based on its ID.
# It expects the room ID as a URL parameter.
# If the room is successfully deleted, it returns a success message.
@room_bp.route("/api/rooms/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM room WHERE id = %s", (room_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Room deleted"})
