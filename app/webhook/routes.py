from flask import Blueprint, jsonify, request, render_template
from datetime import datetime
from app.extensions import get_db
import json

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    if(request.headers['Content-Type']=='application/json'):
        info = request.json
        
        if('pull_request' not in info): # It implies a 'PUSH' action
            commit_hash = info['after']
            user = info['pusher']['name']
            branch = info['ref'].split('/')[-1]
            pushed_at = info['commits'][0]['timestamp']
            # Parse ISO 8601 datetime string
            dt = datetime.fromisoformat(pushed_at.replace('Z', '+00:00'))

            # Format datetime object in the desired format
            formatted_datetime = dt.strftime("%d %B %Y - %I:%M %p UTC")

            db = get_db()
            data = {"request_id": commit_hash, "author":user, "action":"PUSH", "branch":branch, "timestamp":formatted_datetime}  # Assuming JSON data is sent in the POST request

        else:
            if(info['pull_request']['merged'] == True): # It implies a 'MERGE' action
                pull_request_id = info['pull_request']['id']
                user = info['pull_request']['user']['login']
                base_branch = info['pull_request']['base']['ref']
                head_branch = info['pull_request']['head']['ref']
                merged_at = info['pull_request']['merged_at']
                # Parse ISO 8601 datetime string
                dt = datetime.fromisoformat(merged_at.replace('Z', '+00:00'))

                # Format datetime object in the desired format
                formatted_datetime = dt.strftime("%d %B %Y - %I:%M %p UTC")

                db = get_db()
                data = {"request_id": pull_request_id, "author":user, "action":"MERGE", "from_branch":head_branch, 
                "to_branch":base_branch, "timestamp":formatted_datetime}  # Assuming JSON data is sent in the POST request
            
            else: # It implies a 'PULL REQUEST' action
                pull_request_action = info['action']
                pull_request_id = info['pull_request']['id']
                user = info['pull_request']['user']['login']
                base_branch = info['pull_request']['base']['ref']
                head_branch = info['pull_request']['head']['ref']
                created_at = info['pull_request']['created_at']

                # Parse ISO 8601 datetime string
                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))

                # Format datetime object in the desired format
                formatted_datetime = dt.strftime("%d %B %Y - %I:%M %p UTC")

                db = get_db()
                data = {"pull_request_action":pull_request_action,"request_id": pull_request_id, "author":user, "action":"PULL_REQUEST", "from_branch":head_branch, 
                "to_branch":base_branch, "timestamp":formatted_datetime}  # Assuming JSON data is sent in the POST request
        
        # Add the data to MongoDB collection
        db['MyCollection'].insert_one(data)
        return jsonify({"message": "Data inserted successfully"}), 201
        

@webhook.route('/')
def root():
    db = get_db()
    result = list(db['MyCollection'].find({}, {'_id': 0}))  # Retrieve all documents
    return render_template('index.html')

@webhook.route('/getdata')
def getdata():
    db = get_db()
    result = list(db['MyCollection'].find({}, {'_id': 0}))  # Retrieve all documents
    return result