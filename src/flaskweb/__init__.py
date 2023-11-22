from flask import Flask


def init_app():
  """Contruct core Flask application."""
  app = Flask(__name__, 
              static_folder='../static',
              instance_relative_config=False,
              template_folder='../templates')

  with app.app_context():
    from . import routes

    from dashweb.dashapp import init_dash
    app = init_dash(app)
  
    return app
  