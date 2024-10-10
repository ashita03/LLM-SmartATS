import streamlit as st


main_page = st.Page("navigation/main.py", title="Home", icon="🏠", default=True,)
resume_review_page = st.Page("navigation/resume_review.py", title="Resume review", icon="📄",)
cover_letter_page = st.Page("navigation/cover_letter.py", title="Cover Letter", icon="✍🏻",)

pg = st.navigation({"Info":[main_page],
                    "Features":[resume_review_page, cover_letter_page]})



pg.run()

    






