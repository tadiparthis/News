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

MASK_COLORS = [
    (220, 50, 47),   # Deep Crimson
    (211, 84, 0),    # Burnt Orange
    (241, 196, 15),  # Vibrant Gold
    (39, 174, 96),   # Emerald Green
    (41, 128, 185),  # Ocean Blue
    (142, 68, 173),  # Deep Purple
    (231, 76, 60),   # Coral Red
    (22, 160, 133)   # Teal
]

# --- INITIALIZE APP STATE ---
if "step" not in st.session_state:
    st.session_state.step = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "revealed_at_end" not in st.session_state:
    st.session_state.revealed_at_end = False

current_step = st.session_state.step

# Determine current watermark text
current_watermark = QUESTIONS[current_step]["watermark"] if current_step < len(QUESTIONS) else "GRANDCHILD!"

# --- INJECT CUSTOM STYLING ---
st.markdown(f"""
    <style>
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 700px !important;
    }}
    
    html, body, [class*="css"], .stMarkdown, p, div, label, span {{
        color: #000000 !important;
        font-weight: 600;
    }}
    
    .stApp {{
        background: #ffffff;
    }}
    
    .stApp::before {{
        content: "{current_watermark}";
        position: fixed;
        top: 40%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-15deg);
        font-size: clamp(50px, 10vw, 100px);
        font-weight: 900;
        color: rgba(200, 0, 0, 0.03);
        text-transform: uppercase;
        pointer-events: none;
        white-space: nowrap;
        z-index: 0;
    }}
    
    h1 {{
        font-size: 26px !important;
        padding: 0px !important;
        margin-bottom: -10px !important;
    }}
    
    .question-title {{
        font-size: 25px !important;
        font-weight: 800 !important;
        color: #000000 !important;
        margin-top: 5px;
        margin-bottom: 5px;
        line-height: 1.25 !important;
    }}
    
    .stRadio label {{
        font-size: 21px !important;
        font-weight: 700 !important;
        color: #000000 !important;
        padding: 1px 0px !important;
    }}

    .stRadio p {{
        font-size: 21px !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }}
    
    .stButton > button,
    div[data-testid="stFormSubmitButton"] > button,
    div[data-testid="stFormSubmitButton"] button p {{
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #000000 !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        padding: 5px 15px !important;
        width: 100% !important;
        border: 2.5px solid #000000 !important;
        box-shadow: 1px 2px 4px rgba(0,0,0,0.12) !important;
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
    
    .stMarkdown {{
        margin-bottom: -12px !important;
    }}
    
    [data-testid="stImage"] {{
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }}
    
    [data-testid="stImage"] img {{
        width: 100% !important;
        max-width: 420px !important;
        max-height: 280px !important;
        object-fit: contain !important;
        border-radius: 10px;
        border: 2px solid #ddd;
    }}
    
    .big-announcement {{
        font-size: 24px;
        font-weight: bold;
        color: #d90429 !important;
        text-align: center;
        border: 3px dashed #d90429;
        padding: 12px;
        border-radius: 12px;
        background-color: #fff0f3;
    }}
    </style>
""", unsafe_allow_html=True)

