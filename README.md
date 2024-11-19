# Basketball App

This is a Django-based application designed to help unprivileged basketball players showcase their talents and access better opportunities. The app provides APIs for managing players and opportunities, along with a frontend interface for easy interaction.

---

## Features

- **Player Management**: Add, view, and manage players.
- **Opportunities**: Track and add basketball-related opportunities.
- **API Endpoints**:
  - `GET /api/players/`: List all players.
  - `POST /api/players/`: Add a new player.
  - `GET /api/opportunities/`: List all opportunities.
  - `POST /api/opportunities/`: Add a new opportunity.

---

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS
- **Deployment**: Gunicorn, Nginx, Load Balancer
- **Database**: SQLite (can be replaced with PostgreSQL)

---

## Local Setup

Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/dahamkakooza/basketball_app.git
   cd basketball_app
