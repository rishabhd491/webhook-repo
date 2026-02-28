from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
import os

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("/github-receiver", methods=["GET", "POST"])
def github_webhook():
    if request.method == "GET":
        return jsonify({"message": "Webhook endpoint is active and waiting for POST requests"}), 200
        
    # Use from app import mongo locally to avoid circular import if needed
    from app import mongo
    
    data = request.json
    if not data:
        return jsonify({"message": "No data received"}), 400

    # Determine action and extract relevant information
    # GitHub sends event type in 'X-GitHub-Event' header
    event_type = request.headers.get("X-GitHub-Event")

    if event_type == "ping":
        return jsonify({"message": "Ping received successfully"}), 200
    
    action = None
    author = None
    from_branch = None
    to_branch = None
    request_id = None
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if event_type == "push":
        action = "PUSH"
        author = data.get("pusher", {}).get("name")
        # For push, to_branch is 'ref' (e.g., 'refs/heads/master')
        to_branch = data.get("ref", "").split("/")[-1]
        request_id = data.get("after") # Commit hash
        from_branch = None # No 'from' branch for a push
        
    elif event_type == "pull_request":
        # Check for pull request action
        pr_action = data.get("action")
        if pr_action == "closed" and data.get("pull_request", {}).get("merged"):
            action = "MERGE"
            author = data.get("pull_request", {}).get("merged_by", {}).get("login")
            from_branch = data.get("pull_request", {}).get("head", {}).get("ref")
            to_branch = data.get("pull_request", {}).get("base", {}).get("ref")
            request_id = data.get("pull_request", {}).get("merge_commit_sha")
        elif pr_action == "opened":
            action = "PULL_REQUEST"
            author = data.get("pull_request", {}).get("user", {}).get("login")
            from_branch = data.get("pull_request", {}).get("head", {}).get("ref")
            to_branch = data.get("pull_request", {}).get("base", {}).get("ref")
            request_id = str(data.get("pull_request", {}).get("id"))

    if action:
        # Save to MongoDB
        mongo.db.actions.insert_one({
            "request_id": request_id,
            "author": author,
            "action": action,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp
        })
        return jsonify({"message": f"Successfully processed {action} event"}), 201
    else:
        return jsonify({"message": "Unsupported event or action"}), 200

@webhook_bp.route("/actions", methods=["GET"])
def get_actions():
    from app import mongo
    # Fetch all actions sorted by timestamp descending
    actions = list(mongo.db.actions.find({}, {"_id": 0}).sort("timestamp", -1))
    return jsonify(actions)
