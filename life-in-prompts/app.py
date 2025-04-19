import os
import json
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO
from services.anthropic_service import AnthropicService
from services.threads_service import ThreadsService

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

# Constants
ANTHROPIC_API_KEY = ""
THREADS_USERNAME = ""
THREADS_PASSWORD = ""

# Initialize services
anthropic_service = AnthropicService(ANTHROPIC_API_KEY)
threads_service = ThreadsService()  # Using default credentials from the class

# Store conversation history in memory
conversation_history = []

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        # Get text prompt
        prompt = request.form.get('prompt', '')
        
        # Check if there's an image
        image_file = request.files.get('image')
        image_data = None
        
        if image_file:
            image_data = image_file.read()
        
        # Post to Threads first (the prompt, not the response)
        threads_result = False
        threads_message = "Not posted to Threads"
        

        image_file = request.files.get('image')
        image_file.stream.seek(0)

        if image_file:
            threads_result, threads_message = threads_service.post_with_image(prompt, [image_file])
        else:
            threads_result, threads_message = threads_service.post_text(prompt)
            
        image_file = request.files.get('image')
        
        # Get response from Anthropic
        response = anthropic_service.get_response(prompt, image_data)
        
        # Add to conversation history
        conversation_history.append({
            "role": "user",
            "content": prompt,
            "has_image": image_data is not None
        })
        conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Return response
        return jsonify({
            "response": response,
            "threads_posted": threads_result,
            "threads_message": threads_message
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/conversation')
def get_conversation():
    """Get conversation history"""
    return jsonify(conversation_history)

@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({"status": "success"})

if __name__ == '__main__':
    service = ThreadsService()
    
    if service.is_logged_in():
        print(f"✅ Logged in as: {service.username} (User ID: {service.user_id})")
    else:
        print("❌ Not logged in to Threads")
    
    # Run the app
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
