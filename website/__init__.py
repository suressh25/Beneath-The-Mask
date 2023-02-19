from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login  import LoginManager
from os import path
#creating app instance
db=SQLAlchemy()

def create_app():
	app=Flask(__name__)
	app.config['SECRET_KEY']='asdfgh;lkjh'
	app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
	db.init_app(app)
	Bootstrap(app)
	#sepate routers
	from .auth import auth
	from .views import views

	app.register_blueprint(views,url_prefix="/")
	app.register_blueprint(auth,url_prefix="/")
	#database
	from .modals import User
	create_database(app)
	#login manager
	login_manger=LoginManager(app)
	@login_manger.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

	return app

def create_database(app):
	if not path.exists('website/instance/database.db'):
		with app.app_context():
			db.create_all()
			print("database created!")

