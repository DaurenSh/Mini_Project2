/auth/jwt/create/ при логине в html токен в локал сторедж

/auth/login/

auth/register/

POST /auth/users/ - Register a new user.

POST /auth/jwt/create/ - Obtain JWT for authentication.

POST /auth/jwt/refresh/ - Refresh JWT.

POST /auth/jwt/verify/ - Verify JWT.

POST /auth/assign-role/{user_id}/{role_id}/ - Assign a role to a user (Admin only).

{
    "username": "admin",
    "password": 1234
}

GET /courses/

GET /courses/{id}/

GET /attendance/

GET /attendance/{id}/

GET/grades/

GET/grades/{id}/

GET/students/
