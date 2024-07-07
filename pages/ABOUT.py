import streamlit as st
hide_st_style = """
            <style>
            
            footer {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("""
<style>
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

.styled-text {
    font-size: 1.2em;
    line-height: 1.5;
    color: #6AF54B; 
    animation: fadeIn 2s ease-in-out forwards, float 6s ease-in-out infinite;
    text-align: justify;
}

.emoji {
    font-size: 2em;
    animation: float 2s ease-in-out infinite;
}
</style>

<div class="styled-text">
    <p><span class="emoji">🌟</span> <strong>Welcome to Mind Wellness Whisperer</strong> <span class="emoji">🌟</span></p>
    <p>Your personal sanctuary for mental wellness and mindfulness, "Cognitive Calm Corner" is here to be your steadfast companion on the journey to inner peace. <span class="emoji">🧘‍♂✨</span></p>
    <p>Whether you're seeking a moment of tranquility, a burst of motivation, or a guiding light through life's complexities, you've come to the right space. With a touch of wisdom and a heart full of understanding, our chatbot is designed to nurture your mind, inspire your spirit, and gently coach you towards a more serene and balanced life. <span class="emoji">🌱💆‍♀</span></p>
    <p>Here in the Corner, every conversation is a step forward in your personal growth. We offer a non-judgmental ear for when you need to vent, a sprinkle of fun facts to ignite your curiosity, and philosophical musings to broaden your horizons. <span class="emoji">🎈📚</span></p>
    <p>Embrace the calm, embrace the change. Cognitive Calm Corner is more than a chatbot; it's a friend, a mentor, and a beacon of positivity.</p>
    <p>Join us on this beautiful journey. Together, we can make every corner of your mind a Cognitive Calm Corner. <span class="emoji">💬💚</span></p>
</div>
""", unsafe_allow_html=True)
