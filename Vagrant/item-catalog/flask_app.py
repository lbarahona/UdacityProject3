import auth_db
import uuid
from bleach import clean
from config_file import *
from db_items import *
from default_data import load_default_data
from dicttoxml import dicttoxml
from flask import Flask, render_template, request, redirect, url_for,\
    flash, jsonify, g, session
from flask.ext.github import GitHub

# load in our simple config
# setup flask
app = Flask(__name__)
app.config.from_object(__name__)

# setup github-flask
github = GitHub(app)


# before and after requests
@app.before_request
def before_request():
    """ runs before all requests to move user_id from session to g.user """
    # A flask g (global) variable for the user that is set empty to start
    g.user = None
    # If the flask session has a user_id store it in our g.user variable
    if 'user_id' in session:
        g.user = auth_db.User.query.get(session['user_id'])


@app.after_request
def after_request(response):
    """ runs after all requests to remove the SQLAlchemy session before
     continuing """
    auth_db.db_session.remove()
    return response


# reset data routes
@app.route('/resetdatajson')
def reset_data_json():
    """ return json for use in an ajax modal for full data reset """
    token = get_token()
    modaljson = render_template('resetdatamodal.html',
                                user_name=get_user_name(), token=token)
    return jsonify(result=modaljson)


@app.route('/resetdata', methods=['POST'])
def reset_data():
    """ reset all data from the company and items tables to default.  This
     should not be in the production version without extra checks """
    # check login and secure token using check_security function
    token = request.args.get('token', type=str)
    if check_security(
            token, "Must be logged in to reset all data.",
            "Secure token did not match when trying to reset all data!"):
        empty_all_data()
        load_default_data(DBSession)
        flash("All items and companies have been restored to their default values!")
    kill_token()
    return redirect(url_for('back'))


# start main app page related routes
# Main index
@app.route('/')
def index():
    # store this as a key page that we can come back to after a redirect
    session['redir'] = url_for('index')
    companies = all_companies_db()
    token = get_token()
    for company in companies:
        company.items = get_sales_items_from_id_db(company.id)
    return render_template('app.html', frontpage="true",
                           companies=companies,
                           user_name=get_user_name(), token=token)


# filtered index
@app.route('/company/<int:company_id>/')
def company(company_id):
    # store this as a key page that we can come back to after a redirect
    session['redir'] = url_for('company', company_id=company_id)
    companies = (get_company_from_id_db(company_id),)
    token = get_token()
    for company in companies:
        company.items = get_sales_items_from_id_db(company_id)
    return render_template('app.html', frontpage="false",
                           companies=companies,
                           user_name=get_user_name(), token=token)
# end main app page related routes


# start of company related routes
# Add
@app.route('/addcompanyjson')
def add_company_json():
    """ return json for use in an ajax modal for add company form """
    token = get_token()
    modaljson = render_template('addcompanymodal.html',
                                user_name=get_user_name(), token=token)
    return jsonify(result=modaljson)


@app.route('/addcompany', methods=['POST'])
def add_company():
    """ add a company to the db after checking login """
    # check login and secure token using check_security function
    token = request.args.get('token', type=str)
    if check_security(
            token, "Must be logged in to add a company.",
            "Secure token did not match when trying to add a company!"):
        try:
            name = clean(request.form['company_name'])
            site_uri = clean(request.form['company_site_uri'])
            add_company_db(name=name, site_uri=site_uri)
            flash("new company added!")
        except:
            flash("Error adding company!")
    kill_token()
    return redirect(url_for('back'))


# Delete
@app.route('/deletecompanyjson')
def delete_company_json():
    """ return json for use in an ajax modal for item delete confirmation """
    # if id sent can't be converted to int, id assigned is 0
    company_id = request.args.get('company_id', 0, type=int)
    company = get_company_from_id_db(company_id)
    token = get_token()
    modaljson = render_template('deletecompanymodal.html', company=company,
                                user_name=get_user_name(), token=token)
    return jsonify(result=modaljson)


@app.route('/deletecompany', methods=['POST'])
def delete_company():
    """ delete a company and all of it's items after checking login """
    company_id = request.args.get('company_id', 0, type=int)
    # check login and secure token using check_security function
    token = request.args.get('token', type=str)
    if check_security(
            token, "Must be logged in to delete companies.",
            "Secure token did not match when trying to delete a company!"):
        try:
            company = get_company_from_id_db(company_id)
        except:
            company = None
        if company:
            try:
                delete_company_db(company_id)
                flash("Company has been deleted!")
            except:
                flash("Error deleting the Company!")
        else:
            flash("Company to delete was not found!")
    kill_token()
    return redirect(url_for('back'))


