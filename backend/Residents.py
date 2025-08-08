from flask import Blueprint, request, jsonify
from config import get_db_connection


resident_bp = Blueprint('resident_bp', __name__)



# GET endpoint to retrieve all residents
# This endpoint retrieves all residents from the database and returns them as a JSON response.
# It uses a database connection to execute a SQL query that selects all records from the resident table
## and returns the results in a JSON format.
# The connection is closed after the query execution to free up resources.
@resident_bp.route("/residents", methods=["GET"]) 
def get_residents():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM resident")
    result = cursor.fetchall()
    conn.close()
    return jsonify(result)

# POST endpoint to add a new resident
# This endpoint allows the addition of a new resident to the database.
# It expects a JSON payload containing the resident's details such as firstname, lastname, age, and room.
# The endpoint validates the existence of the specified room before inserting the new resident.
# If the room does not exist, it returns an error response.
# If the insertion is successful, it commits the transaction and returns a success message.
# If an error occurs during the insertion, it rolls back the transaction and returns an error message
@resident_bp.route("/api/residents", methods=["POST"])
def add_resident():
    data = request.json
    print("DEBUG incoming data:", data)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Validate room exists
    cursor.execute("SELECT id FROM room WHERE id = %s", (data['room'],))
    room_exists = cursor.fetchone()
    print("DEBUG room exists:", room_exists)

    if not room_exists:
        return jsonify({"error": "Room ID does not exist"}), 400

    try:
        cursor.execute(
            "INSERT INTO resident (firstname, lastname, age, room) VALUES (%s, %s, %s, %s)",
            (data['firstname'], data['lastname'], data['age'], data['room'])
        )
        conn.commit()
        return jsonify({"message": "Resident added"}), 201

    except Exception as e:
        print("ERROR inserting resident:", e)
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# PUT endpoint to update an existing resident
# This endpoint updates the details of an existing resident identified by their ID.
# It expects a JSON payload containing the updated details such as firstname, lastname, age, and room.
# The endpoint first checks if the resident exists in the database.
# If the resident does not exist, it returns a 404 error.
# It also checks if the specified room exists before performing the update.
@resident_bp.route("/api/residents/<int:resident_id>", methods=["PUT"])
def update_resident(resident_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if resident exists
        cursor.execute("SELECT id FROM resident WHERE id = %s", (resident_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Resident ID not found"}), 404

        # Check if room exists
        cursor.execute("SELECT id FROM room WHERE id = %s", (data['room'],))
        if not cursor.fetchone():
            return jsonify({"error": "Room ID not found"}), 400

        # Perform update
        cursor.execute(
            "UPDATE resident SET firstname = %s, lastname = %s, age = %s, room = %s WHERE id = %s",
            (data['firstname'], data['lastname'], data['age'], data['room'], resident_id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Update failed or no changes made"}), 400

        return jsonify({"message": "Resident updated"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# DELETE endpoint to remove a resident
# This endpoint deletes a resident from the database based on their ID.
# It expects the resident ID as a URL parameter.
# If the resident is successfully deleted, it returns a success message.
@resident_bp.route("/api/residents/<int:resident_id>", methods=["DELETE"])
def delete_resident(resident_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM resident WHERE id = %s", (resident_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Resident deleted"})
