from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from os import path
from flask_login import login_manager
from .starter_data import links, user_list

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app=app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Application

    with app.app_context():
        # Clear out any data in the table before initializing the app
        db.drop_all()
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Initialize the given data, for some reason it won't happen unless it's done after the login stuff
    with app.app_context():
        #print('Filling default values now')
        # Fill the User table with defaults
        # Not allowing the passwords to be the same, even with unique set to false
        for u in user_list:
            new_user = User(email=u, password=user_list[u])
            db.session.add(new_user)
            db.session.commit()

        # Checking to see if the defaults were put in correctly
        # users = User.query.all()
        # for user in users:
        #     print(str(user.id) + ' ' + str(user.email) + ' ' + str(user.password) + ' ' + str(user.links))
        #     print(f"")

        # Fill the Application table with given information
        for l in links:
            row = Application(name=l['name'], 
                                description=l['description'],
                                color=l['color'],
                                status=l['default_status'],
                                link=l['link'])
            db.session.add(row)
            db.session.commit()

        # Checking to see if the links have been added correctly
        # applications = Application.query.all()
        # for a in applications:
        #     print(str(a.id) + ' ' +  str(a.name) + ' ' + str(a.description) + ' ' + str(a.color) + ' ' + str(a.status) + ' ' + str(a.link))
        #     print(f"")

        # Fills the links field for each user so that their active links are known
        users = User.query.all()
        for user in users:
            active_apps = Application.query.filter(Application.status == True)
            cur_user = User.query.get(user.id)
            for a in active_apps:
                cur_user.links.append(a)

        db.session.commit()

        ## Check to see if all default 
        # for user in users:
        #     print(str(user.id) + ' ' + str(user.email) + ' ' + str(user.password) + ' ' + str(user.links))
        #     print(f"")
        #print('Default Values have been entered\n')
            
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
