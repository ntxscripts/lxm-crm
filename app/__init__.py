from flask import Flask
from flask_cors import CORS
from .models import db
import os
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lxm_crm.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')
    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    from .routes.api import api_bp
    from .routes.auth import auth_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.cli.command('init-db')
    def init_db():
        """Initialize the database."""
        with app.app_context():
            db.create_all()
            # Create default admin user if none exists
            from .models import User
            from werkzeug.security import generate_password_hash
            if not User.query.filter_by(username='admin').first():
                admin = User(
                    username='admin',
                    password_hash=generate_password_hash('admin'),
                    is_admin=True
                )
                db.session.add(admin)
                db.session.commit()
                print('Default admin user created.')
            print('Database tables created.')

    @app.cli.command('check-db')
    def check_db():
        """Check database state and users."""
        with app.app_context():
            from .models import User
            users = User.query.all()
            print(f"\nFound {len(users)} users in database:")
            for user in users:
                print(f"- Username: {user.username}, Admin: {user.is_admin}")
            print("\nDatabase URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    return app
