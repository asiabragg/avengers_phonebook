from avengers_pkg import app, db
from avengers_pkg.models import User, Requests

@app.shell_context_processor
def make_shell_context():
    return{'db': db, 'User': User, 'Requests': Requests}