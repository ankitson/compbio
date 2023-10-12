"""Routes for parent Flask app."""
from flask import redirect, render_template
from flask import current_app as app

@app.route('/')
def home():
    """Landing page."""
    return redirect('/dash')

    return """
      <h1>Hello from Flask</h1>
      <a href="/dash/">Dash App</a>
    """