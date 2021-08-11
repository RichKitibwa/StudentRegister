from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)
app.secret_key = b'_5#y2L"F4Qz\n\xec]/'


class Students(db.Model):
    id = db.Column('Student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    course = db.Column(db.String(200))
    college = db.Column(db.String(200))
    year = db.Column(db.String(10))

    def __repr__(self):
        return '<Student %r>' % self.id

    def __init__(self, name, course, college, year):
        self.name = name
        self.course = course
        self.college = college
        self.year = year


@app.route('/')
def index():
    return render_template('index.html', students=Students.query.all())


@app.route('/register', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['course'] or not request.form['college'] or not request.form[
            'year']:
            flash('Please enter all fields', 'error')
        else:
            student = Students(request.form['name'], request.form['course'], request.form['college'],
                               request.form['year'])

            try:
                db.session.add(student)
                db.session.commit()
                flash('Record was successfully added')
                return redirect('/')
            except:
                return "There was an error adding the student"

        return redirect(url_for('register_student'))

    return render_template('register_student.html')


@app.route('/delete/<int:id>')
def delete(id):
    delete_student = Students.query.get_or_404(id)

    try:
        db.session.delete(delete_student)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting that student."


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
