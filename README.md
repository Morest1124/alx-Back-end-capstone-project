# Freelance Marketplace Backend

This repository contains the backend for a freelance marketplace platform designed to connect clients with professionals in a secure and reliable environment.

**Note:** This is a functional but incomplete application. It is currently under active development.

## Project Description

The core idea behind this project is to create a freelance marketplace that prioritizes user trust and safety. To combat spam and scams prevalent on other platforms, this marketplace requires mandatory ID verification for all users. This ensures that all interactions are between verified individuals, fostering a community built on trust.

## Table of Contents

- [Project Status](#project-status)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Management Commands](#management-commands)
- [Live API](#live-api)
- [API Endpoints](#api-endpoints)
- [Profiles and Computed Fields](#profiles-and-computed-fields)
- [Scripts](#scripts)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Status

This project is currently under active development. New features are being added regularly, and improvements are continuously being made.

## Features

- **User Authentication:** Secure registration and login for both freelancers and clients.
- **User Profiles:** Detailed profiles for users, including computed fields like completed projects, portfolio, active projects, projects posted, and average rating.
- **Project Management:** Clients can create, update, and delete projects. Freelancers can view available projects.
- **Proposal System:** Freelancers can submit proposals to projects, and clients can accept or reject them.
- **Review and Rating System:** Clients can submit reviews and ratings for freelancers.
- **Messaging System:** Users can send and receive messages.
- **Dashboard:** Separate dashboards for freelancers and clients to view relevant metrics.
- **API Key Generation:** Users can generate API keys for programmatic access.
- **ID Verification:** Mandatory ID verification for all users to ensure trust and safety.

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
4.  Generate an API key (optional, but recommended for programmatic access):
    ```sh
    docker-compose exec django /bin/sh
    python binaryblade24/manage.py generate_api_key
    ```

## Management Commands

This project includes several custom management commands to help with development and testing.

*   `count_users`: Counts the total number of users in the database.
*   `create_missing_profiles`: Creates a profile for any user that does not have one.
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
*   MySQL

## Contributing

We welcome contributions to the Freelance Marketplace Backend! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and ensure they adhere to the project's coding standards.
4.  Write tests for your changes.
5.  Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Here is an example of how to register a user
{
    "username": "required_user4",
    "first_name": "Required4",
    "last_name": "Example3",
    "email": "required.example@test4.com",
    "password": "aStrongRequiredPassword!",
    "identity_number": "1122334455",
    "country_origin": "Germany",
    "roles": ["FREELANCER"]
}
