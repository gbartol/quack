from flask import session, redirect;

class LogoutController:
    def index(self):
        session['id'] = None;
        return redirect('/login');