import streamlit as st
import pandas as pd
import win32com.client
import os
import SessionState
import mysql.connector
from datetime import date

# Function that calculates the loan risk score using tk solver
def calculate_tk(Age, Rainfall, Debt, Savings, Weather):
    # Defining some constants
    MIN_AGE = 18
    MAX_AGE = 95
    a = -0.20
    MIN_RAINFALL = 20
    MAX_RAINFALL = 300
    b = 0.50
    MIN_DEBT = 0.0
    MAX_DEBT = 5.0
    c = -0.40
    MIN_SAVINGS = 0.0
    MAX_SAVINGS = 5.0
    d = 0.40
    MIN_WEATHER = 0
    MAX_WEATHER = 100
    e = 0.60
    MIN_MONTH = 1
    MAX_MONTH = 12
    max_value = a * MAX_AGE + b * MAX_RAINFALL + c * MAX_DEBT + d * MAX_SAVINGS + e * MAX_WEATHER

    # Setting up the present working directory as pwd so that the user do not have to set path according to
    # his/her device
    pwd = os.getcwd()

    # Loading the scoreCalculator tksolver model and opening it
    objTKSolver = win32com.client.Dispatch("TKWX.Document")
    objTKSolver.LoadModel("r", pwd + "\\riskScoreCalculator.tkwx")
    # objTKSolver.ShowWindow(3)

    # Entering all the data into tkSolver model
    objTKSolver.SetValue("a", "i", a)
    objTKSolver.SetValue("age", "i", Age)
    objTKSolver.SetValue("b", "i", b)
    objTKSolver.SetValue("rainfall", "i", Rainfall)
    objTKSolver.SetValue("c", "i", c)
    objTKSolver.SetValue("debt", "i", Debt)
    objTKSolver.SetValue("d", "i", d)
    objTKSolver.SetValue("savings", "i", Savings)
    objTKSolver.SetValue("e", "i", e)
    objTKSolver.SetValue("weather", "i", Weather)
    objTKSolver.SetValue("max_value", "i", max_value)
    objTKSolver.Solve()
    sc = objTKSolver.GetValue("score", "o")
    return sc


