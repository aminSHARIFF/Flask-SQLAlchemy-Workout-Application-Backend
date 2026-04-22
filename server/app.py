from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema, exercises_schema,
    workout_schema, workouts_schema,
    workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


# ==================================================================
# Workout Routes
# ==================================================================

@app.route('/workouts', methods=['GET'])
def get_workouts():
    """Return a list of all workouts."""
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    """
    Return a single workout by ID.
    Response includes all associated exercises with their
    sets, reps, and duration data.
    """
    workout = Workout.query.get_or_404(id)
    return make_response(jsonify(workout_schema.dump(workout)), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    """
    Create a new workout.
    Expects JSON body with: date, duration_minutes, and optionally notes.
    """
    data = request.get_json()

    # validate against schema before touching the database
    errors = workout_schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)

    try:
        from datetime import date
        if 'date' in data and isinstance(data['date'], str):
            data['date'] = date.fromisoformat(data['date'])

        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
        return make_response(jsonify(workout_schema.dump(workout)), 201)
    except ValueError as e:
        # catches model-level validation errors
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    """
    Delete a workout by ID.
    Associated WorkoutExercises are deleted automatically via cascade.
    """
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({'message': f'Workout {id} deleted successfully.'}), 200)


# ==================================================================
# Exercise Routes
# ==================================================================

@app.route('/exercises', methods=['GET'])
def get_exercises():
    """Return a list of all exercises."""
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    """
    Return a single exercise by ID.
    Response includes all workouts this exercise has been added to.
    """
    exercise = Exercise.query.get_or_404(id)
    return make_response(jsonify(exercise_schema.dump(exercise)), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    """
    Create a new exercise.
    Expects JSON body with: name, category, and optionally equipment_needed.
    """
    data = request.get_json()

    # validate against schema before touching the database
    errors = exercise_schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)

    try:
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
        return make_response(jsonify(exercise_schema.dump(exercise)), 201)
    except ValueError as e:
        # catches model-level validation errors
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    """
    Delete an exercise by ID.
    Associated WorkoutExercises are deleted automatically via cascade.
    """
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({'message': f'Exercise {id} deleted successfully.'}), 200)


# ==================================================================
# WorkoutExercise Route
# ==================================================================

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    """
    Add an exercise to a workout by creating a WorkoutExercise record.
    workout_id and exercise_id come from the URL.
    Expects JSON body with at least one of: reps, sets, duration_seconds.
    """
    # make sure both parent records actually exist before proceeding
    Workout.query.get_or_404(workout_id)
    Exercise.query.get_or_404(exercise_id)

    data = request.get_json()
    data['workout_id'] = workout_id
    data['exercise_id'] = exercise_id

    # validate against schema
    errors = workout_exercise_schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)

    try:
        we = WorkoutExercise(**data)
        db.session.add(we)
        db.session.commit()
        return make_response(jsonify(workout_exercise_schema.dump(we)), 201)
    except ValueError as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)