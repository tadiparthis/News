import streamlit as st
import os
from PIL import Image, ImageFilter

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="The Family Mystery Challenge", page_icon="🎁", layout="centered")

# --- MULTIPLE CHOICE QUESTIONS SETUP ---
QUESTIONS = [
    {
        "q": "Question 1 (Bible): According to Psalm 127:3, children are a gift and a blessing from whom?",
        "options": ["The King", "The Lord / God", "The Neighbors", "The Mayor"],
        "correct": "The Lord / God",
        "hint": "They are a divine blessing from above!",
        "watermark": "Nibling"
    },
    {
        "q": "Question 2 (Math): In standard math, 1 + 1 = 2. But in family math, 1 + 1 = ?",
        "options": ["2", "3", "0", "10"],
        "correct": "3",
        "hint": "Two parents plus a new addition!",
        "watermark": "Mom"
    },
    {
        "q": "Question 3 (Physics): What high-frequency sound wave do doctors use to take the very first photo inside the womb?",
        "options": ["Micro-wave", "Radio wave", "Ultrasound", "Infrared"],
        "correct": "Ultrasound",
        "hint": "It starts with 'Ultra'!",
        "watermark": "Dad"
    },
    {
        "q": "Question 4 (Bible): Which famous baby in the Old Testament was saved in a basket floating on the Nile River?",
        "options": ["Moses", "David", "Solomon", "Noah"],
        "correct": "Moses",
        "hint": "He grew up to lead his people!",
        "watermark": "Nani"
    },
    {
        "q": "Question 5 (Physics/Math): What happens to matter when heat is added—does it contract or expand?",
        "options": ["Contract", "Expand", "Disappear", "Freeze"],
        "correct": "Expand",
        "hint": "Think about things growing bigger!",
        "watermark": "Nana"
    },
    {
        "q": "Question 6 (General): What tiny, soft footwear is usually sold in pairs for very small feet?",
        "options": ["Hiking Boots", "Baby Booties", "High Heels", "Flip Flops"],
        "correct": "Baby Booties",
        "hint": "Way too small for an adult!",
        "watermark": "Dadi"
    },
    {
        "q": "Question 7 (Family): What new title do parents get when a new generation arrives?",
        "options": ["Dada & Dadi / Nana & Nani", "Captain", "Professor", "Neighbor"],
        "correct": "Dada & Dadi / Nana & Nani",
        "hint": "The best promotion in the family!",
        "watermark": "Granddaughter"
    },
    {
        "q": "Question 8 (FINAL): Combine all clues: Ultrasound + 1+1=3 + Baby Booties + Grandparent Promotion = ?",
        "options": ["New Car", "Vacation", "WE ARE HAVING A BABY!", "Pet Cat"],
        "correct": "WE ARE HAVING A BABY!",
        "hint": "Choose the biggest news!",
        "watermark": "BABY IS COMING!"
    }
]

# GIF URLs
SUCCESS_GIF = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdW43ZGl6ZTh3OXBmbTdrZnkyN3p1czV3OWlqaTRjcXRiYnQzbGF0ayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/artj92V8o75VPL7AeQ/giphy.gif"
THINKING_GIF = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHBsZ3Uxa3lseGJnYThmb2QzeGs5YXdtYXRyNnBucnlwbHRmNzByYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7bu3XilJ5BOiSGic/giphy.gif"

# --- INITIALIZE APP STATE ---
if "step" not in st.session_state:
    st.session_state.step = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = None

current_step = st.session_state.step

# Determine current watermark text
current_watermark = QUESTIONS[current_step]["watermark"] if current_step < len(QUESTIONS) else "GRANDCHILD!"

# --- INJECT DYNAMIC BACKGROUND WATERMARK CSS ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.92));
    }}
    .stApp::before {{
        content: "{current_watermark}";
        position: fixed;
        top: 40%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-15deg);
        font-size: clamp(60px, 12vw, 130px);
        font-weight: 900;
        color: rgba(217, 4, 41, 0.08);
        text-transform: uppercase;
        pointer-events: none;
        white-space: nowrap;
        z-index: 0;
    }}
    .stButton>button {{
        background-color: #ff4b4b;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 8px 24px;
        width: 100%;
    }}
    .big-announcement {{
        font-size: 30px;
        font-weight: bold;
        color: #d90429;
        text-align: center;
        border: 3px dashed #d90429;
        padding: 25px;
        border-radius: 15px;
        background-color: #fff0f3;
    }}
    </style>
""", unsafe_unsafe_allow_html=True)

# Function to dynamically blur ultrasound image based on progress
def get_focused_ultrasound(step, max_steps):
    img_path = "ultrasound.jpg"
    if os.path.exists(img_path):
        image = Image.open(img_path)
        # Calculate blur radius (Level 0 = Blur 25, Level 7 = Blur 2, Final = Blur 0)
        blur_radius = max(0, (max_steps - step) * 3.5)
        if blur_radius > 0:
            return image.filter(ImageFilter.GaussianBlur(blur_radius))
        return image
    return None

# --- GUI HEADER ---
st.title("🧩 The Family Mystery Challenge")
st.write("Solve the riddles to reveal the secret image!")
st.write("---")

# --- GAME LOGIC ---
if current_step < len(QUESTIONS):
    # Progress Bar
    progress = (current_step) / len(QUESTIONS)
    st.progress(progress)
    st.caption(f"Progress: Level {current_step + 1} of {len(QUESTIONS)}")

    # Display Current Question
    q_data = QUESTIONS[current_step]
    st.subheader(q_data["q"])
    
    # Form with Radio Options
    with st.form(key=f"form_{current_step}"):
        selected_option = st.radio("Select your answer:", q_data["options"], key=f"radio_{current_step}")
        submit_button = st.form_submit_button(label="Submit Answer")

    if submit_button:
        if selected_option == q_data["correct"]:
            st.session_state.feedback = "correct"
            st.session_state.step += 1
            st.rerun()
        else:
            st.session_state.feedback = "wrong"

    # Display GIFs & Blurred Image Progress
    if st.session_state.feedback == "wrong":
        st.error(f"Incorrect! Hint: {q_data['hint']}")
        st.image(THINKING_GIF, caption="Hmm... try another option!", width=260)
    elif st.session_state.feedback == "correct":
        st.success("Correct! The mystery picture is getting clearer...")
        st.image(SUCCESS_GIF, caption="Great job!", width=260)
        st.session_state.feedback = None

    # Show gradually focusing image preview below
    focused_img = get_focused_ultrasound(current_step, len(QUESTIONS))
    if focused_img:
        st.write("### 🔍 Mystery Preview:")
        st.image(focused_img, caption=f"Focus Level: {(current_step/len(QUESTIONS))*100:.0f}%", width=350)

# --- FINAL REVEAL SCREEN ---
else:
    st.progress(1.0)
    st.balloons()
    
    st.markdown("""
        <div class="big-announcement">
            🎉 SURPRISE! WE ARE HAVING A BABY! 👶<br><br>
            <span style="font-size: 22px; color: #333;">
                You are going to be <b>DADA & DADI / NANA & NANI</b>! ❤️
            </span><br><br>
            <span style="font-size: 18px; color: #555;">
                Expected Arrival: [Insert Due Date Here]
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    # Display 100% crystal clear ultrasound photo
    final_img = get_focused_ultrasound(len(QUESTIONS), len(QUESTIONS))
    if final_img:
        st.image(final_img, caption="100% Focused: Our Very First Photo! ❤️", use_container_width=True)
