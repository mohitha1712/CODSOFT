import streamlit as st
import time
from game import check_winner, is_full, get_best_move

st.set_page_config(page_title="Tic-Tac-Toe AI", layout="centered")

# 🎨 MODERN UI STYLING
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #1e1e2f, #0f2027);
}

.main {
    background: transparent;
}

.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: #00c6ff;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #aaa;
    margin-bottom: 30px;
}

div.stButton > button {
    width: 100%;
    height: 100px;
    font-size: 42px;
    font-weight: bold;
    border-radius: 15px;
    border: none;
    background: linear-gradient(145deg, #2a2a40, #1a1a2e);
    color: white;
    box-shadow: 0 0 10px rgba(0,198,255,0.2);
    transition: 0.2s;
}

div.stButton > button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 20px rgba(0,198,255,0.6);
}

.score-box {
    text-align: center;
    padding: 15px;
    border-radius: 15px;
    background: rgba(0,198,255,0.1);
    font-size: 20px;
    font-weight: bold;
    margin-top: 15px;
}

.status {
    text-align: center;
    font-size: 18px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# 🎮 TITLE
st.markdown('<div class="title">🎮 Tic-Tac-Toe AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Play against an unbeatable AI</div>', unsafe_allow_html=True)

# 🎛️ MODE
mode = st.sidebar.radio("Mode", ["Smart", "Unbeatable"])

# 🧠 SESSION STATE
if "board" not in st.session_state:
    st.session_state.board = [" "] * 9
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "turn" not in st.session_state:
    st.session_state.turn = "Player"
if "player_score" not in st.session_state:
    st.session_state.player_score = 0
if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0
if "draws" not in st.session_state:
    st.session_state.draws = 0
if "score_updated" not in st.session_state:
    st.session_state.score_updated = False

# 🎮 MOVE FUNCTION
def handle_click(i):
    if st.session_state.board[i] == " " and not st.session_state.game_over:

        # Player move
        st.session_state.board[i] = "X"
        st.session_state.turn = "AI"

        winner, _ = check_winner(st.session_state.board)
        if winner or is_full(st.session_state.board):
            st.session_state.game_over = True
            return

        # AI delay
        time.sleep(0.4)

        # AI move
        ai_move = get_best_move(st.session_state.board, mode)
        st.session_state.board[ai_move] = "O"
        st.session_state.turn = "Player"

        winner, _ = check_winner(st.session_state.board)
        if winner or is_full(st.session_state.board):
            st.session_state.game_over = True

# 🎮 GAME BOARD
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        i = row * 3 + col
        symbol = st.session_state.board[i]

        # Simple clean symbols
        if symbol == "X":
            display = "X"
        elif symbol == "O":
            display = "O"
        else:
            display = " "

        cols[col].button(display, key=i, on_click=handle_click, args=(i,))

# 📊 RESULT
winner, _ = check_winner(st.session_state.board)

# 🎯 STATUS DISPLAY
st.markdown("<div class='status'>", unsafe_allow_html=True)

if st.session_state.game_over and not st.session_state.score_updated:

    if winner == "X":
        st.success("🏆 You Win!")
        st.session_state.player_score += 1

    elif winner == "O":
        st.error("🤖 AI Wins!")
        st.session_state.ai_score += 1

    else:
        st.info("🤝 It's a Draw!")
        st.session_state.draws += 1

    st.session_state.score_updated = True

elif not st.session_state.game_over:
    if st.session_state.turn == "Player":
        st.info("👉 Your Turn")
    else:
        st.warning("🤖 AI Thinking...")

st.markdown("</div>", unsafe_allow_html=True)

# 🎮 CONTROLS
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 New Match"):
        st.session_state.board = [" "] * 9
        st.session_state.game_over = False
        st.session_state.turn = "Player"
        st.session_state.score_updated = False

with col2:
    if st.button("♻ Reset Score"):
        st.session_state.player_score = 0
        st.session_state.ai_score = 0
        st.session_state.draws = 0

# 📊 SCOREBOARD
st.markdown("### 📊 Scoreboard")

st.markdown(f"""
<div class="score-box">
Player: {st.session_state.player_score} |
AI: {st.session_state.ai_score} |
Draws: {st.session_state.draws}
</div>
""", unsafe_allow_html=True)
