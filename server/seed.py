#!/usr/bin/env python3
from datetime import date
from app import app
from models import *

with app.app_context():
    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()

    e1 = Exercise(name='Push Up', category='strength', equipment_needed=False)
    e2 = Exercise(name='Running', category='cardio', equipment_needed=False)
    e3 = Exercise(name='Yoga Stretch', category='flexibility', equipment_needed=False)

    w1 = Workout(date=date(2024, 1, 10), duration_minutes=45, notes='Morning session')
    w2 = Workout(date=date(2024, 1, 12), duration_minutes=30, notes='Evening run')

    db.session.add_all([e1, e2, e3, w1, w2])
    db.session.commit()

    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=e1.id, sets=3, reps=15)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=e3.id, duration_seconds=300)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=e2.id, duration_seconds=1800)

    db.session.add_all([we1, we2, we3])
    db.session.commit()
    print("Seeded successfully!")