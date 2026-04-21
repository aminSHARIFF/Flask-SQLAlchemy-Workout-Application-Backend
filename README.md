# Flask SQLAlchemy Workout Application Backend

## Project Description

A RESTful API backend for a workout tracking application used by personal trainers.
Built with Flask, SQLAlchemy, and Marshmallow, the API allows trainers to manage
workouts and exercises — creating, viewing, and deleting both, and linking exercises
to specific workouts with sets, reps, or duration data.

The application uses a relational SQLite database with three tables: `exercises`,
`workouts`, and `workout_exercises` (a join table). Validations are enforced at
the database, model, and schema level to ensure clean and consistent data.

---

## Installation

**1. Clone the repository:**

```bash
git clone https://github.com/aminSHARIFF/Flask-SQLAlchemy-Workout-Application-Backend.git
cd Flask-SQLAlchemy-Workout-Application-Backend
```

**2. Install dependencies using Pipenv:**

```bash
pipenv install
pipenv shell
```

**3. Navigate into the server directory:**

```bash
cd server
```

**4. Set up the database:**

```bash
flask db init
flask db migrate -m "initial models"
flask db upgrade head
```

**5. Seed the database with sample data:**

```bash
python seed.py
```

---

## Running the Application

```bash
python app.py
```

The API will be available at `http://localhost:5555`

---

## Endpoints

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Get a single workout with its exercises, sets, reps and duration |
| POST | `/workouts` | Create a new workout |
| DELETE | `/workouts/<id>` | Delete a workout and its associated workout exercises |

**POST /workouts — example request body:**
```json
{
  "date": "2024-03-01",
  "duration_minutes": 45,
  "notes": "Morning session"
}
```

---

### Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get a single exercise and all workouts it appears in |
| POST | `/exercises` | Create a new exercise |
| DELETE | `/exercises/<id>` | Delete an exercise and its associated workout exercises |

**POST /exercises — example request body:**
```json
{
  "name": "Push Up",
  "category": "strength",
  "equipment_needed": false
}
```

---

### Workout Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with sets, reps, or duration |

**POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises — example request body:**
```json
{
  "sets": 3,
  "reps": 12,
  "duration_seconds": null
}
```

---

## Validations

**Table Constraints:**
- `Exercise.name` — required and unique
- `Exercise.category` — required
- `Workout.date` — required
- `Workout.duration_minutes` — required
- `WorkoutExercise.workout_id` — required foreign key
- `WorkoutExercise.exercise_id` — required foreign key

**Model Validations:**
- Exercise name must be at least 2 characters
- Exercise category must be one of: strength, cardio, flexibility, balance
- Workout duration must be greater than 0
- WorkoutExercise sets must be greater than 0 if provided
- WorkoutExercise reps must be greater than 0 if provided

**Schema Validations:**
- Exercise name minimum length of 2
- Exercise category must match allowed values
- Workout duration minimum value of 1
- WorkoutExercise reps, sets, duration_seconds minimum value of 1 each