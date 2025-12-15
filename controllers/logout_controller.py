from flask import session, redirect;

class LogoutController:
    def index(self):
        session.clear();
        return redirect('/login');
