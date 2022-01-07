import streamlit as st
import sqlite3
import pandas as pd
from sqlite3 import Error

st.set_page_config(page_title='DB APP', page_icon=':smiley')

def get_fullschema(conn):
    schema = conn.cursor().execute("""SELECT SQL FROM sqlite_master where type ='table';""").fetchall()
    schema = ["\n".join(i) for i in schema]
    schema = "\n".join(schema)
    return schema

st.title("Computer Store SQL Database")

uploaded_file = st.file_uploader("Upload Database", type='db')
submit_file = st.button("Upload")


            
with st.expander(label="Database Query Interface"):
    query = st.text_area(label="Insert Query")
    submit_qry = st.button(label="Submit")
    if submit_qry:
        st.text("Query Used")
        st.code(query, language='SQL')
        conn = sqlite3.connect("tmp.db")
        try:
            df = pd.read_sql(query, conn)
            st.text("Query Return")
            st.dataframe(data=df)
        except Exception as e:
            print(e)
            try:
                conn.cursor().execute(query)
                conn.commit()
                st.text("Query Executed Successfully")
            except Error as e:
                st.code(e)
        conn.close()

if submit_file:
    if uploaded_file is not None:
        file_open = open("tmp.db", 'wb')
        file_open.write(uploaded_file.getvalue())
        file_open.close()

with st.expander(label="Full Schema"):
    conn = sqlite3.connect("tmp.db")            
    full_schema = get_fullschema(conn)
    st.code(str(full_schema), language='SQL')
    conn.close()
    
        

with open("tmp.db", 'rb') as tmp_db:
    download_db = st.download_button(data=tmp_db, label="Download DB", file_name="new_database.db")