# Function to dynamically mask ultrasound image based on stage
def get_masked_ultrasound(step, force_clear=False):
    img_path = "ultrasound.jpg"
    if os.path.exists(img_path):
        try:
            image = Image.open(img_path).convert("RGBA")
            w, h = image.size
            
            # 1. Force clear reveal at the end after pause
            if force_clear:
                return image.convert("RGB")
            
            # 2. Questions 1 through 6: HEAVILY Blurred, Pixelated and Masked (Unreadable)
            if step < 6:
                pixel_size = 100
                small_w, small_h = max(1, w // pixel_size), max(1, h // pixel_size)
                pixelated = image.resize((small_w, small_h), resample=Image.NEAREST).resize((w, h), resample=Image.NEAREST)
                pixelated = pixelated.filter(ImageFilter.GaussianBlur(15))
                
                overlay = Image.new("RGBA", (w, h), MASK_COLORS[step % len(MASK_COLORS)] + (220,))
                return Image.alpha_composite(pixelated, overlay).convert("RGB")
            
            # 3. Question 7 & 8: Brought partially into perspective
            elif step == 6:  # Question 7
                pixelated = image.resize((max(1, w//16), max(1, h//16)), resample=Image.NEAREST).resize((w, h), resample=Image.NEAREST)
                overlay = Image.new("RGBA", (w, h), MASK_COLORS[6] + (140,))
                return Image.alpha_composite(pixelated, overlay).convert("RGB")
            
            elif step == 7:  # Question 8 (Final Question)
                pixelated = image.resize((max(1, w//8), max(1, h//8)), resample=Image.NEAREST).resize((w, h), resample=Image.NEAREST)
                overlay = Image.new("RGBA", (w, h), MASK_COLORS[7] + (80,))
                return Image.alpha_composite(pixelated, overlay).convert("RGB")
                
            return image.convert("RGB")
            
        except Exception as e:
            st.error(f"Error loading image: {e}")
            return None
    return None

# --- GUI HEADER ---
st.title("🧩 The Family Mystery Challenge")
st.markdown("<p style='margin-bottom: 2px; font-size: 15px;'>Solve the riddles to reveal the secret image!</p>", unsafe_allow_html=True)

# --- GAME LOGIC ---
if current_step < len(QUESTIONS):
    # Progress Bar
    progress = (current_step) / len(QUESTIONS)
    st.progress(progress)

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
        st.image(THINKING_GIF, caption="Hmm... try another option!", width=200)
        time.sleep(2)
        st.session_state.feedback = None
        st.rerun()

    elif st.session_state.feedback == "correct":
        st.success("Correct! Moving to the next level...")
        st.image(SUCCESS_GIF, caption="Great job!", width=200)
        time.sleep(2)
        st.session_state.feedback = None
        st.session_state.step += 1
        st.rerun()

    # Show preview image below
    masked_img = get_masked_ultrasound(current_step)
    if masked_img:
        st.image(masked_img, caption=f"Level {current_step + 1} of {len(QUESTIONS)} — Unmasking Mystery Image...", use_container_width=True)
    else:
        st.warning("⚠️ Please place your 'ultrasound.jpg' file in the app folder to display the reveal picture.")

# --- FINAL REVEAL SCREEN ---
else:
    st.progress(1.0)
    st.balloons()
    
    AUDIO_URL = "https://raw.githubusercontent.com/tadiparthis/News/main/thank_you_lord.mp3"
    
    # AUDIO PLAYER WITH FADE-IN (0-3s) AND FADE-OUT AT 45 SECONDS
    st.components.v1.html(f"""
        <audio id="reveal-audio" controls style="width: 100%; height: 40px;">
            <source src="{AUDIO_URL}#t=52" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        <script>
            const audio = document.getElementById('reveal-audio');
            if (audio) {{
                audio.volume = 0.0;
                const playPromise = audio.play();
                if (playPromise !== undefined) {{
                    playPromise.catch(() => {{ console.log("Autoplay blocked by browser."); }});
                }}

                let fadeInInterval = setInterval(() => {{
                    if (audio.volume < 0.95) {{
                        audio.volume = Math.min(1.0, audio.volume + 0.05);
                    }} else {{
                        audio.volume = 1.0;
                        clearInterval(fadeInInterval);
                    }}
                }}, 150);

                setTimeout(() => {{
                    let fadeOutInterval = setInterval(() => {{
                        if (audio.volume > 0.05) {{
                            audio.volume = Math.max(0.0, audio.volume - 0.05);
                        }} else {{
                            audio.volume = 0.0;
                            audio.pause();
                            clearInterval(fadeOutInterval);
                        }}
                    }}, 250);
                }}, 40000);
            }}
        </script>
    """, height=50)
    
    st.markdown("""
        <div class="big-announcement">
            🎉 SURPRISE! WE ARE HAVING A BABY! 👶<br>
            <span style="font-size: 18px; color: #111111; font-weight: bold;">
                You are going to be <b>DADA & DADI / NANA & NANI</b>! ❤️
            </span><br>
            <span style="font-size: 15px; color: #222222; font-weight: 600;">
                Expected Arrival: [Insert Due Date Here]
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Placeholder for image to enable 6-second delay reveal
    img_container = st.empty()
    
    if not st.session_state.revealed_at_end:
        # Show heavily blurred teaser first while on reveal screen
        blurred_img = get_masked_ultrasound(current_step=0, force_clear=False)
        img_container.image(blurred_img, caption="Revealing the picture in a few seconds...", use_container_width=True)
        
        # Spend 6 seconds on the final screen before displaying the full unmasked picture
        time.sleep(6)
        st.session_state.revealed_at_end = True
        st.rerun()
    else:
        # Display 100% unmasked clear ultrasound photo
        final_img = get_masked_ultrasound(current_step=len(QUESTIONS), force_clear=True)
        if final_img:
            img_container.image(final_img, caption="100% Clear: Our Very First Photo! ❤️", use_container_width=True)
        else:
            st.warning("⚠️ Make sure 'ultrasound.jpg' is located in the same directory as this script.")
        
    st.stop()
