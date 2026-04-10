# Flask SQLAlchemy Workout Application Backend

## Description
A backend API for a workout tracking application used by personal trainers. Built with Flask, SQLAlchemy, and Marshmallow. The API tracks workouts and their associated exercises, with full CRUD functionality.

## Installation

1. Clone the repository:
   git clone <your-repo-url>
   cd Flask-SQLAlchemy-Workout-Application-Backend

2. Install dependencies:
   pipenv install

3. Enter the virtual environment:
   pipenv shell

4. Navigate to server folder:
   cd server

5. Run migrations:
   flask db upgrade head

6. Seed the database:
   python3 seed.py

## Running the App
   flask run --port=5555

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /workouts | List all workouts |
| GET | /workouts/<id> | Get a single workout with exercises |
| POST | /workouts | Create a new workout |
| DELETE | /workouts/<id> | Delete a workout |
| GET | /exercises | List all exercises |
| GET | /exercises/<id> | Get a single exercise |
| POST | /exercises | Create a new exercise |
| DELETE | /exercises/<id> | Delete an exercise |
| POST | /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises | Add an exercise to a workout |
