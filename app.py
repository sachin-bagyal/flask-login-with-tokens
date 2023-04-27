from flask import Flask, render_template, request, make_response, redirect, url_for
import uuid

app = Flask(__name__)
app.secret_key = 'secretkey'

# Store tokens in a dictionary
tokens = {}

@app.route('/')
def index():
    if 'token' in request.cookies and request.cookies['token'] in tokens:
        return redirect(url_for('secret_screen'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check user's credentials
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            # Generate a unique token
            token = str(uuid.uuid4())
            # Store the token in the tokens dictionary
            tokens[token] = request.form['username']
            # Set the token as a cookie
            response = make_response(redirect(url_for('secret_screen')))
            response.set_cookie('token', token)
            return response
        else:
            return render_template('login.html', error='Invalid credentials')
    else:
        return render_template('login.html')

@app.route('/secret_screen')
def secret_screen():
    if 'token' in request.cookies and request.cookies['token'] in tokens:
        return render_template('secret_screen.html', username=tokens[request.cookies['token']])
    else:
        return redirect(url_for('login'))

@app.route('/get_profile')
def get_profile():
    return tokens[request.cookies['token']]

@app.route('/logout',  methods=['POST'])
def logout():
    if 'token' in request.cookies and request.cookies['token'] in tokens:
        # Remove the token from the tokens dictionary
        del tokens[request.cookies['token']]
    # Delete the token cookie
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('token')
    return response
