###################################################
#                                                 #
#   Includes all routes to achievement page.      #
#   This includes my achievements and create an   #
#   achievement.                                  #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from databaseHelpers.achievement import *
from databaseHelpers.restaurant import *
from databaseHelpers.qr_code import *
from databaseHelpers.achievementProgress import *
from databaseHelpers.employee import *
from databaseHelpers.restaurant import verify_scan_list

achievement_page = Blueprint('achievement_page', __name__, template_folder='templates')

@achievement_page.route('/achievement.html', methods=['GET', 'POST'])
@achievement_page.route('/achievement', methods=['GET', 'POST'])
def achievement():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to owners and employees only, if user is a customer, redirect to home page
    elif session['type'] == -1:
        return redirect(url_for('home_page.home'))
    else:
        if request.method == 'POST':
            aid = request.form['achievement']
            delete_achievement(aid)
    #get achievements
    if session['type'] == 1:
        rid = get_rid(session["account"])
    else:
        rid = get_employee_rid(session["account"])
    achievement_list = filter_expired_achievements(rid)

    return render_template("achievement.html", achievements = achievement_list)


# To create an achievement
@achievement_page.route('/createAchievement.html', methods=['GET', 'POST'])
@achievement_page.route('/createAchievement', methods=['GET', 'POST'])
def create_achievement():
    # If someone is not logged in redirects them to login page, same as coupon
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to owners only, if user is not an owner, redirect to home page
    elif session['type'] == -1 or session["type"] == 0:
        return redirect(url_for('home_page.home'))

    if request.method == 'POST':
        if session["type"] == 1:
            rid = get_rid(session["account"])
        else:
            rid = get_employee_rid(session["account"])
        name = request.form['name']
        experience = request.form['experience']
        points = request.form['points']
        type = int(request.form.get('type'))
        item = request.form['item'].replace(";", "")
        amount = request.form['amount' + str(type)]
        end = request.form['end']
        begin = request.form['start']
        indefinite = "indefinite" in request.form

        value = item + ";" + amount + ";" + str(indefinite) + ";" + begin + ";" + end

        errmsg = get_errmsg(name, experience, points, type, value)

        if not errmsg:
            insert_achievement(rid, name, experience, points, type, value)
            return redirect(url_for('achievement_page.achievement'))
        else:
            return render_template('createAchievement.html', errmsg = errmsg)

    return render_template('createAchievement.html')


@achievement_page.route('/achievementStats.html', methods=['GET', 'POST'])
@achievement_page.route('/achievementStats', methods=['GET', 'POST'])
def achievement_stats():
    # If someone is not logged in redirects them to login page, same as coupon
    if 'account' not in session:
        return redirect(url_for('login_page.login'))
    elif session["type"] == -1 or session["type"] == 0:
        return redirect(url_for('home_page.home'))
    else:
        filter = "all"
        if request.method == 'POST' and "active" in request.form:
            filter = "active"
        elif request.method == 'POST' and "expired" in request.form:
            filter = "expired"

        if session["type"] == 1:
            rid = get_rid(session["account"])
        elif session["type"] == 2:
            rid = get_employee_rid(session["account"])
        achievements = get_achievement_progress_stats(get_achievements_by_rid(rid))
        return render_template('achievementStats.html', achievements = achievements, filter = filter)


@achievement_page.route('/verifyAchievement/<aid>/<uid>', methods=['GET', 'POST'])
def use_achievement(aid, uid):

    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    scanner = session['account']
    rid = get_rid_by_aid(aid)
    access = verify_scan_list(rid)
    rname = get_restaurant_name_by_rid(rid)

    # Page is restricted to employee/owner only, if user is a customer, redirect to home page
    if session['type'] == -1 or scanner not in access:
        return redirect(url_for('qr_page.scan_failure', rname=rname))

    # get achievement
    achievementProgress = get_exact_achivement_progress(aid, uid)
    achievement = get_achievement_by_aid(aid)

    if achievement != 'Not Found':
        # check if achievement is already complete
        if get_progress_completion_status(achievementProgress) == COMPLETE:
            return redirect(url_for('qr_page.scan_forbidden', forbiddenType = 0, itemType = 'Achievement'))

        # check if it is before achievement start date or after achievement end date
        isInDateRange = is_today_in_achievement_date_range(achievement)
        if isInDateRange != 0:
            return redirect(url_for('qr_page.scan_forbidden', forbiddenType = isInDateRange, itemType = 'Achievement'))

        # update progress
        add_one_progress_bar(achievementProgress, aid, uid)
        return redirect(url_for('qr_page.scan_successful'))

    return redirect(url_for('qr_page.scan_nonexistent', scanType = 1))
