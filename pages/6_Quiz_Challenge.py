import streamlit as st
import random


# ─────────────────────────────────────────────────────────────────────────────
# Quiz Questions Database
# ─────────────────────────────────────────────────────────────────────────────
QUIZ_QUESTIONS = [
    {
        "question": "Which country topped the medal tally at Paris 2024 with the most total medals?",
        "options": ["China", "United States", "Great Britain", "France"],
        "correct": "United States",
        "explanation": "The United States won 126 total medals (40 Gold, 44 Silver, 42 Bronze), the most of any country at Paris 2024."
    },
    {
        "question": "How many gold medals did China win at Paris 2024?",
        "options": ["35", "40", "45", "38"],
        "correct": "40",
        "explanation": "China won 40 gold medals, tying with the United States for the most gold medals at Paris 2024."
    },
    {
        "question": "Which iconic Paris landmark hosted the Beach Volleyball events?",
        "options": ["Louvre Museum", "Eiffel Tower Stadium", "Arc de Triomphe", "Notre-Dame"],
        "correct": "Eiffel Tower Stadium",
        "explanation": "The Eiffel Tower Stadium, located at the Champ de Mars, hosted the Beach Volleyball competitions with the iconic tower as backdrop."
    },
    {
        "question": "Which country is the host nation of the Paris 2024 Olympics?",
        "options": ["Germany", "Spain", "France", "Italy"],
        "correct": "France",
        "explanation": "France hosted the 2024 Summer Olympics in Paris, marking the third time the city has hosted the Games (after 1900 and 1924)."
    },
    {
        "question": "Which sport made its Olympic debut at Paris 2024?",
        "options": ["Skateboarding", "Breaking", "Sport Climbing", "Surfing"],
        "correct": "Breaking",
        "explanation": "Breaking (breakdancing) made its Olympic debut at Paris 2024, held at La Concorde."
    },
    {
        "question": "In which venue were the Fencing and Taekwondo events held?",
        "options": ["Bercy Arena", "Grand Palais", "Stade de France", "Champ de Mars Arena"],
        "correct": "Grand Palais",
        "explanation": "The Grand Palais, a historic exhibition hall built for the 1900 World's Fair, hosted Fencing and Taekwondo."
    },
    {
        "question": "Which country won the most gold medals in Swimming at Paris 2024?",
        "options": ["Australia", "United States", "China", "Great Britain"],
        "correct": "United States",
        "explanation": "The United States dominated swimming at Paris 2024, winning the most gold medals in the pool."
    },
    {
        "question": "Where were the Surfing events held at Paris 2024?",
        "options": ["Nice Beach", "Marseille Marina", "Teahupo'o, Tahiti", "Biarritz"],
        "correct": "Teahupo'o, Tahiti",
        "explanation": "The surfing events were held at Teahupo'o in Tahiti, French Polynesia, about 15,000 km from Paris!"
    },
    {
        "question": "Which stadium hosted the Athletics events and Opening/Closing ceremonies?",
        "options": ["Parc des Princes", "Stade de France", "Bercy Arena", "Lyon Stadium"],
        "correct": "Stade de France",
        "explanation": "The Stade de France in Saint-Denis hosted Athletics events and the Closing Ceremony."
    },
    {
        "question": "How many sports were contested at Paris 2024?",
        "options": ["28", "32", "35", "40"],
        "correct": "32",
        "explanation": "Paris 2024 featured 32 sports with 329 events across various disciplines."
    },
    {
        "question": "Which country won the gold medal in Men's Football at Paris 2024?",
        "options": ["Argentina", "France", "Spain", "Brazil"],
        "correct": "Spain",
        "explanation": "Spain won the gold medal in Men's Football at Paris 2024."
    },
    {
        "question": "Which venue hosted the Tennis events at Paris 2024?",
        "options": ["Wimbledon", "Stade Roland-Garros", "Bercy Arena", "Grand Palais"],
        "correct": "Stade Roland-Garros",
        "explanation": "The famous Roland-Garros stadium, home of the French Open, hosted Olympic Tennis."
    },
    {
        "question": "What was the official mascot of Paris 2024?",
        "options": ["Marianne", "The Phryges", "Eiffel", "Pierre"],
        "correct": "The Phryges",
        "explanation": "The Phryges (Olympic Phryge and Paralympic Phryge) were the official mascots, inspired by the Phrygian cap."
    },
    {
        "question": "Which country won the Women's Basketball gold medal?",
        "options": ["France", "United States", "Australia", "China"],
        "correct": "United States",
        "explanation": "The United States women's basketball team continued their dominant streak, winning gold at Paris 2024."
    },
    {
        "question": "In which month did the Paris 2024 Olympics take place?",
        "options": ["June 2024", "July-August 2024", "August-September 2024", "September 2024"],
        "correct": "July-August 2024",
        "explanation": "The Paris 2024 Olympics ran from July 26 to August 11, 2024."
    },
    {
        "question": "Which historic palace hosted Equestrian events?",
        "options": ["Elysée Palace", "Château de Versailles", "Louvre Palace", "Luxembourg Palace"],
        "correct": "Château de Versailles",
        "explanation": "The magnificent Château de Versailles hosted Equestrian and Modern Pentathlon events."
    },
    {
        "question": "How many total medals did Japan win at Paris 2024?",
        "options": ["35", "40", "45", "50"],
        "correct": "45",
        "explanation": "Japan won 45 total medals (20 Gold, 12 Silver, 13 Bronze) at Paris 2024."
    },
    {
        "question": "Which country won the most medals in Judo?",
        "options": ["France", "Japan", "South Korea", "Georgia"],
        "correct": "Japan",
        "explanation": "Japan, the birthplace of Judo, dominated the sport at Paris 2024."
    },
    {
        "question": "Where were the Rowing and Canoe events held?",
        "options": ["Seine River", "Marseille Marina", "Vaires-sur-Marne Nautical Stadium", "Lake Geneva"],
        "correct": "Vaires-sur-Marne Nautical Stadium",
        "explanation": "The Vaires-sur-Marne Nautical Stadium, east of Paris, hosted Rowing, Canoe Slalom, and Canoe Sprint."
    },
    {
        "question": "Which country did the host nation France rank in the final medal tally?",
        "options": ["3rd", "4th", "5th", "6th"],
        "correct": "5th",
        "explanation": "France finished 5th in the medal tally with 64 medals (16 Gold, 26 Silver, 22 Bronze)."
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Session State Initialization
# ─────────────────────────────────────────────────────────────────────────────
def init_session_state():
    """Initialize session state variables."""
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "quiz_completed" not in st.session_state:
        st.session_state.quiz_completed = False
    if "answer_submitted" not in st.session_state:
        st.session_state.answer_submitted = False


def start_quiz(num_questions=10):
    """Start a new quiz with random questions."""
    st.session_state.quiz_started = True
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.quiz_completed = False
    st.session_state.answer_submitted = False
    
    # Select random questions
    questions = random.sample(QUIZ_QUESTIONS, min(num_questions, len(QUIZ_QUESTIONS)))
    st.session_state.quiz_questions = questions


def reset_quiz():
    """Reset the quiz to initial state."""
    st.session_state.quiz_started = False
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.quiz_questions = []
    st.session_state.quiz_completed = False
    st.session_state.answer_submitted = False


def next_question():
    """Move to the next question."""
    st.session_state.current_question += 1
    st.session_state.answer_submitted = False
    
    if st.session_state.current_question >= len(st.session_state.quiz_questions):
        st.session_state.quiz_completed = True


# ─────────────────────────────────────────────────────────────────────────────
# Display Functions
# ─────────────────────────────────────────────────────────────────────────────
def display_welcome_screen():
    """Display the quiz welcome screen."""
    
    # Header
    st.markdown("# 🏅 Paris 2024 Quiz Challenge")
    st.markdown("### Test your knowledge about the Paris 2024 Olympic Games!")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### 📋 How to Play
        
        1. **Select** the number of questions you want to answer
        2. **Click** "Start Quiz" to begin
        3. **Choose** your answer for each question
        4. **Submit** to see if you're correct
        5. **Track** your score as you progress
        
        ---
        
        ### 🏆 Scoring System
        
        | Result | Points |
        |--------|--------|
        | ✅ Correct Answer | +1 point |
        | ❌ Wrong Answer | 0 points |
        
        ---
        
        ### 🎖️ Achievement Levels
        
        - 🏆 **Olympic Champion**: 90%+ correct
        - 🥈 **Silver Medalist**: 70-89% correct
        - 🥉 **Bronze Medalist**: 50-69% correct
        - 🎽 **Participant**: Below 50%
        
        ---
        """)
        
        num_questions = st.slider(
            "📊 Number of Questions",
            min_value=5,
            max_value=min(20, len(QUIZ_QUESTIONS)),
            value=10,
            step=1
        )
        
        st.markdown("")
        
        if st.button("🚀 Start Quiz", use_container_width=True, type="primary"):
            start_quiz(num_questions)
            st.rerun()


def display_question():
    """Display the current question."""
    
    questions = st.session_state.quiz_questions
    current_idx = st.session_state.current_question
    current_q = questions[current_idx]
    
    # Progress bar
    progress = (current_idx) / len(questions)
    st.progress(progress)
    
    # Question counter and score in columns
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        st.markdown(f"### Question {current_idx + 1} of {len(questions)}")
    
    with col3:
        st.success(f"🏆 Score: {st.session_state.score} / {current_idx}")
    
    st.markdown("---")
    
    # Question display
    st.markdown(f"## ❓ {current_q['question']}")
    
    st.markdown("---")
    
    # Answer options
    if not st.session_state.answer_submitted:
        st.markdown("### 📝 Select your answer:")
        
        selected = st.radio(
            "Choose one option:",
            options=current_q["options"],
            index=None,
            key=f"answer_radio_{current_idx}",
            label_visibility="collapsed"
        )
        
        st.markdown("")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_disabled = selected is None
            if st.button("✅ Submit Answer", use_container_width=True, type="primary", disabled=submit_disabled):
                # Check answer
                is_correct = selected == current_q["correct"]
                
                if is_correct:
                    st.session_state.score += 1
                
                st.session_state.answers.append({
                    "question": current_q["question"],
                    "selected": selected,
                    "correct": current_q["correct"],
                    "is_correct": is_correct,
                    "explanation": current_q["explanation"]
                })
                
                st.session_state.answer_submitted = True
                st.rerun()
    
    else:
        # Show answer result
        last_answer = st.session_state.answers[-1]
        
        # Display the options with correct/incorrect highlighting
        for option in current_q["options"]:
            if option == last_answer["correct"]:
                st.success(f"✅ {option} ← Correct Answer")
            elif option == last_answer["selected"] and not last_answer["is_correct"]:
                st.error(f"❌ {option} ← Your Answer")
            else:
                st.markdown(f"⚪ {option}")
        
        st.markdown("---")
        
        # Result message
        if last_answer["is_correct"]:
            st.balloons()
            st.success("### 🎉 Correct! +1 Point")
        else:
            st.error(f"### ❌ Incorrect! The correct answer was: **{last_answer['correct']}**")
        
        # Explanation
        st.info(f"💡 **Explanation:** {last_answer['explanation']}")
        
        st.markdown("")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if current_idx + 1 < len(questions):
                if st.button("➡️ Next Question", use_container_width=True, type="primary"):
                    next_question()
                    st.rerun()
            else:
                if st.button("🏁 See Results", use_container_width=True, type="primary"):
                    next_question()
                    st.rerun()


def display_results():
    """Display the final quiz results."""
    
    score = st.session_state.score
    total = len(st.session_state.quiz_questions)
    percentage = (score / total) * 100 if total > 0 else 0
    
    # Determine grade and message
    if percentage >= 90:
        grade = "🏆 Olympic Champion!"
        message = "Outstanding! You're a true Olympics expert!"
        st.balloons()
    elif percentage >= 70:
        grade = "🥈 Silver Medalist"
        message = "Great job! You know your Olympics well!"
    elif percentage >= 50:
        grade = "🥉 Bronze Medalist"
        message = "Good effort! Keep learning about the Olympics!"
    else:
        grade = "🎽 Participant"
        message = "Don't give up! Try again to improve your score!"
    
    # Results header
    st.markdown(f"# {grade}")
    st.markdown(f"### {message}")
    
    st.markdown("---")
    
    # Score display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="✅ Correct Answers",
            value=score,
            delta=None
        )
    
    with col2:
        st.metric(
            label="📊 Final Score",
            value=f"{percentage:.0f}%",
            delta=None
        )
    
    with col3:
        st.metric(
            label="❌ Incorrect Answers",
            value=total - score,
            delta=None
        )
    
    st.markdown("---")
    
    # Visual score bar
    st.markdown("### 📈 Performance Overview")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(percentage / 100)
    with col2:
        st.markdown(f"**{score}/{total}**")
    
    st.markdown("---")
    
    # Review answers
    st.markdown("### 📋 Review Your Answers")
    
    for i, answer in enumerate(st.session_state.answers):
        icon = "✅" if answer['is_correct'] else "❌"
        with st.expander(f"Question {i+1}: {icon} {answer['question'][:60]}..."):
            st.markdown(f"**Question:** {answer['question']}")
            st.markdown(f"**Your Answer:** {answer['selected']}")
            st.markdown(f"**Correct Answer:** {answer['correct']}")
            
            if answer['is_correct']:
                st.success("✅ You got this one right!")
            else:
                st.error("❌ Incorrect")
            
            st.info(f"💡 {answer['explanation']}")
    
    st.markdown("---")
    
    # Play again button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Play Again", use_container_width=True, type="primary"):
            reset_quiz()
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="Quiz Challenge - Paris 2024",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    init_session_state()
    
    # Sidebar with quit option during quiz
    if st.session_state.quiz_started and not st.session_state.quiz_completed:
        with st.sidebar:
            st.markdown("### 🎮 Quiz Controls")
            st.metric("Score", st.session_state.score)
            st.metric("Question", f"{st.session_state.current_question + 1}/{len(st.session_state.quiz_questions)}")
            
            st.markdown("---")
            
            if st.button("🚪 Quit Quiz", use_container_width=True):
                reset_quiz()
                st.rerun()
    
    # Main content
    if not st.session_state.quiz_started:
        display_welcome_screen()
    elif st.session_state.quiz_completed:
        display_results()
    else:
        display_question()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888;'>"
        "Paris 2024 Olympic Games Quiz | Built with Streamlit"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
