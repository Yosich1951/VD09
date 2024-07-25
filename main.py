from app import app, db
from app.models import User

# with app.app_context():
#     db.create_all()

if __name__ == 'main':
    app.run(debug=True)