def app(session_state):
    if session_state.login_state:
        # Admin logs in
        if session_state.res[5] == "YES":
            conn = mysql.connector.connect(host="localhost", user="root", passwd="12345", database="UTS")
            myCursor = conn.cursor()

            st.title("Farmer's Loan Eligibility Check")

            # Title
            st.write("Calculates the score for a farmer who comes in to apply for a loan.\n")
            if st.checkbox("Show all details"):
                myCursor.execute(
                    "CREATE TABLE IF NOT EXISTS ELIGIBILITY_DETAILS(USER VARCHAR (20), AADHAR VARCHAR(14) "
                    "PRIMARY KEY, CROP VARCHAR(10), AGE VARCHAR(4), RAINFALL VARCHAR(10), DEBT VARCHAR(10), "
                    "SAVINGS VARCHAR(10), WEATHER VARCHAR(10), HARVESTING_MONTH VARCHAR(2), SCORE VARCHAR("
                    "4));")
                myCursor.execute("SELECT * FROM ELIGIBILITY_DETAILS;")
                res = myCursor.fetchall()
                lst = []
                for x in res:
                    lst.append(x)
                df = pd.DataFrame(lst,
                                  columns=["USER", "AADHAR", "CROP", "AGE", "RAINFALL", "DEBT", "SAVINGS", "WEATHER",
                                           "HARVESTING_MONTH", "SCORE"])
                st.write(df)
            if st.checkbox("Details of specific customer"):
                aadhar = str(st.text_input("Enter the Aadhar Number of customer:"))
                if st.button("Calculate score"):
                    try:
                        myCursor.execute("SELECT DISTINCT * FROM ELIGIBILITY_DETAILS WHERE AADHAR='{}';".format(aadhar))
                        result = myCursor.fetchall()
                        lst = []
                        for x in result:
                            lst.append(x)
                        df1 = pd.DataFrame(lst, columns=["USER", "AADHAR", "CROP", "AGE", "RAINFALL", "DEBT", "SAVINGS",
                                                         "WEATHER", "HARVESTING_MONTH", "SCORE"])

                        # Updating score in the database
                        SCORE = calculate_tk(str(df1["AGE"][0]), str(df1["RAINFALL"][0]), str(df1["DEBT"][0]), str(df1["SAVINGS"][0]), str(df1["WEATHER"][0]))
                        myCursor.execute("UPDATE ELIGIBILITY_DETAILS SET SCORE='{}' WHERE AADHAR='{}';".format(SCORE[:4], aadhar))
                        conn.commit()
                        conn.close()

                        # Updating score in the dataframe
                        df1["SCORE"] = SCORE[:4]
                        st.write(df1)
                        if float(SCORE) > 50.0:
                            st.write("The loan can be sanctioned! Please Proceed to Apply for Loan page.")
                        else:
                            st.write("The loan cannot be sanctioned!")
                    except:
                        st.write("NO details found")
        # If a customer logs in
        else:
            conn = mysql.connector.connect(host="localhost", user="root", passwd="12345", database="UTS")
            myCursor = conn.cursor()

            st.title("Farmer's Loan Eligibility Check")

            # Title
            st.write("Submits the details of a farmer who comes in to apply for a loan.\n")

            # st.write("Enter your data through the sliders")

            # Defining some constants
            MIN_AGE = 18
            MAX_AGE = 95
            a = -0.20
            MIN_RAINFALL = 20
            MAX_RAINFALL = 300
            b = 0.50
            MIN_DEBT = 0.0
            MAX_DEBT = 5.0
            c = -0.40
            MIN_SAVINGS = 0.0
            MAX_SAVINGS = 5.0
            d = 0.40
            MIN_WEATHER = 0
            MAX_WEATHER = 100
            e = 0.60
            MIN_MONTH = 1
            MAX_MONTH = 12

            session_state = SessionState.get(z=False)

            z = st.button("Check Eligibility for loan")
            if z:
                session_state.z = True

            if session_state.z:

                # To take user input
                def user_input():
                    name = st.text_input("Name:", "Name")
                    aadhar = st.text_input("Aadhar:", "Aadhar")
                    crop = st.selectbox("Crop preferred:", ("Rice", "Maize", "Cotton"))
                    age = st.slider("Age", MIN_AGE, MAX_AGE, 18)
                    rainfall = st.slider("Rainfall(cm)", MIN_RAINFALL, MAX_RAINFALL, 40)
                    debt = st.slider("Debt(cr)", MIN_DEBT, MAX_DEBT, 1.0)
                    savings = st.slider("Savings(cr)", MIN_SAVINGS, MAX_SAVINGS, 1.0)
                    weather = st.slider("Weather", MIN_WEATHER, MAX_WEATHER, 50)
                    Month_of_harvesting = st.slider("Month of harvesting:", MIN_MONTH, MAX_MONTH, 6)

                    # longitude = st.sidebar.text_input("Enter longitude of your plot location:", "Longitude")
                    # latitude = st.sidebar.text_input("Enter latitude of your plot location:", "Latitude")

                    user_data = {
                        'Name': name,
                        'Aadhar': aadhar,
                        'Crop': crop,
                        'Age': age,
                        'Rainfall': rainfall,
                        'Debt': debt,
                        'Savings': savings,
                        'Weather': weather,
                        'Harvest Month': Month_of_harvesting,
                        # 'Longitude':longitude,
                        # 'Latitude': latitude,
                    }
                    # Converting user input into a dataset
                    features = pd.DataFrame(user_data, index=["Details"])
                    return features

                # Printing the user input as a database
                userInput = user_input()
                st.subheader("Farmer Details:")
                st.write(userInput)

                # Visualization through a bar chart
                df0 = userInput.T
                df = df0.iloc[3:-1]
                user_max_data = {
                    'Age': MAX_AGE,
                    'Rainfall': MAX_RAINFALL,
                    'Debt': MAX_DEBT,
                    'Savings': MAX_SAVINGS,
                    'Weather': MAX_WEATHER,
                    'Harvest Month': MAX_MONTH
                }
                df1 = pd.DataFrame(user_max_data, index=["max_value"]).T
                df_final = pd.concat([df, df1], axis=1, join='inner')
                df_final['percentage'] = (df_final['Details'] / df_final['max_value']) * 100
                # print(df_final.head())
                st.bar_chart(df_final['percentage'])

                y = st.button("Submit")
                if y:
                    session_state.y = True
                else:
                    session_state.y = False
                if session_state.y:
                    data = list(userInput.T["Details"])
                    if data[0] != "Name":
                        myCursor.execute(
                            "CREATE TABLE IF NOT EXISTS ELIGIBILITY_DETAILS(USER VARCHAR (20), AADHAR VARCHAR(14) "
                            "PRIMARY KEY, CROP VARCHAR(10), AGE VARCHAR(4), RAINFALL VARCHAR(10), DEBT VARCHAR(10), "
                            "SAVINGS VARCHAR(10), WEATHER VARCHAR(10), HARVESTING_MONTH VARCHAR(2), SCORE VARCHAR("
                            "4));")
                        myCursor.execute(
                            "INSERT INTO ELIGIBILITY_DETAILS VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL );",
                            tuple(data))
                        conn.commit()
                        conn.close()
                        st.write("Details submitted to the database.")

    # If login is not successful
    else:
        st.write("Please login first")
