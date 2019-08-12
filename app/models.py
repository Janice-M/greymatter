from . import db
from . import login_manager
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(UserMixin,db.Model):
    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    greymatter = db.relationship('Greymatter', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref = 'user', lazy = 'dynamic')
    upvotes = db.relationship('Upvote', backref = 'user', lazy = 'dynamic')
    downvotes = db.relationship('Downvote', backref = 'user', lazy = 'dynamic')


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'{self.username}'

    class Role(db.Model):

        __tablename__='roles'
    
        id=db.Column(db.Integer, primary_key=True)
        name=db.Column(db.String(255), unique=True)
        default = db.Column(db.Boolean, default=False, index=True)
        permissions = db.Column(db.Integer)
        users = db.relationship('User', backref='role', lazy='dynamic')
    

class Greymatter(db.Model):
    '''
    '''
    __tablename__ = 'greymatters'

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    description = db.Column(db.String(), index = True)
    title = db.Column(db.String())
    # downvotes = db.Column(db.Integer, default=int(0))
    # upvotes = db.Column(db.Integer, default=int(0))
    #category = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment',backref='greymatter',lazy='dynamic')
    upvotes = db.relationship('Upvote', backref = 'greymatter', lazy = 'dynamic')
    downvotes = db.relationship('Downvote', backref = 'greymatter', lazy = 'dynamic')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    @classmethod
    def get_greymatters(cls, id):
        greymatters = Greymatter.query.order_by(greymatter_id=id).desc().all()
        return greymatters

    def __repr__(self):
        return f'Greymatter {self.description}'

    

class Comment(db.Model):
    __tablename__='comments'
    
    id = db.Column(db.Integer,primary_key=True)
    greymatter_id = db.Column(db.Integer, db.ForeignKey('greymatters.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    description = db.Column(db.Text)

    
    def __repr__(self):
        return f"Comment : id: {self.id} comment: {self.description}"


class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer,primary_key=True)
    upvote = db.Column(db.Integer,default=1)
    greymatter_id = db.Column(db.Integer,db.ForeignKey('greymatters.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_upvotes(self):
        db.session.add(self)
        db.session.commit()


    def add_upvotes(cls,id):
        upvote_greymatter = Upvote(user = current_user, pitch_id=id)
        upvote_greymatter.save_upvotes()

    
    @classmethod
    def get_upvotes(cls,id):
        upvote = Upvote.query.filter_by(greymatter_id=id).all()
        return upvote

    @classmethod
    def get_all_upvotes(cls,pitch_id):
        upvotes = Upvote.query.order_by('id').all()
        return upvotes

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'



class Downvote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer,primary_key=True)
    downvote = db.Column(db.Integer,default=1)
    greymatter_id = db.Column(db.Integer,db.ForeignKey('greymatters.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_downvotes(self):
        db.session.add(self)
        db.session.commit()


    def add_downvotes(cls,id):
        downvote_greymatter = Downvote(user = current_user, pitch_id=id)
        downvote_greymatter.save_downvotes()

    
    @classmethod
    
    def get_downvotes(cls,id):
        downvote = Downvote.query.filter_by(pitch_id=id).all()
        return downvote

    @classmethod
    
    def get_all_downvotes(cls,pitch_id):
        downvote = Downvote.query.order_by('id').all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'


