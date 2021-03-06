


from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from databaseHelpers.experience import *
from databaseHelpers.favourite import *

restaurant_page = Blueprint('restaurant_page', __name__, template_folder='templates')


# The home landing page
# Currently nothing is here
@restaurant_page.route('/favourites', methods=['GET', 'POST'])
@restaurant_page.route('/favourites.html', methods=['GET', 'POST'])
def favourites():
    if 'account' not in session:
        return redirect(url_for('login_page.login'))
    if session['type'] != -1:
        return redirect(url_for('home_page.home'))
    else:
        if request.method == 'POST' and 'rid' in request.form:
            rid = request.form['rid']
            return redirect(url_for('search_page.restaurant', rid=rid))
        restaurants = get_favourites(session['account'])
        return render_template('favourites.html', restaurants = restaurants)
