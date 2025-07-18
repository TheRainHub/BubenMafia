# Buben Mafia

**Buben Mafia** is a modern, closed‑source web application designed to support the full lifecycle of Mafia club events-from real‑time game facilitation to comprehensive historical analysis of played sessions.

---

## Table of Contents

1. [Key Features](#key-features)
2. [Architecture Overview](#architecture-overview)
3. [Technology Stack](#technology-stack)
4. [Installation & Local Development](#installation--local-development)
5. [Environment Configuration](#environment-configuration)
6. [Usage & Workflow](#usage--workflow)
7. [Directory Structure](#directory-structure)
8. [API Documentation](#api-documentation)
9. [Contributing Guidelines](#contributing-guidelines)

---

## Key Features

### Live Game Interface

* **Role Distribution**: Assign roles (Don, Mafia, Sheriff, Citizen, Casper) via modal dialog. Hidden until revealed by host.
* **Timed Speeches**: 30s or 60s countdown per player, with Pause/Resume controls and visual alert on timeout.
* **Nomination & Voting**: Interactive nomination list and numeric inputs to record vote counts per nominated player.
* **In‑Game Events**: Quick action buttons for “Killed”, “Voted Out”, “Foul”, or “Casper” removals. Automatic foul tracking with skip/punishment logic.
* **Bonus Points (“Extra Points”)**: Manual adjustments by host in 0.1‑point increments for special actions.
* **Auto‑save & Recovery**: All game events are persisted every 2 seconds; host can reconnect and resume at any point.
* **Game Completion & Abortion**: Finalize a game with score calculation or abort with reason; completed games are locked for editing (GM vs Organizer roles).

### Historical Statistics

* **Game Records**: Searchable, filterable table of all completed games (date, winner faction, number of players, host).
* **Player Profiles**: Total games, win rates (overall, as citizens vs mafia), cumulative points, point trend chart.
* **Club Dashboard**: Pie chart of faction win distribution, Top‑10 leaderboard by total points, date‑range selection.

### User & Access Management

* **Roles & Permissions**:

  * **Organizer**: Full system administration, rule configuration, audit logs, manage user roles.
  * **Game Master (GM)**: Create and run live games, quick‑add players, finalize/abort sessions.
  * **Player**: View personal stats and club dashboards; self‑registration with email confirmation or GM‑issued quick code.
  * **Guest**: Read‑only access to public statistics.
* **Authentication**: JWT‑based HttpOnly cookies managed via fastapi‑users.
* **Player Quick‑Add**: GM can register a temporary player by nickname; later linked via one‑time code during full signup.

---

## Architecture Overview

1. **Backend (FastAPI)**:

   * REST endpoints for games, players, events, statistics
   * Auto‑generated OpenAPI/Swagger UI
   * JWT HttpOnly authentication
   * PostgreSQL storage with SQLModel ORM and Alembic migrations

2. **Frontend (React + MUI + Tailwind CSS)**:

   * Vite bundler with TypeScript
   * MUI components for layout and interactive controls
   * Tailwind utilities for responsive styling
   * TanStack Query for data fetching and cache management

3. **DevOps & CI/CD**:

   * Dockerized backend and frontend services
   * Docker‑Compose for local orchestration
   * GitHub Actions for linting, testing, and building images
   * Deployment to Fly.io (staging and production) behind Traefik proxy
   * Sentry integration for error monitoring

---

## Technology Stack

| Layer                | Framework / Tool                |
|----------------------|---------------------------------|
| **Backend**          | FastAPI 1.1, Python 3.13        |
| **ORM & Migrations** | SQLModel, SQLAlchemy, Alembic   |
| **Database**         | PostgreSQL 15                   |
| **Authentication**   | fastapi‑users (JWT cookies)     |
| **Frontend**         | React 18, TypeScript, Vite      |
| **UI Libraries**     | MUI v7, TailwindCSS 4           |
| **State Management** | TanStack Query (react-query)    |
| **Containerization** | Docker, Docker‑Compose          |
| **CI/CD**            | GitHub Actions, Fly.io, Traefik |
| **Monitoring**       | Sentry                          |

---

## Installation & Local Development

1. **Clone the repository**

   ```bash
   git clone git@github.com:TheRainHub/BubenMafia.git
   cd BubenMafia
   ```

2. **Backend Setup**

   ```bash
   cd backend
   python3.13 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   alembic upgrade head
   ```

3. **Frontend Setup**

   ```bash
   cd ../frontend
   npm install
   ```

4. **Run services via Docker‑Compose**

   ```bash
   docker-compose up -d
   ```

5. **Start Development Servers**

   ```bash
   # Backend
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Frontend
   cd ../frontend
   npm run dev
   ```

6. **Access the application**

   * Backend API docs: `http://localhost:8000/docs` or `/redoc`
   * Frontend UI: `http://localhost:5173`

---

## Environment Configuration

Copy `.env.example` to `.env` in the `backend` folder and set values:

```ini
DATABASE_URL=postgresql://user:password@db:5432/mafia_db
FASTAPI_USERS_SECRET=supersecretkey
SENTRY_DSN=https://...@sentry.io/...   # optional
```

---

## Usage & Workflow

1. **Organizer** creates an initial admin user via CLI or database seed.
2. **Organizer** assigns GM roles to selected accounts.
3. **GM** initiates a new Game, quickly adds any unregistered players.
4. **GM** uses Live Interface to distribute roles and record nominations, votes, and events.
5. **Live game data** is auto‑saved in real time; GM may pause and resume as needed.
6. At the game end, **GM** clicks “Finish”, triggering score calculations and locking the session.
7. **Players** and **Guests** explore historical data in the Stats module at their leisure.

---

## Directory Structure

```
/backend
  ├─ app/
  │   ├─ main.py         # FastAPI application entry point
  │   ├─ models/        # SQLModel definitions
  │   ├─ api/           # routers and endpoints
  │   ├─ core/          # settings, dependencies, auth
  │   └─ alembic/       # migration scripts
  └─ requirements.txt

/frontend
  ├─ public/           # static assets
  ├─ src/
  │   ├─ components/   # reusable React components
  │   ├─ pages/        # route views
  │   ├─ hooks/        # custom React hooks
  │   └─ App.tsx       # root component
  └─ package.json

docker-compose.yml
.env.example
.gitignore
README.md
```

---

## API Documentation

All API routes are documented via OpenAPI. Visit:

* **Swagger UI**: `http://localhost:8000/docs`
* **ReDoc**: `http://localhost:8000/redoc`

---

## Contributing Guidelines

1. **Branching**: Create branches from `main` using `feature/<name>` or `bugfix/<name>`.
2. **Commits**: Use clear, imperative messages (e.g. `feat: add nomination endpoint`).
3. **Pull Requests**: Submit PRs against `main`; include description, linked issues, and screenshots if UI‑related.
4. **Code Reviews**: Assign reviewers, address comments, and await CI checks before merging.
5. **Testing**: Write unit and integration tests; aim for ≥ 80% coverage.

---

*This repository contains proprietary, closed‑source code. Unauthorized copying, modification, or distribution is prohibited.*