# Edit
@app.route('/editcompanyjson')
def edit_company_json():
    """ return json for use in an ajax modal allowing company edits """
    company_id = request.args.get('company_id', 0, type=int)
    company = get_company_from_id_db(company_id)
    token = get_token()
    modaljson = render_template('editcompanymodal.html', company=company,
                                user_name=get_user_name(), token=token)
    return jsonify(result=modaljson)


@app.route('/editcompany', methods=['POST'])
def edit_company():
    """ edit a company after checking login """
    company_id = request.args.get('company_id', 0, type=int)
    # check login and secure token using check_security function
    token = request.args.get('token', type=str)
    if check_security(
            token, "Must be logged in to edit companies.",
            "Secure token did not match when trying to edit a company!"):
        try:
            name = clean(request.form['company_name'])
            site_uri = clean(request.form['company_site_uri'])
            edit_company_db(name=name, site_uri=site_uri,
                            company_id=company_id)
            flash("company edited!")
        except:
            flash("company edit failed!")
    kill_token()
    return redirect(url_for('back'))
# end of company related routes


# start of item related routes
# View
@app.route('/itemjson')
def item_json():
    """ return json for use in an ajax modal showing item information """
    # if id sent can't be converted to int, id assigned is 0
    company_id = request.args.get('company_id', 0, type=int)
    item_id = request.args.get('item_id', 0, type=str)
    item = get_sales_item_from_id_db(company_id, item_id)
    modaljson = render_template('itemmodal.html', company_id=company_id,
                                item=item, user_name=get_user_name())
    return jsonify(result=modaljson)


# Add
@app.route('/additemjson')
def add_item_json():
    """ return json for use in an ajax modal for add item form """
    company_id = request.args.get('company_id', 0, type=int)
    company = get_company_from_id_db(company_id)
    token = get_token()
    modaljson = render_template('additemmodal.html', company=company,
                                user_name=get_user_name(),
                                token=token)
    return jsonify(result=modaljson)


@app.route('/additem', methods=['POST'])
def add_item():
    """ add a sales item after checking login """
    company_id = request.args.get('company_id', 0, type=int)
    # check login and secure token using check_security function
    token = request.args.get('token', type=str)
    if check_security(
            token, "Must be logged in to add items.",
            "Secure token did not match when trying to add an item!"):
        try:
            name = clean(request.form['item_name'])
            price = clean(request.form['item_price'])
            image_uri = clean(request.form['item_image_uri'])
            add_sales_item_db(name=name, price=price, image_uri=image_uri,
                              company_id=company_id)
            flash("item added!")
        except:
            flash("item add failed!")
    kill_token()
    return redirect(url_for('back'))


# Edit
@app.route('/edititemjson')
def edit_item_json():
    """ return json for use in an ajax modal allowing item edits """
    company_id = request.args.get('company_id', 0, type=int)
    item_id = request.args.get('item_id', 0, type=int)
    item = get_sales_item_from_id_db(company_id, item_id)
    token = get_token()
    modaljson = render_template('edititemmodal.html', company_id=company_id,
                                item=item, user_name=get_user_name(),
                                token=token)
    return jsonify(result=modaljson)


# TODO consider sharing redundant code between add and edit routes
@app.route('/edititem', methods=['POST'])
def edit_item():
    """ edit a sales item after checking login """
    company_id = request.args.get('company_id', 0, type=int)
    item_id = request.args.get('item_id', 0, type=int)
    # check login and secure token using check_security function
    token = request.args.get('token', type=str)
    if check_security(
            token, "Must be logged in to edit items.",
            "Secure token did not match when trying to edit an item!"):
        try:
            name = clean(request.form['item_name'])
            price = clean(request.form['item_price'])
            image_uri = clean(request.form['item_image_uri'])
            edit_sales_item_db(name=name, price=price, image_uri=image_uri,
                               company_id=company_id, item_id=item_id)
            flash("item edited!")
        except:
            flash("item edit failed!")
    kill_token()
    return redirect(url_for('back'))


# Delete
@app.route('/deleteitemjson')
def delete_item_json():
    """ return json for use in an ajax modal for item delete confirmation """
    # if id sent can't be converted to int, id assigned is 0
    company_id = request.args.get('company_id', 0, type=int)
    item_id = request.args.get('item_id', 0, type=str)
    item = get_sales_item_from_id_db(company_id, item_id)
    token = get_token()
    modaljson = render_template('deleteitemmodal.html', company_id=company_id,
                                item=item, user_name=get_user_name(),
                                token=token)
    return jsonify(result=modaljson)


