from flask import render_template, session;
from models.quackservice import QuackService;

class MentionsController:
    def index(self):
        quacks = get_quacks_by_mention( get_username_by_id( session['id'] ) );

        return render_template( 'mentions.html', quacks=quacks, msg='' );