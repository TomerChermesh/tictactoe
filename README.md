## Tic Tac Toe – Full‑Stack App with Gen AI Opponent

This repository contains a **full‑stack Tic Tac Toe application**:

- **Backend**: FastAPI + MongoDB (Beanie ODM), JWT auth, rate limiting, AI service (Google Gemini).
- **Frontend**: React + TypeScript + Vite, Material UI, Redux Toolkit + RTK Query.

The AI plays as one of the players and uses a Gen AI model (Gemini) to suggest moves, which are then validated on the backend.

---

## 1. Project Structure

- **`backend/`** – FastAPI service, data access, business logic, AI integration.
  - `app.py` – FastAPI app factory and server entrypoint.
  - `src/db.py` – MongoDB + Beanie initialization.
  - `src/models/` – Pydantic & Beanie models (`users`, `matchups`, `games`, `auth`, `responses`).
  - `src/dal/` – DAL (Data Access Layer) for users, games, matchups (`BaseDAL` generic).
  - `src/services/` – Domain logic (`GameService`, `AIService`).
  - `src/api/` – FastAPI routers (`auth`, `matchup`, `game`, `health`).
  - `src/security/` – JWT auth, password hashing.
  - `src/utils/` – helpers (`game`, `db`, `rate_limit`, `logger`, `files`).
  - `src/constants/` – global constants (FastAPI, game, AI, logger).
  - `logs/` – daily log files (`YYYY-MM-DD.log`) created at runtime.

- **`frontend/`** – React SPA.
  - `src/api/` – RTK Query API slices (`authApi`, `gameApi`, `matchupApi`, `baseQuery`).
  - `src/store/` – Redux store + slices (`authSlice`, `gameSlice`, `matchupSlice`).
  - `src/components/` – UI components (board, players panel, layout, alerts, etc.).
  - `src/pages/` – Pages (`LoginPage`, `HomePage`, `GamePage`, `MatchupsListPage`).
  - `src/types/` – Shared TS types (`auth`, `game`, `matchup`, `players`).

---

## 2. Setup Instructions

### 2.1. Clone the repository

```bash
git clone <REPO_URL> tictactoe
cd tictactoe
```

Replace `<REPO_URL>` with your Git remote URL.

---

### 2.2. Backend setup (FastAPI)

#### 2.2.1. Create & activate virtualenv

From the `backend/` directory:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# On Windows: venv\Scripts\activate
```

#### 2.2.2. Install backend dependencies

```bash
pip install -r requirements.txt
```

#### 2.2.3. Environment variables (backend)

The backend uses a `.env` file (loaded via `src/config.py`).  
There are **two kinds** of environment variables:

- **Non‑secret vars** – have sensible defaults in code.
- **Secrets** – **not** stored in git; values are provided in a separate Google Doc (as required).

Create a `.env` file in `backend/` (alongside `app.py`), for example:

```env
# Mongo
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=tictactoe

# JWT
JWT_SECRET_KEY=change_me_in_prod
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=60

