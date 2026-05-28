from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "my_game_list_secret_key"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    email = request.form.get('email', '')
    action = request.form.get('action', 'login')
    login_identifier = username or email

    conn = get_db_connection()
    if action == 'register':
    
        if not username:
            conn.close()
            return render_template('login.html', error='Username is required for registration.')
        if not password:
            conn.close()
            return render_template('login.html', error='Password is required for registration.')
        if not email:
            conn.close()
            return render_template('login.html', error='Email is required for registration.')
 


        try:
            hashed = generate_password_hash(password)
            conn.execute(
                'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                (username, hashed, email),
            )
            conn.commit()
            conn.close()
            return render_template('login.html', success='Registration successful! You can login now.')
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('login.html', error='Username or email already exists. Please choose a different one.')

    elif action == 'login':

        user = conn.execute('SELECT * FROM users WHERE username=? OR email=?', (login_identifier, login_identifier)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password. Please try again.')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    played_games = conn.execute('SELECT * FROM games WHERE user_id=? AND status=?', (session['user_id'], 'Played')).fetchall()
    wishlist_games = conn.execute('SELECT * FROM games WHERE user_id=? AND status=?', (session['user_id'], 'Wishlist')).fetchall()
    conn.close()
    return render_template('home.html', username=session['username'], played_games=played_games, wishlist_games=wishlist_games)

@app.route('/add_game', methods=['POST'])
def add_game():
    if 'username' not in session:
        return redirect(url_for('index'))
        
    game_name = request.form['game_name']
    status = request.form['status']
  
    conn = get_db_connection()
    conn.execute('INSERT INTO games (user_id, game_name, status) VALUES (?, ?, ?)',
                 (session['user_id'], game_name, status))
    conn.commit()
    conn.close()
    
    return redirect(url_for('home'))


@app.route('/delete_game/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    game = conn.execute('SELECT * FROM games WHERE id=?', (game_id,)).fetchone()
    if not game:
        conn.close()
        return redirect(url_for('home'))


    if game['user_id'] != session['user_id']:
        conn.close()
        return redirect(url_for('home'))

    conn.execute('DELETE FROM games WHERE id=?', (game_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))


@app.route('/mark_played/<int:game_id>', methods=['POST'])
def mark_played(game_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    game = conn.execute('SELECT * FROM games WHERE id=?', (game_id,)).fetchone()
    if not game or game['user_id'] != session['user_id']:
        conn.close()
        return redirect(url_for('home'))

    conn.execute('UPDATE games SET status=? WHERE id=?', ('Played', game_id))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))



@app.route('/rate_game/<int:game_id>', methods=['POST'])
def rate_game(game_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    rating = request.form.get('rating')
    try:
        rating_int = int(rating)
    except (TypeError, ValueError):
        return redirect(url_for('home'))

    if rating_int < 1 or rating_int > 5:
        return redirect(url_for('home'))

    conn = get_db_connection()
    game = conn.execute('SELECT * FROM games WHERE id=?', (game_id,)).fetchone()
    if not game or game['user_id'] != session['user_id']:
        conn.close()
        return redirect(url_for('home'))

    conn.execute('UPDATE games SET rating=? WHERE id=?', (rating_int, game_id))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))






@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(debug=True)