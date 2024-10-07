from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

tasks = []
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_task', methods=['POST'])
def create_task():
    title = request.form.get('title')
    description = request.form.get('description', '')
    task_type = request.form.get('type')
    priority = request.form.get('priority')
    creator = request.form.get('creator')
    performer = request.form.get('performer') or None

    task = {
        'number': len(tasks) + 1,
        'title': title,
        'description': description,
        'type': task_type,
        'priority': priority,
        'creator': creator,
        'performer': performer,
        'status': 'To Do',
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    tasks.append(task)
    return redirect('/task_manager')

@app.route('/update_task/<int:task_number>', methods=['POST'])
def update_task(task_number):
    new_status = request.form.get('new_status')
    for task in tasks:
        if task['number'] == task_number:
            task['status'] = new_status
            task['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    return redirect('/task_manager')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('task_manager'))
    return "Invalid credentials, please try again."

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    if password == confirm_password and username not in users:
        users[username] = password
        return redirect(url_for('index'))
    return "Registration failed. Username might already be taken or passwords do not match."

@app.route('/task_manager')
def task_manager():
    if 'username' in session:
        return render_template('task_manager.html', tasks=tasks, username=session['username'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