# FastAPI / CORS
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Gen AI (secret – real value in the separate document)
GEMINI_API_KEY=YOUR_REAL_KEY_HERE
GEMINI_MODEL=gemini-1.5-pro
```

Notes:
- For **non‑secret** vars, defaults exist in `src/config.py` and `src/constants/*`.
- The **real `GEMINI_API_KEY` and other secrets are not committed**; they are documented in the dedicated Google Doc as requested.

#### 2.2.4. Run the backend

From `backend/` with venv activated:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- `http://localhost:8000/api/...`

---

### 2.3. Frontend setup (React + Vite)

From the project root:

```bash
cd frontend
npm install
```

#### 2.3.1. Frontend environment variables

Vite expects env vars in files like `.env`, `.env.development`, etc.  
The main variable is typically:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

- Non‑secret values like `VITE_API_BASE_URL` can be committed with defaults.
- Secrets (if any on the frontend) should **not** be committed and should use the same Google Doc / local override strategy.

Create `frontend/.env.development`:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

#### 2.3.2. Run the frontend

From `frontend/`:

```bash
npm run dev
```

By default Vite runs at:

- `http://localhost:5173`

---

### 2.4. Launch the website

1. **Start backend** (FastAPI, port 8000).
2. **Start frontend** (Vite dev server, port 5173).
3. Open: `http://localhost:5173` in your browser.

Login / register, create a matchup, and start playing against a friend or the AI.

---

## 3. Data Model & Architecture

### 3.1. Core entities

#### User (`UserDocument`)

- `id: ObjectId` – MongoDB ID.
- `email: string` – unique.
- `password: string` – hashed.
- `created_at: datetime`
- `updated_at: datetime`

#### Matchup (`MatchupDocument`)

Represents a *series* / session between two players.

- `id: ObjectId`
- `user_id: ObjectId` – owner (the logged‑in user).
- `mode: 'friend' | 'ai'`
- `player1_name: string`
- `player1_score: int`
- `player2_name: string`
- `player2_score: int`
- `created_at: datetime`
- `updated_at: datetime`

On the frontend this is mapped to:

- `Matchup` with nested `player1` & `player2` objects:
  - `player: { id: 1 | 2, name: string, score: number }`

#### Game (`GameDocument`)

Represents a *single Tic Tac Toe game* under a matchup.

- `id: ObjectId`
- `matchup_id: ObjectId`
- `board: List[0 | 1 | 2]` – 9 cells, 0 = empty, 1 = X, 2 = O.
- `current_turn: 1 | 2`
- `winner: 1 | 2 | null`
- `winning_triplet: List[int] | null` – indexes of winning cells.
- `is_finished: bool`
- `created_at: datetime`
- `updated_at: datetime`

On the frontend this is mapped to:

- `Game` with:
  - `board: CellValue[]` (0 | 1 | 2)
  - `currentTurn`, `winner`, `winningTriplet`, etc.

### 3.2. Backend architecture

- **API layer (`src/api/*`)**
  - `auth.py` – register/login/logout (JWT), uses `UsersDAL`.
  - `matchup.py` – create/list/get/update matchups.
  - `game.py` – create new game, player move, AI move, get last game for matchup.
  - Uses FastAPI dependencies for auth (`get_current_user`), DALs, and `GameService`.

- **Service layer (`src/services/game.py`, `src/services/ai.py`)**
  - `GameService` encapsulates all game logic:
    - Creates matchups & games.
    - Validates moves.
    - Checks wins / draws.
    - Updates scores in `MatchupsDAL`.
    - Coordinates with `AIService` for AI moves.
  - `AIService` encapsulates Gen AI calls to Gemini.

- **DAL layer (`src/dal/*`)**
  - `BaseDAL` – generic helper for Beanie Documents (handles `created_at`, `updated_at`, updates).
  - `UsersDAL`, `MatchupsDAL`, `GamesDAL` – CRUD and specific operations (e.g. `increase_player_score_by_one`).

- **Security**
  - `src/security/auth.py` – JWT token creation & validation, `get_current_user`.
  - `src/security/password.py` – hashing & verifying passwords.

- **Cross‑cutting**
  - `src/utils/rate_limit.py` – in‑memory rate limiting per IP+path (3 req/sec by default, configurable).
  - `src/utils/logger.py` – unified logger (terminal + daily log files).
  - `src/utils/files.py` – safe file helpers.

### 3.3. Frontend architecture

- **RTK Query APIs**
  - `authApi` – login, register, logout.
  - `matchupApi` – create matchup, list, get, update player names.
  - `gameApi` – create new game, player move, last game for matchup.
  - All share `baseQueryWithReauth` which:
    - Adds `Authorization: Bearer <token>`.
    - Handles 401 → clears store and redirects to `/login`.
    - Enforces a global timeout with `AbortController`.

- **Redux slices**
  - `authSlice` – user, token, `isAuthenticated`, persisted in `localStorage`.
  - `matchupSlice` – current matchup, persisted.
  - `gameSlice` – current game, persisted.
  - Listener middleware to clear state on logout or 401.

- **Pages**
  - `LoginPage` – login/register.
  - `HomePage` – main menu (resume, new matchup, rules).
  - `GamePage` – board, players panel, game over status, AI “Thinking…” indicator.
  - `MatchupsListPage` – matchups overview using MUI DataGrid, including replay of last game.

---

## 4. Gen AI Integration (Gemini)

### 4.1. Board & state representation in the prompt

The board is represented as a **1D array of 9 integers**:

- `0` – empty cell.
- `1` – player X.
- `2` – player O.

The prompt includes:

- The raw board array, e.g. `[1, 0, 2, 0, 2, 0, 0, 0, 0]`.
- Which player is the AI (`ai_player_id`).
- Which player is the opponent.
- The list of winning lines (all possible 3‑in‑a‑row combinations).
- Rules:
  - Must choose an **empty cell** (value 0).
  - Prefer winning moves.
  - Otherwise block opponent’s winning moves.
  - Otherwise pick the best move for AI to win.
  - **Return only a single integer index (0–8), no text or code blocks.**

### 4.2. Expected structured response

Although Gemini is a free‑form model, we **constrain its response**:

- We ask it to return **only an integer index between 0 and 8**, with no surrounding text.
- In practice, the backend:
  - Parses the first integer found via regex `\d+`.
  - Validates that:
    - It’s in the range `[0, 8]`.
    - The cell is actually empty on the board (`board[index] == 0`).

### 4.3. Validation & applying the model suggestion

Flow:

1. `GameService.ai_move(game_id, ai_player_id)`:
   - Loads the game from DB.
   - Derives `opponent_player_id`.
   - Calls `AIService.get_next_move(board, ai_player_id, opponent_player_id)`.

2. `AIService.get_next_move(...)`:
   - Builds the full prompt with rules + board state.
   - Sends request to Gemini via `google.genai`.
   - Parses the response:
     - Extracts first integer.
     - Validates range and emptiness as described.
   - Returns the chosen `cell_index` or raises `AIServiceError`.

3. Back in `GameService.ai_move(...)`:
   - Calls `player_move(game_id, ai_player_id, ai_cell_index)` which:
     - Validates move (turn, occupancy).
     - Applies move.
     - Checks for winner / draw.
     - Updates DB (game + matchup scores).
     - Returns updated `UpdateResponse { matchup, game }`.

The frontend receives the updated `Game` and `Matchup` and updates Redux accordingly.

### 4.4. Handling unexpected responses

Unexpected AI responses are handled defensively in `AIService`:

- Empty response → `AIServiceError('AI returned an empty response.')`.
- No number found → `AIServiceError('AI returned a non-numeric response: ...')`.
- Out‑of‑range index → `AIServiceError('AI returned an out-of-range cell index: ...')`.
- Index points to a non‑empty cell → `AIServiceError('AI selected an invalid or occupied cell index: ...')`.
- API errors (`APIError`) and general exceptions → wrapped as `AIServiceError` with a clear message.

In `GameService.ai_move(...)`:

- `AIServiceError` is **caught and translated to** `InvalidMoveError` so that the API returns a clear 400 error with a helpful message.
- The frontend:
  - Shows the error in a `Snackbar` without crashing.
  - Does **not** retry indefinitely; AI is triggered in a controlled way after human moves as long as the game is not finished yet.

### 4.5. Secrets, security & environment configuration

- **Secrets (e.g. `GEMINI_API_KEY`)**
  - Never committed to git.
  - Documented in a dedicated Google Doc, as required.
  - Loaded from environment / `.env` via `src/config.py`.

- **JWT & auth**
  - `JWT_SECRET_KEY` stored in env, never hard‑coded in the repo.
  - Tokens are:
    - Issued on login/register.
    - Verified for each protected route via `get_current_user`.

- **Basic security considerations**
  - Rate limiting middleware (`rate_limiter`) to reduce abuse (3 req/sec per IP+path by default, configurable in `src/constants/fastapi.py`).
  - CORS is restricted to known origins (`VALID_ORIGINS` in `src/constants/fastapi.py`).
  - Passwords are hashed using `passlib` before storing in MongoDB.
  - Centralized `baseQueryWithReauth` on frontend:
    - Automatically attaches JWT.
    - On 401:
      - Clears auth + game + matchup state.
      - Redirects user to `/login`.

- **Logging**
  - Custom `Logger` writes:
    - To stdout (for local dev / container logs).
    - To daily log files: `backend/logs/YYYY-MM-DD.log`.
  - Errors from AI, DB, auth, etc. are logged with level `ERROR` or `CRITICAL` and include exception info.

---

## 5. How to Extend / Customize

- **Change rate limit** – update `RATE_LIMIT_MAX_REQUESTS` / `RATE_LIMIT_WINDOW_SECONDS` in `src/constants/fastapi.py`.
- **Change AI model or prompt** – edit `src/constants/ai.py` and `src/services/ai.py`.
- **Add new pages / stats** – extend `frontend/src/pages` and `frontend/src/api/*` to expose new backend endpoints.
- **Swap DB** – most logic goes through DALs; replacing Mongo/Beanie would mostly affect `src/db.py` and `src/dal/*`.
