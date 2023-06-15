import streamlit as st
import requests
import json
import pandas as pd
import datetime

st.set_page_config(layout="wide")

@st.cache_data
def callSparkModel(inputdata):

    url = "https://excel.uat.us.coherent.global/coherent/api/v3/folders/Spark FE Demos/services/loan-origination/Execute"

    payload = json.dumps({
       "request_data": {
          "inputs": {
            "Channel": inputdata['Channel'],
            "Dependants": inputdata['Dependants'],
            "DOB": inputdata['DOB'],
            "DurationOfLoan": inputdata['DurationOfLoan'],
            "Education": inputdata['Education'],
            "ExistingCustomer": inputdata['ExistingCustomer'],
            "Gender": inputdata['Gender'],
            "Home": inputdata['Home'],
            "Income": inputdata['Income'],
            "Living_Area": inputdata['Living_Area'],
            "LoanAmount": inputdata['LoanAmount'],
            "LoanStart": inputdata['LoanStart'],
            "NationalID": inputdata['NationalID'],
            "Nationality": inputdata['Nationality'],
            "Occupation": inputdata['Occupation']
          }
       },
        "request_meta": {
            "compiler_type": "Neuron",
        }
    })
    headers = {
       'Content-Type': 'application/json',
       'x-tenant-name': 'coherent',
       'SecretKey': '2277565c-9fad-4bf4-ad2b-1efe5748dd11'
    }


    response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)
    return response

#Start of UI
image_path = "coherent-logo.png"
st.image(image_path, caption="", width=32)

st.write("## Retail Lending - Credit Risk Evaluation and Pricing")

col21, col22, col23 = st.columns([12, 2, 32])

with col21:
  st.text("‎") 
  st.write("Applicant Details")
  with st.expander("**Loan Details**", expanded=True):
    LoanAmount = st.text_input("Loan Amount")
    LoanStart = st.date_input("Loan Start", datetime.date.today())
    DurationOfLoan = st.slider("Term (months)", 36, 240, (120))
  with st.expander("**Customer Details**"):
    ExistingCustomer = st.selectbox('Returning Customer', ['Yes', 'No'], index=0)
    dobdefault = datetime.date(1980, 1, 1)
    DOB = st.date_input("Date of Birth", dobdefault)
    Gender = option = st.radio("Gender", ("Male", "Female"), index=1)
    Nationality = option = st.radio("Nationality", ("Local", "Non-Local"), index=0)
    NationalID = st.text_input("National ID", 'E678912(3)')
    Dependants = st.selectbox('Dependents?', ['0', '1', '2+'], index=0)
    Education = st.selectbox('Highest Level of Education', ['Primary', 'Secondary', 'Graduate', 'University or above'], index=3)  
  with st.expander("**Occupation**"):
    Occupation = st.selectbox('Occupation', ['Finance', 'Student', 'Small business owner', 'Employed - Manufacturing', 'Employed - Agriculture', 'Employed - Travel', 'Employed - Telecom', 'Others'], index=0)
    Income = st.text_input("Annual Income", '100000')
  with st.expander("**Residence**"):
    Living_Area = st.selectbox('Area of Residence', ['Class A City', 'Class B City', 'Class C City', 'Class D City', 'Class E City'], index=0)
    Home = st.selectbox('Type of Building', ['Rental', 'Selfowned with mortgage', 'Selfowned without mortgage'], index=0)
  with st.expander("**Channel**"):
    Channel = st.selectbox('Distribution Channel', ['Agency', 'Branch'], index=0)  
  inputdata = {
    "Channel": Channel,
    "Dependants": Dependants,
    "DOB": DOB.strftime("%Y-%m-%d"),
    "DurationOfLoan": DurationOfLoan,
    "Education": Education,
    "ExistingCustomer": ExistingCustomer,
    "Gender": Gender,
    "Home": Home,
    "Income": Income,
    "Living_Area": Living_Area,
    "LoanAmount": LoanAmount,
    "LoanStart": LoanStart.strftime("%Y-%m-%d"),
    "NationalID": NationalID,
    "Nationality": Nationality,
    "Occupation": Occupation
  }   
  if st.button("Submit Application", type='primary'):    
    alldata = callSparkModel(inputdata)
    outputs = alldata.json()['response_data']['outputs']

with col22:
  st.text("‎") 

with col23:
  st.text("‎") 
  #API call 
  alldata = callSparkModel(inputdata)
  outputs = alldata.json()['response_data']['outputs']
  st.write("Illustration and Scoring")

  with st.expander("**Illustration**", expanded=True):
    st.markdown('***')
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col1:
      formatted_monthlypayment = "{:,.0f}".format(outputs['MonthlyLoanPayment'])
      st.metric(label='Monthly Payment', value=formatted_monthlypayment)
    with col2:  
      formatted_totalpayment = "{:,.0f}".format(outputs['Total_Monthly_Payment'])
      st.metric(label='Total Payment', value=formatted_totalpayment)
    with col3:  
      formatted_interest = "{:.0f}%".format(outputs['LoanRate']*100)
      st.metric(label='Interest Rate', value=formatted_interest)
    with col4:  
      formatted_totalinterest = "{:,.0f}".format(outputs['Total_Interest_Payment'])
      st.metric(label='Total Interest Paid', value=formatted_totalinterest)
    st.markdown('***')
    df_illus = pd.DataFrame(outputs['Amortization'])
    st.write(df_illus)
  # with st.expander("**Scoring Details**"):
  #   st.error('Under construction')
  # with st.expander("**API Results**"):  
  #   st.write(outputs)


