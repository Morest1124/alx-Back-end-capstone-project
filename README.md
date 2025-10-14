# Freelance Marketplace Backend

This repository contains the backend for a freelance marketplace platform designed to connect clients with professionals in a secure and reliable environment.

## Project Description

The core idea behind this project is to create a freelance marketplace that prioritizes user trust and safety. To combat spam and scams prevalent on other platforms, this marketplace requires mandatory ID verification for all users. This ensures that all interactions are between verified individuals, fostering a community built on trust.

## Key Features

*   **User Authentication**: Secure user registration and login using JSON Web Tokens (JWT).
*   **User Roles**: Distinct roles for "Client" and "Freelancer" with different permissions.
*   **ID Verification**: A mandatory identity verification process for all users.
*   **Project Management**: Clients can create, update, and delete project listings.
*   **Proposal System**: Freelancers can submit proposals (bids) for projects.
*   **Review System**: Clients and freelancers can rate and review each other after a project is completed.
*   **Messaging**: A messaging system for communication between users.
*   **Dashboards**: API endpoints for freelancer and client dashboards to view key metrics.

## Project Plan & Progress

The project is being developed following a five-week plan.

*   **[x] Week 1: The Vision**: Conceptualized the project idea and defined the core value proposition of a trust-based freelance platform.
*   **[x] Week 2: The Blueprint**: Designed the Django app structure, database schema, and API endpoints.
*   **[x] Week 3: Building the Foundation**:
    *   Set up the Django project and created the `users`, `projects`, and `reviews` apps.
    *   Implemented the custom `User` and `Profile` models.
    *   Built the JWT-based authentication system with endpoints for registration and login.
    *   Created CRUD operations for user profiles.
*   **[x] Week 4: The Core Functionality**:
    *   Implement project management features (create, retrieve, update, delete projects).
    *   Build the proposal system for freelancers to bid on projects.
    *   Implement a permissions system to restrict actions based on user roles.
    *   Implemented Dashboard APIs.
*   **[x] Week 5: Finishing Touches and Launch**:
    *   Implemented the messaging system.
    *   Implement the review system.
    *   Write comprehensive tests for the entire application.
    *   Prepare the project for deployment.

## API Endpoints

The following table outlines the RESTful API endpoints for the platform.

| Entity         | Method | Endpoint                               | Description                                                      |
| -------------- | ------ | -------------------------------------- | ---------------------------------------------------------------- |
| **Authentication** | POST   | `/auth/register`                       | Creates a new user (Freelancer or Client).                       |
|                | POST   | `/auth/login`                          | Authenticates a user and returns a token.                        |
| **User**           | GET    | `/users/{id}`                          | Retrieves a specific user's public profile.                      |
|                | PUT    | `/users/{id}`                          | Updates the authenticated user's details.                        |
| **User Profile**   | GET    | `/users/{id}/profile`                  | Retrieves the detailed profile for a user.                       |
|                | PUT    | `/users/{id}/profile`                  | Creates or updates the detailed profile for the authenticated user.|
| **Project**        | GET    | `/projects`                            | Retrieves a list of all open projects.                           |
|                | GET    | `/projects/{id}`                       | Retrieves a specific project's details.                          |
|                | POST   | `/projects`                            | Creates a new project (Client only).                             |
|                | PUT    | `/projects/{id}`                       | Updates an existing project (Client only).                       |
|                | DELETE | `/projects/{id}`                       | Deletes a project (Client only).                                 |
| **Proposal**       | GET    | `/projects/{project_id}/proposals`     | Retrieves all proposals for a specific project.                  |
|                | GET    | `/proposals/{id}`                      | Retrieves a specific proposal's details.                         |
|                | POST   | `/projects/{project_id}/proposals`     | Submits a new proposal to a project (Freelancer only).           |
|                | PUT    | `/proposals/{id}/status`               | Client accepts or rejects a proposal.                            |
|                | GET    | `/users/{id}/proposals`                | Retrieves all proposals submitted by a specific freelancer.      |
| **Review**         | POST   | `/projects/{project_id}/reviews`       | Client submits a review/rating for a freelancer.                 |
|                | GET    | `/users/{id}/reviews`                  | Retrieves all reviews received by a user.                        |
| **Comment**        | POST   | `/projects/{project_id}/comments`      | Adds a comment to a specific project.                            |
|                | GET    | `/projects/{project_id}/comments`      | Retrieves all comments for a specific project.                   |
| **Dashboard**      | GET    | `/api/dashboard/freelancer/`           | Retrieves metrics for the freelancer dashboard.                  |
|                | GET    | `/api/dashboard/client/`               | Retrieves metrics for the client dashboard.                      |
| **Message**        | GET    | `/api/messages/`                       | Retrieves the user's inbox.                                      |
|                | GET    | `/api/messages/sent/`                  | Retrieves the user's sent messages.                              |
|                | GET    | `/api/messages/{id}/`                  | Retrieves a single message and marks it as read.                 |
|                | POST   | `/api/messages/send/`                  | Sends a new message.                                             |

## Technologies Used

*   Python
*   Django
*   Django REST Framework
