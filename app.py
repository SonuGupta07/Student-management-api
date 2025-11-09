from flask import Flask, request, jsonify
from models import db, Student
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = Student(name=data['name'], age=data['age'], course=data['course'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully!"}), 201

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{"id": s.id, "name": s.name, "age": s.age, "course": s.course} for s in students])

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found"}), 404
    student.name = data['name']
    student.age = data['age']
    student.course = data['course']
    db.session.commit()
    return jsonify({"message": "Student updated successfully!"})

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
