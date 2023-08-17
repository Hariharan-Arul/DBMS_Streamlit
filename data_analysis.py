import streamlit as st
import pandas as pd
import sqlite3
from sklearn import tree
from sklearn.preprocessing import LabelEncoder


def home():
    st.markdown("# Welcome to our Dropout-Predictor")
    st.sidebar.markdown("# Home🏠")

    st.subheader("Enter Your Details in the forms Page of our Website to predict your interest in going to the institution")

    st.write("In this Session you will build a website that takes values from the user,stores the value in a database and uses the data to predict whether the user will be regular in going to institution.")

    st.success("👈Choose the Forms option in the sidebar to predict your result.")
    st.success("👈Choose the Display Stats option to visualize the response of different users.")


def forms():
    st.markdown("# Form📑")
    st.sidebar.markdown("# Form📑")

    skl_type = st.selectbox("Choose your school type:",["Academic","Vocational"])

    interest = st.selectbox("Select How interested are you in going to college?",["Less Interested","Very Interested","Uncertain"])

    residence = st.selectbox("Select your Residence area:",["Urban","Rural"])

    parent_salary = st.number_input("Enter your parent's salary",0)

    percent = st.slider("Enter your Percentage}:",0,100)

    form_submit = st.button("Predict my Values")

    if form_submit:
        conn = sqlite3.connect("data.db")

        df = pd.read_sql_query("SELECT * FROM user_data",conn)

        enc = LabelEncoder()

        for i in df.columns:
            if df[i].dtype == "O":
                df[i] = enc.fit_transform(df[i])

        X = df.iloc[:,:-1]
        Y = df.iloc[:,-1]

        model = tree.DecisionTreeClassifier()
        model = model.fit(X,Y)

        user_data = [skl_type,interest,residence,parent_salary,percent]

        new_df = pd.DataFrame([user_data])

        for i in new_df.columns:
            if new_df[i].dtype == "O":
                new_df[i] = enc.fit_transform(new_df[i])

        predict = model.predict(new_df[new_df.columns])

        if predict == 1:
            st.balloons()
            st.success("You are Expected to maintain attendance and continue in the school")
        
        else:
            st.snow()
            st.error("You are not Expected to maintain attendance and hence you have chances of droping out")

        try:
            cursor = conn.cursor()
            cursor.execute(f'''INSERT INTO user_data VALUES ('{skl_type}','{interest}','{residence}',{parent_salary},{percent},{predict[0]})''')
            conn.commit()
        except Exception as e:
            print(e)

def student():
    
    st.markdown("# Student_Insertion")
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
        conn = sqlite3.connect("mydb.db")
        df = pd.read_sql_query("SELECT * FROM Student",conn)


        

        
        try:
            
            
            cursor = conn.cursor()
            


            cursor.execute(f'''INSERT INTO Student VALUES ({dropout_rates},{boys},{girls},'{state}',{age_group},'{disability}')''')
            
            conn.commit()
        except Exception as e:
            print(e)
def student_delete():
    
    st.markdown("# Student_Deletion")

    value1 = st.selectbox("Enter the columns name:",["dropout_rate","boys","girls","state","age_group","disability"])
    value2 = st.text_input("Enter the colmuns value:")

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        form_submit = st.button("SUBMIT VALUES")
    with col5:
        form_reset = st.button("RESET VALUES")
    
    if form_submit:
        conn = sqlite3.connect("mydb.db")
        df = pd.read_sql_query("SELECT * FROM Student",conn)
        

            

            
        try:
                
                
            cursor = conn.cursor()
            cursor.execute(f'''DELETE FROM Student WHERE {value1} = '{value2}' ''')
                


            
                
            conn.commit()
        except Exception as e:
            print(e)
    
    
def student_update():
    st.markdown("# Student_Updation")
    
    value1 = st.selectbox("Enter the columns name:",["dropout_rate","boys","girls","state","age_group","disability"])
    
    value2 = st.text_input("Enter the colmuns value:")

    value3 = st.selectbox("Enter the condition's name:",["dropout_rate","boys","girls","state","age_group","disability"])

    value4 = st.text_input("Enter the condition's value:")
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        form_submit = st.button("SUBMIT VALUES")
    with col5:
        form_reset = st.button("RESET VALUES")
    if form_submit:
        
        conn = sqlite3.connect("mydb.db")
        df = pd.read_sql_query("SELECT * FROM Student",conn)
        
       
    
        try:
            cursor = conn.cursor()
            
                
                
            
            
            cursor.execute(f'''UPDATE Student
                               SET {value1} = '{value2}'
                               WHERE {value3} = '{value4}' ''')
            


            conn.commit()
            
        
        except Exception as e:
            print(e)
            

def data_display():
    st.markdown("# Display Stats📈")
    st.sidebar.markdown("# Display Stats📈")

    conn = sqlite3.connect("data.db")
    conn1 = sqlite3.connect("mydb.db")
    
    
    df = pd.read_sql_query("SELECT * FROM user_data",conn)
    
    df1 = pd.read_sql_query("SELECT * FROM Student",conn1)
    

    
    st.subheader("Analysis table")
    st.dataframe(df)
    st.subheader("Student Table")
    st.dataframe(df1)
   

    st.subheader("BarChart1:")

    st.write("Correlation between resident area and Interest to Institution")

    st.bar_chart(df,y="parent_salary",x="will_go_to_college")

    st.subheader("BarChart2:")

    st.write("Correlation between dropout rates between boys and girls")

    st.bar_chart(df1,y="boys",x="girls")

    st.subheader("LineChart1:")

    st.write("Correlation between percentage and parent salary")

    st.line_chart(df,x="percentage",y="parent_salary")

    st.subheader("LineChart2:")

    st.write("Correlation between dropout rates and state")

    st.line_chart(df1,x="state",y="dropout_rate")

    

page_names_to_funcs = {
    "Home🏠": home,
    "Student_insert📑" : student,
    "Student_delete📑" : student_delete,
    "Student_update📑" : student_update,
    "Forms📑": forms,
    "Data Visualization📈": data_display,
    
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
