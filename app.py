from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_12345'  # Needed for flash messages

# Storage for our todos (list of dictionaries)
todos = []
next_id = 1

@app.route('/')
def index():
    """Display all todo items"""
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    """Add a new todo item"""
    global next_id
    
    title = request.form.get('title')
    description = request.form.get('description')
    
    if not title:
        flash('Title is required!', 'error')
        return redirect(url_for('index'))
    
    todo = {
        'id': next_id,
        'title': title,
        'description': description,
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    todos.append(todo)
    next_id += 1
    flash('Todo added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    """Mark a todo as complete/incomplete"""
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            status = "completed" if todo['completed'] else "uncompleted"
            flash(f'Todo marked as {status}!', 'success')
            break
    
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    """Delete a todo item"""
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    flash('Todo deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    """Edit a todo item"""
    todo = None
    for t in todos:
        if t['id'] == todo_id:
            todo = t
            break
    
    if not todo:
        flash('Todo not found!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if title:
            todo['title'] = title
            todo['description'] = description
            flash('Todo updated successfully!', 'success')
            return redirect(url_for('index'))
    
    return render_template('edit.html', todo=todo)

if __name__ == '__main__':
    app.run(debug=True)