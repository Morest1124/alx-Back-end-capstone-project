# API Endpoints

The base URL for the live API is: **https://binaryblade24-api.onrender.com**

The following table outlines the RESTful API endpoints for the platform.

| Entity         | Method | Endpoint                               | Description                                                      |
| -------------- | ------ | -------------------------------------- | ---------------------------------------------------------------- |
| **Authentication** | POST   | `/api/auth/register/`                  | Creates a new user (Freelancer or Client).                       |
|                | POST   | `/api/auth/login/`                     | Authenticates a user and returns a token.                        |
| **User**           | GET    | `/api/users/{id}/`                     | Retrieves a specific user's public profile.                      |
|                | PUT    | `/api/users/{id}/`                     | Updates the authenticated user's details.                        |
| **User Profile**   | GET    | `/api/users/{id}/profile/`             | Retrieves the detailed profile for a user.                       |
|                | PUT    | `/api/users/{id}/profile/`             | Creates or updates the detailed profile for the authenticated user.|
| **Project**        | GET    | `/api/projects/`                       | Retrieves a list of all open projects.                           |
|                | GET    | `/api/projects/{id}/`                  | Retrieves a specific project's details.                          |
|                | POST   | `/api/projects/`                       | Creates a new project (Client only).                             |
|                | PUT    | `/api/projects/{id}/`                  | Updates an existing project (Client only).                       |
|                | DELETE | `/api/projects/{id}/`                  | Deletes a project (Client only).                                 |
| **Proposal**       | GET    | `/api/projects/{project_id}/proposals/`| Retrieves all proposals for a specific project.                  |
|                | GET    | `/api/proposals/{id}/`                 | Retrieves a specific proposal's details.                         |
|                | POST   | `/api/projects/{project_id}/proposals/`| Submits a new proposal to a project (Freelancer only).           |
|                | PUT    | `/api/proposals/{id}/status/`          | Client accepts or rejects a proposal.                            |
|                | GET    | `/api/users/{id}/proposals/`           | Retrieves all proposals submitted by a specific freelancer.      |
| **Review**         | POST   | `/api/projects/{project_id}/reviews/`  | Client submits a review/rating for a freelancer.                 |
|                | GET    | `/api/users/{id}/reviews/`             | Retrieves all reviews received by a user.                        |
| **Comment**        | POST   | `/api/projects/{project_id}/comments/` | Adds a comment to a specific project.                            |
|                | GET    | `/api/projects/{project_id}/comments/` | Retrieves all comments for a specific project.                   |
| **Dashboard**      | GET    | `/api/dashboard/freelancer/`           | Retrieves metrics for the freelancer dashboard.                  |
|                | GET    | `/api/dashboard/client/`               | Retrieves metrics for the client dashboard.                      |
| **Message**        | GET    | `/api/messages/`                       | Retrieves the user's inbox.                                      |
|                | GET    | `/api/messages/sent/`                  | Retrieves the user's sent messages.                              |
|                | GET    | `/api/messages/{id}/`                  | Retrieves a single message and marks it as read.                 |
|                | POST   | `/api/messages/send/`                  | Sends a new message.                                             |
