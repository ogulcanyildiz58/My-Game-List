# My Game List 🎮

A simple, lightweight web application built with Python and Flask to manage and track your video game collection. Users can register, log in securely, and organize their games into structured lists based on their playing status.

## Features
* **User Authentication:** Secure user registration and login system using SQLite and hashed passwords.
* **Game Management (CRUD):** * Add games to your collection.
  * List games dynamically by status (**Played** or **Wishlist**).
  * Update a game's status from Wishlist to Played with a single click.
  * Rate played games on a scale of 1-5.
  * Delete games completely from your lists.
* **Modern Interface:** Clean, user-friendly Dark Mode interface built entirely with semantic HTML and CSS.

## Project Structure
```text
My-Game-List/
├── static/
│   └── style.css          # Dark mode styling and layouts
├── templates/
│   ├── login.html         # Authentication interface
│   └── home.html          # User dashboard and game lists
├── tests/
│   └── test_app.py        # Automated unit tests for application routes
├── app.py                 # Main application controller and routes
├── database.py            # Database connection logic              
├── schema.sql             # Database schema initialization
└── database.db            # Local SQLite database file
