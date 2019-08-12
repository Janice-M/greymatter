from flask import render_template,request,redirect,url_for,abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import Greymatter, User,Comment,Upvote,Downvote
from .forms import GreymatterForm, CommentForm, UpvoteForm
from flask.views import View,MethodView
from .. import db 



@main.route('/', methods = ['GET','POST'])
def index():

    '''
    Root page functions that return the home page and its data
    '''
    
    title = 'Welcome To Greymatter Rafiki'
    
    form = GreymatterForm()
    
    upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)
    
    if form.validate_on_submit():
        post = Greymatter(body=form.body.data, author=current_user._get_current_object())
        post.save_post()
        return redirect(url_for('.index'))

    posts = Greymatter.query.order_by(Greymatter.timestamp.desc()).all()

    return render_template('home.html',upvotes=upvotes, form=form, posts=posts)




@main.route('/pitches/new/', methods = ['GET','POST'])
@login_required
def new_greymatter():
    form = GreymatterForm()
    my_upvotes = Upvote.query.filter_by(greymatter_id = Greymatter.id)
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        owner_id = current_user
        print(current_user._get_current_object().id)
        new_greymatter = Greymatter(owner_id =current_user._get_current_object().id, title = title,
        db.session.add(new_greymatter)
        db.session.commit()
        
        
        return redirect(url_for('main.index'))
    return render_template('pitches.html',form=form)



@main.route('/comment/new/<int:pitch_id>', methods = ['GET','POST'])
@login_required
def new_comment(pitch_id):
    form = CommentForm()
    greymatter=greymatter.query.get(_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description = description, user_id = current_user._get_current_object().id, greymatter_id = greymatter_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('.new_comment', greymatter_id= greymatter_id))

    all_comments = Comment.query.filter_by(greymatter_id = greymatter_id).all()
    return render_template('comments.html', form = form, comment = all_comments, greymatter = greymatter )

    """ The above allows you to add a comment in blog posts at greymatter"""

@main.route('/greymatter/upvote/<int:greymatter_id>/upvote', methods = ['GET', 'POST'])
@login_required
def upvote(greymatter_id):
    greymatter = Greymatter.query.get(greymatter_id)
    user = current_user
    greymatter_upvotes = Upvote.query.filter_by(greymatter_id= greymatter_id)
    
    if Upvote.query.filter(Upvote.user_id==user.id,Upvote.greymatter_id==greymatter_id).first():
        return  redirect(url_for('main.index'))


    new_upvote = Upvote(greymatter_id=greymatter_id, user = current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('main.index'))





@main.route('/greymatter/downvote/<int:greymatter_id>/downvote', methods = ['GET', 'POST'])
@login_required
def downvote(greymatter_id):
    greymatter = Greymatter.query.get(greymatter_id)
    user = current_user
    greymatter_downvotes = Downvote.query.filter_by(greymatter_id= greymatter_id)
    
    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.greymatter_id==greymatter_id).first():
        return  redirect(url_for('main.index'))


    new_downvote = Downvote(greymatter_id=greymatter_id, user = current_user)
    new_downvote.save_downvotes()
    return redirect(url_for('main.index'))


		
   