@app.route('/deleteitem', methods=['POST'])
def delete_item():
    """ delete a sales item from a company after checking login """
    company_id = request.args.get('company_id', 0, type=int)
    item_id = request.args.get('item_id', 0, type=int)
    # check login and secure token using check_security function
    token = request.args.get('token', type=str)
    if check_security(
            token, "Must be logged in to delete items.",
            "Secure token did not match when trying to delete an item!"):
        try:
            item = get_sales_item_from_id_db(company_id, item_id)
        except:
            item = None
        if item:
            try:
                delete_sales_item_db(company_id, item_id)
                flash("Item has been deleted!")
            except:
                flash("Error deleting the item!")
        else:
            flash("Item to delete was not found!")
    kill_token()
    return redirect(url_for('back'))
# end of item related routes


# JSON API route
@app.route('/company/<int:company_id>/JSON')
def company_items_json(company_id):
    company = get_company_from_id_db(company_id)
    items = get_sales_items_from_id_db(company_id)
    return jsonify(Company=[company.serialize],
                   SalesItems=[item.serialize for item in items])


# XML API route
@app.route('/company/<int:company_id>/XML')
def company_items_xml(company_id):
    company = get_company_from_id_db(company_id)
    items = get_sales_items_from_id_db(company_id)
    xml = dicttoxml({'Company': [company.serialize],
                     'SalesItems': [item.serialize for item in items]})
    return xml, 200, {'Content-Type': 'text/xml;'}


# special route used to go back to the last important page visited
@app.route('/back')
def back():
    # if we have cisited any important pages use them and if not go to index
    this_url = session.get('redir', None)
    if this_url is None:
        return redirect(url_for('index'))
    else:
        return redirect(this_url)


# start github oauth related routes
# flask-github extension specific token utility
@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token


# github-oauth callback handler
@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        return redirect(next_url)
    # look for and if necessary store our user in the user database now
    user = auth_db.User.query.filter_by(
        github_access_token=oauth_token).first()
    if user is None:
        user = auth_db.User(oauth_token)
        auth_db.db_session.add(user)

    auth_db.db_session.commit()
    session['user_id'] = user.id

    return redirect(url_for('back'))


# login
# TODO: add a javascript spinner while the user waits on oauth and username
@app.route('/login')
def login():
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        flash("Already logged in")
        return redirect(url_for('back'))


# logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    kill_token()
    return redirect(url_for('back'))


# current username as JSON for ajax use
@app.route('/usernamejson')
def username_json():
    this_id = session.get('user_id', None)
    if this_id is None:
        return jsonify({'username': "unknown"})
    else:
        user_name = session.get('username', None)
    if user_name is None:
        user_name = get_user_name()
    return jsonify({'username': username})


# remove all users
@app.route('/killusers')
def killusers():
    """ this will remove all users stored in the user database and should
    not be included in the production environment without an admin system """
    auth_db.empty_users()
    return redirect(url_for('logout'))
# end github oauth related routes


# helper to fetch the current username from github and store it
def get_user_name():
    # try to get it from the session
    user_name = session.get('username', None)
    if user_name is None:
        # if it is not there, try to get it form logged in user DB entry
        this_id = session.get('user_id', None)
        if this_id is not None:
            thisuser = auth_db.get_user_by_id(this_id)
            if thisuser != []:
                user_name = thisuser.username
            # if it is not there either try to get it from github
            if user_name is None:
                user_name = str(github.get('user')['name'])
                auth_db.add_user_name(this_id, user_name)
            session['username'] = user_name
    return user_name


# Secure form token helper functions
def get_token():
    ''' This will be used as a secure temporary token for this user session.
    it will be generated for each ajax modal and removed on use or logout '''
    token = uuid.uuid4().hex
    session['token'] = token
    return token


def kill_token():
    ''' Remove the current token so it can't be used again '''
    session.pop('token', None)


def check_security(token, login_error, token_error):
    ''' this helper function assists in confirming login and secure token
     it takes in a login token and 2 possible error strings and returns true
     if everything looks good '''
    this_token = session.get('token', None)
    this_id = session.get('user_id', None)
    if this_id is None:
        flash(login_error)
    elif this_token is None or this_token != token:
        flash(token_error)
    else:
        return True


if __name__ == '__main__':
    # auth_db.init_db()
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
