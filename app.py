import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="The Secret Mystery Challenge", page_icon="🎁", layout="centered")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 8px 24px;
    }
    .big-announcement {
        font-size: 32px;
        font-weight: bold;
        color: #ff4b4b;
        text-align: center;
        border: 3px dashed #ff4b4b;
        padding: 20px;
        border-radius: 15px;
        background-color: #fff5f5;
    }
    </style>
""", unsafe_allow_html=True)

# --- GAME QUESTIONS SETUP ---
# Customize these questions/answers to fit your story!
QUESTIONS = [
    {
        "q": "Question 1: Where did we have our very first date?",
        "ans": ["starbucks", "coffee", "park"], # Case-insensitive accepted answers
        "hint": "Think back to where it all began!"
    },
    {
        "q": "Question 2: What is 1 + 1?",
        "ans": ["2", "two"],
        "hint": "Simple math... or is it?"
    },
    {
        "q": "Question 3: What room in the house is known for having an 'Oven'?",
        "ans": ["kitchen"],
        "hint": "Where you cook dinner!"
    },
    {
        "q": "Question 4: What is something small, round, and takes roughly 9 months to complete?",
        "ans": ["bun", "pastry", "baby"],
        "hint": "Think of the famous saying..."
    },
    {
        "q": "Question 5: What comes next in this sequence? Seed -> Sprout -> Plant -> ______",
        "ans": ["fruit", "flower", "growth", "bloom"],
        "hint": "Something growing!"
    },
    {
        "q": "Question 6: What footwear is tiny, soft, and usually sold in pairs for tiny feet?",
        "ans": ["booties", "socks", "shoes", "baby shoes"],
        "hint": "Too small for an adult..."
    },
    {
        "q": "Question 7: What do you call someone who is about to get the ultimate 'PROMOTION' in a family?",
        "ans": ["parent", "dad", "mom", "grandma", "grandpa"],
        "hint": "Mom, Dad, Grandma, or Grandpa..."
    },
    {
        "q": "Question 8 (FINAL): Combine the clues: Oven + 9 Months + Tiny Shoes + Promotion = ?",
        "ans": ["baby", "a baby", "pregnant", "we are pregnant", "we are having a baby"],
        "hint": "Type 'BABY' to crack the final code!"
    }
]

# --- INITIALIZE APP STATE ---
if "step" not in st.session_state:
    st.session_state.step = 0

# --- GUI HEADER ---
st.title("🧩 The Secret Clue Challenge")
st.write("Solve all 8 riddles to unlock the secret message at the end!")
st.write("---")

current_step = st.session_state.step

# --- GAME LOGIC ---
if current_step < len(QUESTIONS):
    # Progress Bar
    progress = (current_step) / len(QUESTIONS)
    st.progress(progress)
    st.caption(f"Progress: Level {current_step + 1} of {len(QUESTIONS)}")

    # Display Current Question
    q_data = QUESTIONS[current_step]
    st.subheader(q_data["q"])
    
    # User Input
    user_ans = st.text_input("Enter your answer here:", key=f"ans_{current_step}").strip().lower()
    
    if st.button("Submit Answer"):
        if any(accepted in user_ans for accepted in q_data["ans"]):
            st.success("Correct! Unlocking the next level...")
            st.session_state.step += 1
            st.rerun()
        else:
            st.error(f"Not quite right! Hint: {q_data['hint']}")

# --- FINAL REVEAL SCREEN ---
else:
    st.progress(1.0)
    st.balloons() # Triggers on-screen confetti celebration!
    
    st.markdown("""
        <div class="big-announcement">
            🎉 SURPRISE! WE ARE HAVING A BABY! 👶<br><br>
            <span style="font-size: 20px; color: #333;">
                Expected Arrival: [Insert Due Date Here]
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    # Optionally display ultrasound photo if placed in the same folder:
    # st.image("ultrasound.jpg", caption="Our First Photo!", use_container_width=True)
    
    if st.button("Play Again"):
        st.session_state.step = 0
        st.rerun()