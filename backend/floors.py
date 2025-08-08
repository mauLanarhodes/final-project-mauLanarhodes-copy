from flask import Blueprint, request, jsonify
from config import get_db_connection

floor_bp = Blueprint('floor_bp', __name__)

# GET endpoint to retrieve all floors
# This endpoint retrieves all floors from the database and returns them as a JSON response.
# It uses a database connection to execute a SQL query that selects all records from the floor table
# and returns the results in a JSON format.
@floor_bp.route("/api/floors", methods=["GET"])
def get_floors():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM floor")
    result = cursor.fetchall()
    conn.close()
    return jsonify(result)

# POST endpoint to add a new floor
# This endpoint allows the addition of a new floor to the database.
# It expects a JSON payload containing the floor's details such as level and name.
# If the insertion is successful, it commits the transaction and returns a success message.
@floor_bp.route("/api/floors", methods=["POST"])
def add_floor():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO floor (level, name) VALUES (%s, %s)", (data['level'], data['name']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Floor added"}), 201

# PUT endpoint to update an existing floor
# This endpoint updates the details of an existing floor identified by its ID.
# It expects a JSON payload containing the updated details such as level and name.
# If the update is successful, it commits the transaction and returns a success message.
@floor_bp.route("/api/floors/<int:floor_id>", methods=["PUT"])
def update_floor(floor_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE floor SET level = %s, name = %s WHERE id = %s",
            (data['level'], data['name'], floor_id)
        )
        conn.commit()
        return jsonify({"message": "Floor updated"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

#
# DELETE endpoint to remove a floor
# This endpoint deletes a floor from the database based on its ID.
## It expects the floor ID as a URL parameter.
# If the floor is successfully deleted, it returns a success message.
@floor_bp.route("/api/floors/<int:floor_id>", methods=["DELETE"])
def delete_floor(floor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM floor WHERE id = %s", (floor_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Floor deleted"})

__all__ = ['floor_bp']

