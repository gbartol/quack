from flask import render_template, session;
from models.userservice import UserService;
from models.quackservice import QuackService;

class MentionsController:
    def index(self):
        quacks = QuackService.get_quacks_by_mention( UserService.get_username_by_id( session['id'] ) );

        return render_template( 'mentions.html', quacks=quacks, msg='' );