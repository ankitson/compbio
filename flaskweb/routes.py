"""Routes for parent Flask app."""
from flask import render_template
from flask import current_app as app

@app.route('/')
def home():
    """Landing page."""
    return """
      <h1>Hello from Flask</h1>
      <a href="/dash/">Dash App</a>
    """