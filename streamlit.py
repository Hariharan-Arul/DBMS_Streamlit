import streamlit as st
import pandas as pd
import sqlite3
from sklearn import tree
from sklearn.preprocessing import LabelEncoder

def home():
    st.markdown("# Welcome to our page")
    st.sidebar.markdown("# Home🏠")

    st.subheader("Enter Your Details in the forms Page of our Website to enter the values into the table")

    st.write("In this Session you will build a website that takes values from the user,stores the value in a database")

    st.success("👈Choose the Forms option in the sidebar to do the task.")
    st.success("👈Choose the Display Stats option to visualize the response of different users.")


def student():
    
    st.markdown("# Student")
    st.sidebar.markdown("# Enter data into students")

    dropout_rates = st.slider("Enter The Dropout Rate :",0.00,100.00)

    boys = st.slider("Enter The Dropout Rate of Boys :",0.00,100.00)

    girls = st.slider("Enter The Dropout Rate of Girls :",0.00,100.00)

    state = st.selectbox("Enter the State :",["Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"])

    age_group = st.number_input("Enter the Age Group :", value = 0)

    disability = st.radio("Select the disability :",["Growth Defect","Malnutrition","Visually Impaired","Dylexia","ADHD","NONE"])

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        form_submit = st.button("SUBMIT VALUES")
    with col5:
        form_reset = st.button("RESET VALUES")


    if form_submit:
        


        

        
        try:
            conn = sqlite3.connect("mydb.db")
            
            cursor = conn.cursor()
            


            cursor.execute(f'''INSERT INTO Student VALUES ({dropout_rates},{boys},{girls},'{state}',{age_group},'{disability}')''')
            df = pd.read_sql_query("SELECT * FROM user_data",conn)
            conn.commit()
            
                
                
        except Exception as e:
            print(e)
        st.markdown("# Display Stats📈")
        st.sidebar.markdown("# Display Stats📈")

        conn = sqlite3.connect("mydb.db")
        st.subheader("School Table")

        df2 = pd.read_sql_query("SELECT * FROM School",conn)

        st.dataframe(df2)
        st.write('\t',dropout_rates,'\t','\t',boys,'\t','\t',girls,'\t','\t',state,'\t','\t',age_group,'\t','\t',disability,'\t')
        

def school():
    
    st.markdown("# School")
    st.sidebar.markdown("# Enter data into school")

    student_id = st.text_input("Enter the Student ID : ")

    reason = st.text_input("Enter the Reason : ")

    type_of_school = st.radio("Select the type of school :" ,["Private School","Government School"])

    acad_perf = st.slider("Enter the Academic Performaance :",0.00,100.00)

    disability = st.radio("Select the Disability :" ,["Growth Defect","Malnutrition","Visually Impaired","Dylexia","ADHD","NONE"])

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        form_submit = st.button("SUBMIT VALUES")
    with col5:
        form_reset = st.button("RESET VALUES")

    if form_submit:
        st.write(student_id)
        try:
            conn = sqlite3.connect("mydb.db")
            
            cursor = conn.cursor()
            
            cursor.execute(f'''INSERT INTO School VALUES ('{student_id}','{reason}','{type_of_school}',{acad_perf},'{disability}')''')
            df = pd.read_sql_query("SELECT * FROM user_data",conn)
            conn.commit()
            
                
                
        except Exception as e:
            print(e)

        st.markdown("# Display Stats📈")
        st.sidebar.markdown("# Display Stats📈")

        conn = sqlite3.connect("mydb.db")

        st.subheader("Student table")

        df1 = pd.read_sql_query("SELECT * FROM Student",conn)

        st.dataframe(df1)
        st.write('\t',student_id,'\t','\t',reason,'\t','\t',type_of_school,'\t','\t',acad_perf,'\t','\t',disability,'\t')

    

   

    

        
    
def data_display():
    st.markdown("# Display Stats📈")
    st.sidebar.markdown("# Display Stats📈")

    conn = sqlite3.connect("mydb.db")

    st.subheader("Student table")

    df1 = pd.read_sql_query("SELECT * FROM Student",conn)

    st.dataframe(df1)

    

   

    

    st.subheader("School Table")

    df2 = pd.read_sql_query("SELECT * FROM School",conn)

    st.dataframe(df2)

    

   
    


page_names_to_funcs = {
    "Home🏠": home,
    "STUDENT ": student,
    "SCHOOL" : school,
    "Data📈": data_display
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
