# Job Tracker API

A Flask REST API to manage and track job applications with session-based authentication and SQLite storage.

## What I Learned

Through this project I practiced:

- Building a REST API with Flask
- Structuring routes using Flask Blueprints
- Using SQLite for persistent data storage
- Creating session-based authentication
- Using password hashing and login validation
- Protecting routes with custom decorators
- Building CRUD endpoints
- Writing SQL queries with filters and sorting
- Validating request data and status values
- Managing environment variables
- Refactoring reusable helper functions
- Organizing a backend project structure

## Features

- User registration and login
- Password hashing
- Session-based authentication
- Protected routes
- Create, read, update and delete job applications
- Filter applications by status and company
- Sort applications
- Application summaries by status
- SQLite database
- Environment variable configuration

## Technologies Used

- Python
- Flask
- SQLite
- python-dotenv

## How to Run

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
```

Run the app:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## API Endpoints

### Authentication

#### Register

```text
POST /register
```

Example body:

```json
{
  "username": "ferggz",
  "password": "1234"
}
```

#### Login

```text
POST /login
```

Example body:

```json
{
  "username": "ferggz",
  "password": "1234"
}
```

#### Logout

```text
POST /logout
```

### Applications

#### Get all applications

```text
GET /applications
```

#### Get one application

```text
GET /applications/<id>
```

#### Create application

```text
POST /applications
```

Example body:

```json
{
  "company": "Google",
  "position": "Backend Engineer",
  "status": "applied"
}
```

#### Update application

```text
PUT /applications/<id>
```

#### Delete application

```text
DELETE /applications/<id>
```

#### Get applications summary

```text
GET /applications/summary
```