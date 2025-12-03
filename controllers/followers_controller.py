from flask import render_template;
from models.quackservice import QuackService;

class FollowersController:
    def index(self):
        followers = QuackService.get_followers_by_user( session['id'] );

        return render_template( 'followers.html', followers=followers );