# Import required modules
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from uuid import UUID
from services.login_service import get_user_by_username_password
from services.questionnaire_response_service import search_for_responses
import services.notes_service as ns

# Initialize Flask application
app = Flask(__name__)

# Initialize HTTP Basic Authentication
auth = HTTPBasicAuth()

# Define a function to verify Basic Auth credentials
@auth.verify_password
def verify_password(username, password):
    user = get_user_by_username_password(username,password)
    if user:
        return user
    return None

@app.route('/v1/valid_users', methods=['GET'])
@auth.login_required  # Use the Basic Auth annotation to protect this endpoint
def valid_user():
    return jsonify({})

@app.route('/v1/notes/templates', methods=['GET'])
@auth.login_required  # Use the Basic Auth annotation to protect this endpoint
def get_note_templates():
    note_templates = ns.get_note_templates()
    return jsonify(note_templates)

@app.route('/v1/notes/templates', methods=['POST'])
@auth.login_required  # Use the Basic Auth annotation to protect this endpoint
def create_note_template():
    result = ns.create_note_templates(request.json)
    return jsonify({"_id":result.inserted_id})

@app.route('/v1/notes', methods=['POST'])
@auth.login_required  # Use the Basic Auth annotation to protect this endpoint
def create_note():
    result = ns.create_note(request.json)
    return jsonify(result)

# Protected GET endpoint at /v1/questionnaires/{id}/responses
@app.route('/v1/questionnaires/responses', methods=['GET'])
@auth.login_required  # Use the Basic Auth annotation to protect this endpoint
def get_responses():
    search_term = request.args.get("search_term", "")
    
    responses = search_for_responses(search_term)
    
    return jsonify(responses)

# Unprotected POST endpoint at /v1/questionnaires/{id}/responses
@app.route('/v1/questionnaires/<uuid:id>/responses', methods=['POST'])
def post_responses(id):
    # Get the new response from the request body
    new_response = request.json.get("response", "")

    # Simulate saving the response
    return jsonify({
        "message": "Response created",
        "questionnaire_id": id,
        "response": new_response
    }), 201

# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)  # Change the host and port as needed
