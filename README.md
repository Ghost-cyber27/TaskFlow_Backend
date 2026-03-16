Task Management API (FastAPI)

A scalable and high-performance backend API for a Task Management Mobile Application built with FastAPI. The API provides authentication, task management, and user management features designed to support modern mobile applications.

> Features

* User authentication (JWT based)
* Create, update, delete, and view tasks
* Task status tracking
* Secure API endpoints
* Rate limiting support
* CORS enabled for mobile clients
* Async support for high performance
* PostgreSQL database integration

> Tech Stack

* Backend Framework: FastAPI
* Database: PostgreSQL
* Cache / Rate Limiting: SlowApi
* ORM: SQLAlchemy
* Authentication: JWT Tokens
* Server: Uvicorn

> Project Structure

=> backend/
    > app/
      > routers/
        > auth.py
        > task.py
        > users.py
      > database.py
      > main.py
      > models.py
      > oauth.py
      > schemas.py
      > utils.py
      > README.md
      > requirements.txt


> Installation

1. Clone the repository


-> git clone https://github.com/yourusername/task-manager-api.git

-> cd task-manager-api

2. Create a virtual environment

-> python -m venv venv

Activate the environment

Linux / Mac:

-> source venv/bin/activate

Windows:

-> venv\Scripts\activate

3. Install dependencies

-> pip install -r requirements.txt

Environment Variables

Create a `.env` file in the root directory.

Example:

DATABASE_URL=postgresql://user:password@localhost:5432/taskdb
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60

Running the Server

Start the development server with:

-> uvicorn app.main:app --reload

Server will start at:

http://127.0.0.1:8000

> API Endpoints

=> Authentication

| Method | Endpoint         | Description       |
| ------ | ---------------- | ----------------- |
| POST   | `/auth/signup`   | Register new user 
| POST   | `/auth/login`    | Login user        
| POST   | `/auth/refresh`  | Refreshes access token 
| GET    | `/auth/me`       | Retrieves user data        
| POST   | `/auth/forgot-password`| Create an OTP
| POST   | `/auth/reset-password`  | Reset the user's password

=> Tasks

| Method | Endpoint           | Description       |
| ------ | ------------------ | ----------------- |
| GET    | `/tasks/me`        | Get all tasks relating the user     
| POST   | `/tasks`           | Create task       
| GET    | `/tasks/{task_id}` | Get specific task 
| PUT    | `/tasks/{task_id}` | Update task       
| DELETE | `/tasks/{task_id}` | Delete task       

=> User

| Method | Endpoint           | Description       |
| ------ | ------------------ | ----------------- |
| GET    | `/users`           | Get all users     |
| POST   | `/users`           | Create user       |
| GET    | `/users/{user_id}` | Get specific user |
| DELETE | `/users/{user_id}` | Delete user       |

=> Example Task Object

```json
{
  "id": 1,
  "title": "Finish mobile app UI",
  "description": "Complete task management UI",
  "status": "pending",
  "created_at": "2026-03-10T12:00:00"
}
```

> Security

* JWT Authentication
* Password hashing
* Rate limiting
* Input validation with Pydantic

> Deployment

You can deploy the API using:

* Railway
* Render
* DigitalOcean
* Docker containers

Example production run:

-> uvicorn app.main:app --host 0.0.0.0 --port 8000

## License

This project is licensed under the MIT License.
what is MIT License