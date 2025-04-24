from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db"
# db = SQLAlchemy(); db.init_app(app)
db = SQLAlchemy(app)              
# ma = Marshmallow(); ma.init_app(app)
ma = Marshmallow(app)


# Model
class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
# Schema
class StudentsSchema(SQLAlchemySchema):
    class Meta:
        model = Students
        load_instance = True
        
    id = auto_field()
    name = auto_field()
    age = auto_field()
    
student_schema = StudentsSchema()
students_schema = StudentsSchema(many=True)

# home
@app.route("/")
def home():
    return jsonify({"message":"Home Page"})

# add students
@app.route("/students", methods=["POST"])
def add_students():
    student_details = request.get_json()
    if "student_list" in student_details:
        new_students = [Students(name=s.get("name"), age=s.get("age")) for s in student_details.get("student_list")]
        db.session.add_all(new_students)
    else:
        new_student = Students(name=student_details.get("name"), age=student_details.get("age"))
        db.session.add(new_student)
    db.session.commit()
    return jsonify({"message":"added successfully"}), 201

# get students
@app.route("/students", methods=["GET"])
def get_students():
    students = Students.query.all()
    return jsonify(students_schema.dump(students))

# get single student
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = Students.query.get_or_404(student_id)
    return jsonify(student_schema.dump(student))

# update student
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = Students.query.get_or_404(student_id)
    update_student = request.get_json()
    student.name = update_student.get("name", student.name)
    student.age = update_student.get("age", student.age)
    db.session.commit()
    return jsonify({"message":"updated successfully"})

# delete student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = Students.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message":"deleted successfully"})
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
                
    app.run(debug=True)