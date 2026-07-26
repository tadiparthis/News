import streamlit as st
import os
import time
from PIL import Image, ImageFilter

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="The Family Mystery Challenge", page_icon="🎁", layout="centered")

# --- MULTIPLE CHOICE QUESTIONS SETUP ---
QUESTIONS = [
    {
        "q": "Question 1: In a Nuclear Power Plant, what type of reaction occurs to split atoms?",
        "options": ["Nuclear Fission", "Nuclear Fusion", "Nuclear Fashion", "Nuclear Focus"],
        "correct_options": ["Nuclear Fission"],
        "hint": "It splits atoms to generate energy!",
        "watermark": "Nibling"
    },
    {
        "q": "Question 2: If you can crack this formula, you have a big clue hidden in the options! What is (a+b)²?",
        "options": ["a^2+b^2+2ab", "ay+by", "ba+by+2ab", "ba+ay+4ab"],
        "correct_options": ["a^2+b^2+2ab"],
        "hint": "A squared plus B squared plus 2AB!",
        "watermark": "Mom"
    },
    {
        "q": "Question 3: At what high sound frequencies can dogs hear that humans cannot?",
        "options": ["Micro-wave", "Radio wave", "Ultrasound", "Infrared"],
        "correct_options": ["Ultrasound"],
        "hint": "It starts with 'Ultra'!",
        "watermark": "Dad"
    },
    {
        "q": "Question 4: Which famous baby in the Old Testament was saved in a basket floating on the Nile River?",
        "options": ["Moses", "David", "Solomon", "Noah"],
        "correct_options": ["Moses"],
        "hint": "He grew up to lead his people!",
        "watermark": "Nani"
    },
    {
        "q": "Question 5: In Genesis 1:28, God blessed mankind and commanded them to do what?",
        "options": ["Divide", "Preach", "Multiply", "Heal"],
        "correct_options": ["Multiply"],
        "hint": "Think about things growing bigger!",
        "watermark": "Nana"
    },
    {
        "q": "Question 6: According to the promise, Israel is a land flowing with ___ and honey?",
        "options": ["Wine", "Water", "MILK", "Olives"],
        "correct_options": ["MILK"],
        "hint": "White in color!",
        "watermark": "Dadi"
    },
    {
        "q": "Question 7: According to Psalm 127:3, children are:",
        "options": [
            "A temporary responsibility, not a gift", 
            "A test from man, a punishment from God", 
            "A burden for parents, a curse for families", 
            "A heritage from the Lord, a reward from Him"
        ],
        "correct_options": ["A heritage from the Lord, a reward from Him"],
        "hint": "The best promotion in the family!",
        "watermark": "Granddaughter"
    },
    {
        "q": "Question 8 (FINAL): If you remember all the answers, what does it all boil down to?",
        "options": ["Increasing", "Multiply", "A Ba Be", "Unto us... WE ARE HAVING A BABY!"],
        "correct_options": ["Increasing", "Multiply", "A Ba Be", "Unto us... WE ARE HAVING A BABY!"],
        "hint": "Pick any option to see the big reveal!",
        "watermark": "BABY IS COMING!"
    }
]

# GIF URLs
SUCCESS_GIF  = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeTAxOHB2b2VycTZwbW9hcXk1cGwyeW56eGdodW5wa2FoOXl6dzB4eCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/DffShiJ47fPqM/giphy.gif"
THINKING_GIF = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTdwOHM4dHJmZmVxNnJmeGtnemQ3aDJocGh2Z2N5OTU3NzhhM2FnaiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/eKrgVyZ7zLvJrgZNZn/giphy.gif"

# --- INITIALIZE APP STATE ---
if "step" not in st.session_state:
    st.session_state.step = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = None

current_step = st.session_state.step

# Determine current watermark text
current_watermark = QUESTIONS[current_step]["watermark"] if current_step < len(QUESTIONS) else "GRANDCHILD!"

# --- INJECT CUSTOM STYLING ---
st.markdown(f"""
    <style>
    /* High contrast black text globally */
    html, body, [class*="css"], .stMarkdown, p, div, label, span {{
        color: #000000 !important;
        font-weight: 600;
    }}
    
    .stApp {{
        background: #ffffff;
    }}
    
    /* Watermark styling */
    .stApp::before {{
        content: "{current_watermark}";
        position: fixed;
        top: 40%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-15deg);
        font-size: clamp(60px, 12vw, 130px);
        font-weight: 900;
        color: rgba(200, 0, 0, 0.03);
        text-transform: uppercase;
        pointer-events: none;
        white-space: nowrap;
        z-index: 0;
    }}
    
    /* Question Header Size */
    .question-title {{
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #000000 !important;
        margin-top: 10px;
        margin-bottom: 10px;
    }}
    
    /* Radio Options */
    .stRadio label {{
        font-size: 27px !important;
        font-weight: 700 !important;
        color: #000000 !important;
        padding: 4px 0px;
    }}

    .stRadio p {{
        font-size: 27px !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }}
    
    /* SUBMIT BUTTON */
    .stButton > button,
    div[data-testid="stFormSubmitButton"] > button,
    div[data-testid="stFormSubmitButton"] button p {{
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #000000 !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        border-radius: 10px !important;
        padding: 8px 20px !important;
        width: 100% !important;
        border: 3px solid #000000 !important;
        box-shadow: 2px 3px 6px rgba(0,0,0,0.15) !important;
    }}
    
    .stButton > button:hover,
    .stButton > button:focus,
    .stButton > button:active,
    div[data-testid="stFormSubmitButton"] > button:hover,
    div[data-testid="stFormSubmitButton"] > button:focus,
    div[data-testid="stFormSubmitButton"] > button:active {{
        background-color: #f2f2f2 !important;
        background: #f2f2f2 !important;
        color: #000000 !important;
        border-color: #000000 !important;
    }}
    
    /* Tighten white space */
    .stMarkdown {{
        margin-bottom: -10px;
    }}
    
    /* Fix image container sizing */
    [data-testid="stImage"] {{
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }}
    
    [data-testid="stImage"] img {{
        width: 100% !important;
        max-width: 600px !important;
        height: auto !important;
        border-radius: 12px;
        border: 2px solid #ddd;
    }}
    
    /* Announcement Box */
    .big-announcement {{
        font-size: 29px;
        font-weight: bold;
        color: #d90429 !important;
        text-align: center;
        border: 4px dashed #d90429;
        padding: 20px;
        border-radius: 15px;
        background-color: #fff0f3;
    }}
    </style>
""", unsafe_allow_html=True)

