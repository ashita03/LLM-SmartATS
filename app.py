import streamlit as st
from navigation.main import main
from navigation.cover_letter import cover_main

main_page = st.Page("navigation/main.py", title="Home", icon="🏠", default=True,)
resume_review_page = st.Page("navigation/resume_review.py", title="Resume review", icon="📄",)
cover_letter_page = st.Page("navigation/cover_letter.py", title="Cover Letter", icon="✍🏻",)
networking_page = st.Page("navigation/network.py", title="Networking", icon="👩‍💻",)

pg = st.navigation({"Info":[main_page],
                    "Features":[resume_review_page, cover_letter_page, networking_page]})

pg.run()

    






