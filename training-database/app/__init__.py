from flask import Flask
from app.extensions import db, login_manager, migrate, bcrypt, cors, mail
from app.logger import logger as log
from .config import Config
from app.models import User, Training_log, TrainingTemplate, Role, Department, AssignedTraining



def create_app(run_setup=True):
    app = Flask(__name__)
    app.config.from_object(Config)
    log.info("App configuration loaded")
    
    db.init_app(app)
    log.info("Database initialized")
    migrate.init_app(app, db)
    log.info("Migration engine initialized")
    
    with app.app_context():
        db.create_all()
        log.info("Database schema created")
        
    login_manager.init_app(app)
    log.info("Login manager initialized")
    
    bcrypt.init_app(app)
    log.info("Password hashing initialized")
    
    cors.init_app(app)
    log.info("Cross-origin resource sharing initialized")
    
    mail.init_app(app)
    log.info("Mail server initialized")
    
    if run_setup:
        from app.setup.db_setup import populate_default_db
        with app.app_context():
            populate_default_db()
            log.info("Default database populated")
        
    
    from app.routes import default
    app.register_blueprint(default)
    
    from app.blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    return app
    

    