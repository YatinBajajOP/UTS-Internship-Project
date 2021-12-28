import mmsystem
import streamlit as st
import pandas as pd
import win32com.client
import os
import mysql.connector
import SessionState
from datetime import date


def app(session_state):
    if session_state.res[5] == "YES":
        conn = mysql.connector.connect(host="localhost", user="root", passwd="12345", database="UTS")
        myCursor = conn.cursor()

        st.title("Farmer's Loan Eligibility Check")

        st.write("Applied loan details:")
        myCursor.execute("SELECT * FROM LOAN_DETAILS;")
        res = myCursor.fetchall()
        lst = []
        for x in res:
            lst.append(x)
        df = pd.DataFrame(lst,
                          columns=["USER", "LOAN_AMT", "FEES_AND_CHARGES", "TENURE", "INTEREST_RATE",
                                   "EMI", "INTEREST_AMT", "TOTAL_REPAYMENT", "DATE_OF_APPLICATION"])
        st.write(df)
    else:
        try:
            conn = mysql.connector.connect(host="localhost", user="root", passwd="12345", database="UTS")
            myCursor = conn.cursor()
            myCursor.execute("SELECT SCORE FROM ELIGIBILITY_DETAILS WHERE USER='{}';".format(session_state.user))
            SCORE = str(myCursor.fetchone()[0])
            conn.close()
            if SCORE == 'None':
                st.write("Login after sometime, we have your details. Your score will be calculated soon.")

            elif float(SCORE) > 50.0:

                st.title("Apply for Loan")
                pwd = os.getcwd()

                # Loading the scoreCalculator tksolver model and opening it
                objTKSolver = win32com.client.Dispatch("TKWX.Document")
                objTKSolver.LoadModel("r", pwd + "\\riskScoreCalculator.tkwx")
                # objTKSolver.ShowWindow(3)
                # session_state = SessionState.get(x=False,y=False,)
                # farmers details

                MIN_loan = 50000
                MAX_loan = 2500000
                MIN_charges = 0
                MAX_charges = 100000

                def EMI_CALC():
                    objTKSolver.SetValue("P", "i", loan)
                    objTKSolver.SetValue("R", "i", rate / (12 * 100))
                    objTKSolver.SetValue("N", "i", tenure)
                    objTKSolver.Solve()
                    EMI = objTKSolver.GetValue("EMI", "o")
                    # EMI= (P * R * (1+R)**N)/((1*R)**N-1).
                    return EMI

                def interest():
                    objTKSolver.SetValue("P", "i", loan)
                    objTKSolver.SetValue("R", "i", rate)
                    objTKSolver.Solve()
                    i = objTKSolver.GetValue("I", "o")
                    return i

                def payment():
                    objTKSolver.SetValue("P", "i", loan)
                    objTKSolver.GetValue("I", "o")
                    objTKSolver.SetValue("fees", "i", fees)
                    objTKSolver.Solve()
                    pay = objTKSolver.GetValue("T", "o")
                    return pay

                # col1, col2, col3 = st.beta_columns(3)
                # x = st.button("Apply for loan")
                # if x:
                # session_state.x = True

                # if session_state.x:

                st.subheader("Farmer's Loan Application Form")
                loan = st.slider("Select your Loan Amount requirement", MIN_loan, MAX_loan, 50000, step=25000)
                # with col2:
                st.write("Your loan amount is:", loan)
                fees = st.slider("Fees & Charges:", MIN_charges, MAX_charges, 500, step=500)
                # with col2:
                st.write("Your fees & charges are:", fees)
                tenure = st.number_input("Tenure:", 12)
                rate = st.number_input("Interest Rate (%):", 3.5)
                emi = EMI_CALC()
                int_amt = interest()
                repayment = payment()
                # st.write(emi)

                user_data = {
                    'LOAN_AMT': str(loan),
                    'FEES_AND_CHARGES': str(fees),
                    'TENURE': str(tenure),
                    'INTEREST_RATE': "{:.2f}".format(float(rate)),
                    'EMI': emi,
                    'INTEREST_AMT': "{:.2f}".format(float(int_amt)),
                    'TOTAL_REPAYMENT': "{:.2f}".format(float(repayment)),
                }
                features = pd.DataFrame(user_data, index=[0])
                st.write("Your final selections are:")
                st.write(features)

                # Storing the data in the database
                if st.button("Apply"):
                    data = (str(session_state.user),) + tuple(user_data.values()) + (str(date.today()),)
                    conn = mysql.connector.connect(host="localhost", user="root", passwd="12345", database="UTS")
                    myCursor = conn.cursor()
                    myCursor.execute("CREATE TABLE IF NOT EXISTS LOAN_DETAILS(USER VARCHAR(20), LOAN_AMT "
                                     "BIGINT, FEES_AND_CHARGES FLOAT, TENURE INT, INTEREST_RATE FLOAT, EMI VARCHAR(25),"
                                     "INTEREST_AMT FLOAT, TOTAL_REPAYMENT FLOAT, DATE_OF_APPLICATION DATE);")

                    myCursor.execute("INSERT INTO LOAN_DETAILS VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);", data)
                    conn.commit()
                    conn.close()
                    st.write("Details submitted to the database.")
            else:
                st.write("You are not eligible to apply for the Loan.")
        except:
            st.write("Get your eligibility checked from eligibility tab")


