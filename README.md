# Freelance Marketplace Backend

This repository contains the backend for a freelance marketplace platform designed to connect clients with professionals in a secure and reliable environment.

**Note:** This is a functional but incomplete application. It is currently under active development.

## Project Description

The core idea behind this project is to create a freelance marketplace that prioritizes user trust and safety. To combat spam and scams prevalent on other platforms, this marketplace requires mandatory ID verification for all users. This ensures that all interactions are between verified individuals, fostering a community built on trust.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   Docker
*   Docker Compose

### Installation

1.  Clone the repo
    ```sh
    git clone https://github.com/your_username_/your_project_name.git
    ```
2.  Create a `.env` file in the root of the project and add the following environment variables:
    ```
    SECRET_KEY=your_secret_key
    DEBUG=True
    MYSQL_DATABASE=your_db_name
    MYSQL_USER=your_db_user
    MYSQL_PASSWORD=your_db_password
    MYSQL_ROOT_PASSWORD=your_db_root_password
    ```
3.  Build and run the Docker containers:
    ```sh
    docker-compose up --build
    ```

## Management Commands

This project includes several custom management commands to help with development and testing.

*   `load_mock_data`: Loads mock data from the `mock_data.json` file into the database.
*   `delete_mock_data`: Deletes all mock data from the database.
*   `reset_and_reload_data`: Deletes all mock data and reloads it from the `mock_data.json` file.

To run a management command, open a shell in the `django` container and run the following:

```sh
docker-compose exec django /bin/sh
python binaryblade24/manage.py your_command_name
```

## Live API

The API is hosted on Render and can be accessed at the following URL:

- [https://binaryblade24-api.onrender.com](https://binaryblade24-api.onrender.com)

## API Endpoints

For a detailed description of all the API endpoints available in this application, please see the [API_ENDPOINTS.md](API_ENDPOINTS.md) file.

## Profiles and computed fields

The `Profile` model exposes several computed/read-only fields that are surfaced via the API (available under the `profile` key when fetching `/api/users/{id}/profile/` or nested inside the `UserSerializer`):

- `completed_projects` - array of the user's completed projects (minimal info: id, title, thumbnail, status).
- `portfolio` - list of thumbnail URLs from completed projects.
- `active_projects` - array of active projects (in-progress projects).
- `projects_posted` - integer count of projects the user has posted.
- `avg_rating` - aggregated average rating from Review records (falls back to `profile.rating` if set).

These fields are read-only and are computed on-demand by the serializer; they do not require database schema changes or migrations.

## Scripts

The `binaryblade24/scripts/` directory includes helper scripts used during development to create users, profiles, projects, proposals, and reviews programmatically. Important notes:

- Scripts use SimpleJWT tokens returned by `/api/auth/login/`; they look for the `access` token and use it as `Authorization: Bearer <access>`.
- `post_complete_mock_data.py` is intended for development use and will make many requests to the API; use with caution on production.


## Technologies Used

*   Python
*   Django
*   Django REST Framework
*   Docker