import login
import viz
import percentage
import eligibility
import loan
import signup
import streamlit as st
import SessionState
PAGES = {
    "Login": login,
    "SignUp": signup,
    "Visualization": viz,
    "Visualization II": percentage,
    "Eligibility": eligibility,
    "Apply for Loan": loan,
}
session_state = SessionState.get(x=False, y=False, z=False, SCORE=None, Z=False, login_state=False, user='', passwd='', res=None,count=0,pred=False)

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]

if selection in ["Login" , "Visualization","Visualization II", "Eligibility", "Apply for Loan", "SignUp"]:
    if selection in ["Login", "Visualization","Visualization II", "Eligibility", "Apply for Loan"]:
        page.app(session_state)
    elif selection in ["Eligibility", "Apply for Loan"]:
        page.app(session_state)
    else:
        page.app()
