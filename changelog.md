# Changelog - Week of October 12, 2025

This document summarizes the major changes and improvements made to the freelance marketplace platform this week.

## New Features

*   **User Profile Enhancements**
    *   **Profile Pictures**: Users can now upload their own profile pictures. A new `profile_picture` field has been added to the `User` model, and the necessary configuration for handling image uploads has been implemented.
    *   **Freelancer Details**: The `Profile` model has been enhanced with `hourly_rate` and `availability` fields, allowing freelancers to provide more information to potential clients.

*   **New API Endpoint**
    *   A new endpoint at `/api/proposals/` has been created to retrieve a list of all proposals in the system.

## API and Endpoint Updates

*   The `endpoint.txt` file has been updated to include the new `/api/proposals/` endpoint and to provide more detailed and accurate information about all the existing endpoints.

## Core Functionality

*   A significant portion of the core functionality for project and proposal management has been implemented and tested.
*   Several bugs in the user registration and authentication system have been fixed, improving the overall stability of the platform.

## Technology and Configuration

*   **Database**: The development database has been switched from MySQL to SQLite for easier setup and development.
*   **Dependencies**:
    *   The `Pillow` library has been added to the project to handle image processing for the new profile picture feature.
    *   The unused `mysqlclient` dependency has been removed.
*   **Media Files**: The project has been configured to handle user-uploaded media files, which are now stored in the `media` directory.

## Development and Testing

*   **Mock Data**: Scripts have been created to bulk-create mock users, projects, and proposals. This will help to speed up development and testing by providing a realistic dataset.
*   **Error Handling**: The bulk creation scripts have been improved with better error handling to make them more robust and easier to debug.
