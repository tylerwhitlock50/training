from flask import Blueprint, render_template

default = Blueprint('default', __name__, template_folder='templates')

@default.route('/')
def index():
    return render_template('index.html')

@default.route('/health')
def health():
    return {"status": "healthy"}, 200

@default.errorhandler(404)
def not_found(error):
    return {"message": "Resource not found"}, 404

@default.errorhandler(500)
def internal_error(error):
    return {"message": "Internal server error"}, 500

@default.errorhandler(401)
def unauthorized(error):
    return {"message": "Unauthorized"}, 401

@default.errorhandler(403)
def forbidden(error):
    return {"message": "Forbidden"}, 403