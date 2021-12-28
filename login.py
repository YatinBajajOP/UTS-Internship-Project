import mysql.connector
import streamlit as st
import SessionState
import pandas as pd

def app(session_state):
    conn = mysql.connector.connect(host="localhost", user="root", passwd="12345", database="UTS")
    myCursor = conn.cursor()
    myCursor.execute("CREATE TABLE IF NOT EXISTS CUSTOMER_DETAILS(USER VARCHAR(20) PRIMARY KEY, PASS VARCHAR(20), "
                     "NAME VARCHAR(20), PHONE_NUM VARCHAR(10), AADHAR VARCHAR(14), ADMIN VARCHAR(4));")

    # Python code to implement
    # Vigenere Cipher

    # This function generates the
    # key in a cyclic manner until
    # it's length isn't equal to
    # the length of original text
    def generateKey(string, key):
        key = list(key)
        if len(string) == len(key):
            return key
        else:
            for i in range(len(string) - len(key)):
                key.append(key[i % len(key)])
        return "".join(key)

    # This function returns the
    # encrypted text generated
    # with the help of the key
    def cipherText(string, key):
        cipher_text = []
        for i in range(len(string)):
            x = (ord(string[i]) +
                 ord(key[i])) % 26
            x += ord('A')
            cipher_text.append(chr(x))
        return "".join(cipher_text)

    # This function decrypts the
    # encrypted text and returns
    # the original text
    # def originalText(cipher_text, key):
    #     orig_text = []
    #     for i in range(len(cipher_text)):
    #         x = (ord(cipher_text[i]) -
    #              ord(key[i]) + 26) % 26
    #         x += ord('A')
    #         orig_text.append(chr(x))
    #     return "".join(orig_text)

    # Login page
    # session_state = SessionState.get(user= None, passwd = None)
    st.title("Welcome to the login section")
    user = str(st.text_input("Enter username:", value=""))
    session_state.user = user
    passwd = str(st.text_input("Enter password:", type="password", value=""))
    session_state.passwd = passwd

    encrypt_key_string = "UTSEncryptionKey"
    encrypt_key = generateKey(passwd, encrypt_key_string)
    cipher_pass = cipherText(passwd, encrypt_key)

    data = (user, cipher_pass)
    session_state = SessionState.get(Z=False)

    Z = st.button("Login")
    if Z:
        session_state.Z = True

    if session_state.Z:
        try:
            if session_state.count == 0:
                myCursor.execute("SELECT * FROM CUSTOMER_DETAILS WHERE user=%s AND pass=%s", data)
                res = myCursor.fetchone()
                session_state.res = res
                if session_state.res is not None:
                    session_state.count = 1 
             
            if session_state.res is not None:
                st.write("Login successful")
                session_state.login_state = True
                data1 = [[session_state.res[0], session_state.res[2], session_state.res[3], session_state.res[4], session_state.res[5]]]
                df = pd.DataFrame(data1, columns=["USER", "NAME", "PHONE NO.", "AADHAR", "ADMIN"], index=[""])
                st.write(df.T)

                if session_state.res[5] == "NO":
                    st.write("Logged in as Customer")
                else:
                    st.write("Logged in as Admin")

            else:
                st.write("Login unsuccessful")
                session_state.login_state = False
        except:
            st.write("error in code")

    log = st.button("Logout")
    if log:
        session_state.Z = False
        session_state.login_state = False
        session_state.count = 0
        session_state.res = None
        session_state.user = ''
        session_state.passwd = ''

        st.write("logout successful")

    conn.close()
