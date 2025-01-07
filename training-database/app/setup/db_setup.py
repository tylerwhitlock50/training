from app.extensions import db, logger
from app.models import User, UserStatus, Role, EvaluationType, TrainingResult, Department


def populate_default_db():
    try:
        # Check and create a default department
        department = Department.query.filter_by(name='IT').first()
        if not department:
            department = Department(name='IT')
            db.session.add(department)
            db.session.commit()
            logger.info("Default department 'IT' created.")
        else:
            logger.info("Default department 'IT' already exists.")

        # Check and create user statuses
        active = UserStatus.query.filter_by(status='Active').first()
        if not active:
            active = UserStatus(status='Active', description='User is active and can login')
            db.session.add(active)
            logger.info("UserStatus 'Active' created.")

        inactive = UserStatus.query.filter_by(status='Inactive').first()
        if not inactive:
            inactive = UserStatus(status='Inactive', description='User is inactive and cannot login')
            db.session.add(inactive)
            logger.info("UserStatus 'Inactive' created.")
        db.session.commit()

        # Check and create default user
        user = User.query.filter_by(username='admin').first()
        if not user:
            user = User(
                username='admin',
                role=Role.ADMIN,
                department_id=department.id,
                user_status=active.id
            )
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            logger.info("Default admin user created.")
        else:
            logger.info("Default admin user already exists.")
            
        logger.info("Testing bcrypt password hashing")
        if user.check_password('password'):
            logger.info("Password hashing successful")
        else:
            logger.error("Password hashing failed")

        # Check and create default evaluation types
        evaluation_types = [
            ('Pre-training evaluation', 'Evaluation done before training'),
            ('Post-training evaluation', 'Evaluation done after training'),
            ('Training effectiveness evaluation', 'Evaluation done to determine the effectiveness of the training')
        ]
        for name, description in evaluation_types:
            if not EvaluationType.query.filter_by(name=name).first():
                db.session.add(EvaluationType(name=name, description=description))
                logger.info(f"EvaluationType '{name}' created.")

        # Check and create default training results
        training_results = [
            ('Pass', 'User passed the training'),
            ('Fail', 'User failed the training')
        ]
        for result, description in training_results:
            if not TrainingResult.query.filter_by(result=result).first():
                db.session.add(TrainingResult(result=result, description=description))
                logger.info(f"TrainingResult '{result}' created.")

        # Commit all changes
        db.session.commit()
        logger.info("Default database populated successfully.")

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error populating default database: {e}")
        raise
