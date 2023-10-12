"""Application entry point."""
from flaskweb import init_app

app = init_app()

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=3001, debug=True)