# Function to dynamically blur ultrasound image based on progress
def get_focused_ultrasound(step, max_steps):
    img_path = "ultrasound.jpg"
    if os.path.exists(img_path):
        try:
            image = Image.open(img_path).convert("RGB")
            blur_radius = max(0, (max_steps - step) * 3.5)
            if blur_radius > 0:
                return image.filter(ImageFilter.GaussianBlur(blur_radius))
            return image
        except Exception as e:
            st.error(f"Error loading image: {e}")
            return None
    return None

# --- GUI HEADER ---
st.title("🧩 The Family Mystery Challenge")
st.markdown("<p style='margin-bottom: -5px; font-size: 18px;'>Solve the riddles to reveal the secret image!</p>", unsafe_allow_html=True)

# --- GAME LOGIC ---
if current_step < len(QUESTIONS):
    # Progress Bar
    progress = (current_step) / len(QUESTIONS)
    st.progress(progress)
    st.caption(f"Progress: Level {current_step + 1} of {len(QUESTIONS)}")

    # Display Current Question
    q_data = QUESTIONS[current_step]
    st.markdown(f'<div class="question-title">{q_data["q"]}</div>', unsafe_allow_html=True)
    
    # Form with Radio Options
    with st.form(key=f"form_{current_step}"):
        selected_option = st.radio("Select your answer:", q_data["options"], key=f"radio_{current_step}")
        submit_button = st.form_submit_button(label="Submit Answer")

    if submit_button:
        if selected_option in q_data["correct_options"]:
            st.session_state.feedback = "correct"
        else:
            st.session_state.feedback = "wrong"
        st.rerun()

    # Display GIFs with temporary 2-second timeout
    if st.session_state.feedback == "wrong":
        st.error(f"Incorrect! Hint: {q_data['hint']}")
        st.image(THINKING_GIF, caption="Hmm... try another option!", width=260)
        time.sleep(2)
        st.session_state.feedback = None
        st.rerun()

    elif st.session_state.feedback == "correct":
        st.success("Correct! Moving to the next level...")
        st.image(SUCCESS_GIF, caption="Great job!", width=260)
        time.sleep(2)
        st.session_state.feedback = None
        st.session_state.step += 1
        st.rerun()

    # Show gradually focusing image preview below
    focused_img = get_focused_ultrasound(current_step, len(QUESTIONS))
    if focused_img:
        st.write("### 🔍 Mystery Preview:")
        st.image(focused_img, caption=f"Focus Level: {(current_step/len(QUESTIONS))*100:.0f}%", use_container_width=True)
    else:
        st.warning("⚠️ Please place your 'ultrasound.jpg' file in the app folder to display the reveal picture.")

# --- FINAL REVEAL SCREEN ---
else:
    st.progress(1.0)
    st.balloons()
    
    AUDIO_URL = "https://raw.githubusercontent.com/tadiparthis/News/main/thank_you_lord.mp3"
    
    # SINGLE CLEAN AUDIO PLAYER (Prevents double audio playing)
    st.audio(AUDIO_URL, format="audio/mp3", start_time=52, autoplay=True)
    
    st.markdown("""
        <div class="big-announcement">
            🎉  WE ARE HAVING A BABY! 👶<br><br>
            <span style="font-size: 21px; color: #111111; font-weight: bold;">
                You are going to be <b>Great GrandPa & Great GrandMa / NANA & NANI/ </b>! ❤️
                ATTA & MAMU / GrandMa & GrandPa / MS - ATTA & MBA- ATTA / </b>! ❤️
            </span><br><br>
            <span style="font-size: 18px; color: #222222; font-weight: 600;">
                Expected Arrival: March, 2027
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    # Display 100% crystal clear ultrasound photo full width
    final_img = get_focused_ultrasound(len(QUESTIONS), len(QUESTIONS))
    if final_img:
        st.image(final_img, caption="100% Focused: Our Very First Photo! ❤️", use_container_width=True)
    else:
        st.warning("⚠️ Make sure 'ultrasound.jpg' is located in the same directory as this script.")
        
    st.stop()
