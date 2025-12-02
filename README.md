## Tic Tac Toe – Full‑Stack App with Gen AI Opponent

This repository contains a **full‑stack Tic Tac Toe application**:

- **Backend**: FastAPI + MongoDB (Beanie ODM), AI service (Google Gemini).
- **Frontend**: React TypeScript + Vite, Redux Toolkit + RTK Query.

The AI plays as one of the players and uses a Gen AI model (Gemini) to suggest moves, which are then validated on the backend.

Full Design & Documentation here: [👉🏼 TicTacToe Design](https://docs.google.com/document/d/1plBt65QlLYHsZwre_-W8Gcip-vBukbO7hpHlLCRDtuQ/edit?usp=sharing)

---

## 1. Setup Instructions

### 1.1. Clone the repository

```bash
git clone https://github.com/TomerChermesh/tictactoe.git
cd tictactoe
```
---

### 1.2. Backend setup

**Requirements:**
- **Python 3.10 or higher** (tested with Python 3.11.3)
  - The codebase uses union types with `|` syntax (e.g., `int | None`), which requires Python 3.10+.
  - Verify your Python version: `python3 --version`

#### 1.2.1. Create & activate virtualenv

From the `backend/` directory:

```bash
cd backend
python3 -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### 2.2.2. Install backend dependencies

```bash
pip install -r requirements.txt
```

#### 1.2.3. Environment variables (backend)

The backend uses a `.env` file (loaded via `src/config.py`).  
There are **two kinds** of environment variables:

- **Non‑secret vars** – have sensible defaults in code.
- **Secrets** – **not** stored in git; You can use your own or reach me out.

Create a `.env` file in `backend/` (alongside `app.py`), for example:

```env
# Mongo
MONGO_URI=<MONGODB_CONNECTION_STRING>
MONGO_DB_NAME=tictactoe

# JWT
JWT_SECRET_KEY=<JWT_SECRET_KEY>
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=60

# GenAI
GEMINI_API_KEY=<GEMINI_API_KEY>
```

Notes:

The **real `GEMINI_API_KEY`, `MONGODB_CONNECTION_STRING` and `JWT_SECRET_KEY` are not committed**; You can use your own or reach me out.

#### 1.2.4. Run the backend

From `backend/` with venv activated:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- `http://localhost:8000/api/...`

---

### 1.3. Frontend setup

From the project root:

```bash
cd frontend
npm install
```

#### 1.3.1. Frontend environment variables

The frontend has a **default API URL** (`http://localhost:8000/api`) in case you did not created an `.env` file

***No secrets are currently used in the frontend.**

If you need to override the API URL (e.g., for a different backend port or remote server), create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:<PORT>/api
```

#### 1.3.2. Run the frontend

From `frontend/`:

```bash
npm run dev
```

By default Vite runs at:

- `http://localhost:5173`

---

### 1.4. Launch the website

**Open in your default browser**: 
   - **On GitHub/GitLab**: [👉🏼 Launch Application](http://localhost:5173).
   - **In IDE**: Copy `http://localhost:5173` and paste it into your browser.

Login / register, create a matchup, and start playing against a friend or the AI.

---

## 2. Gen AI Integration (Gemini)

### 2.1. Board & state representation in the prompt

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

### 2.2. Expected structured response

Although Gemini is a free‑form model, we **constrain its response**:

- We ask it to return **only an integer index between 0 and 8**, with no surrounding text.
- In practice, the backend:
  - Validate the response.
  - Then Validates that:
    - It’s in the range `[0, 8]`.
    - The cell is actually empty on the board (`board[index] == 0`).

### 2.3. Validation & applying the model suggestion

Flow:

1. `GameService.ai_move(game_id, ai_player_id)`:
   - Loads the game from DB.
   - Derives `opponent_player_id`.
   - Calls `AIService.get_next_move(board, ai_player_id, opponent_player_id)`.

2. `AIService.get_next_move(...)`:
   - Builds the full prompt with rules + board state.
   - Sends request to Gemini via `google.genai`.
   - Parses & Validate the response
   - Returns the chosen `cell_index` or raises `AIServiceError`.

3. Back in `GameService.ai_move(...)`:
   - Calls `player_move(game_id, ai_player_id, ai_cell_index)` which is the same for any kind of a player move

The frontend receives the updated `Game` and `Matchup` and updates Redux accordingly.

### 2.4. Handling unexpected responses

Unexpected AI responses are handled defensively in `AIService`:

- Empty response → `AIServiceError('AI returned an empty response.')`.
- Bad Response → `AIServiceError('AI returned a bad structured response: ...')`.
- Out‑of‑range index → `AIServiceError('AI returned an out-of-range cell index: ...')`.
- Index points to a non‑empty cell → `AIServiceError('AI selected an invalid or occupied cell index: ...')`.

In any of those cases, the `GameService` is responsible to return the first empty cell.
