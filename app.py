from flask import Flask, jsonify
from threading import Lock
import os

app = Flask(__name__)

# File path for persistent storage
COUNTER_FILE = '/data/counter.txt'
lock = Lock()

def initialize_counter():
    """Create the counter file with 0 if it doesn't exist"""
    if not os.path.exists(COUNTER_FILE):
        os.makedirs(os.path.dirname(COUNTER_FILE), exist_ok=True)
        with open(COUNTER_FILE, 'w') as f:
            f.write('0')
        return 0
    return None

def read_counter():
    """Read the current counter value from file"""
    try:
        with open(COUNTER_FILE, 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        # If file doesn't exist or contains invalid data, initialize it
        return initialize_counter() or 0

def write_counter(value):
    """Write the new counter value to file"""
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(value))

@app.route('/')
def home():
    return jsonify({
        "message": "Persistent Counter API is running!",
        "endpoints": {
            "/count": "Get next number (basic)",
            "/count_lock": "Get next number (thread-safe)", 
            "/current": "Get current number without incrementing",
            "/reset": "Reset counter to 0",
            "/health": "Check API status"
        }
    })

@app.route('/count')
def get_count():
    """Basic version - potential for race conditions"""
    current_count = read_counter()
    new_count = current_count + 1
    write_counter(new_count)
    return jsonify({
        "previous_count": current_count,
        "new_count": new_count,
        "message": "Counter incremented (basic version)"
    })

@app.route('/count_lock')
def get_count_safe():
    """Thread-safe version using file locking"""
    with lock:
        current_count = read_counter()
        new_count = current_count + 1
        write_counter(new_count)
    
    return jsonify({
        "previous_count": current_count,
        "new_count": new_count, 
        "message": "Counter incremented (thread-safe version)"
    })

@app.route('/current')
def get_current():
    """Get current value without incrementing"""
    current_count = read_counter()
    return jsonify({
        "current_count": current_count,
        "message": "Current counter value"
    })

@app.route('/reset')
def reset_counter():
    """Reset counter to 0"""
    with lock:
        write_counter(0)
    return jsonify({
        "message": "Counter has been reset to 0",
        "new_count": 0
    })

@app.route('/health')
def health_check():
    current_count = read_counter()
    return jsonify({
        "status": "healthy",
        "counter_value": current_count,
        "storage_file": COUNTER_FILE,
        "file_exists": os.path.exists(COUNTER_FILE)
    })

if __name__ == '__main__':
    # Initialize counter file on startup
    initialize_counter()
    print(f"Counter initialized. Storage file: {COUNTER_FILE}")
    print(f"Current counter value: {read_counter()}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

    # Add this to the bottom of your app.py, replacing the last lines:
if __name__ == '__main__':
    # Initialize counter file on startup
    initialize_counter()
    print(f"Counter initialized. Storage file: {COUNTER_FILE}")
    print(f"Current counter value: {read_counter()}")
    
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)