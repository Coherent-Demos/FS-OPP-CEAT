import streamlit as st
import requests
import json
import pandas as pd
import datetime

st.set_page_config(layout="wide")

def callSparkModel(inputdata):

    url = "https://excel.uat.jp.coherent.global/nttdata/api/v3/folders/SIP/services/Sales Incentive Report Generator/Execute"

    payload = json.dumps({
       "request_data": {
          "inputs": inputdata
        },
        "request_meta": {
            "compiler_type": "Neuron",
            "call_purpose": "Digital Front End",
        }
    })
    headers = {
       'Content-Type': 'application/json',
       'x-tenant-name': 'nttdata',
       'Authorization': bearerToken
    }


    response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)
    return response

# Function to create a button linking to the URL
def create_button_link(url, text):
    return f'<a href="{url}" target="_blank"><button style="border: 2px solid rgb(107, 50, 177);border-radius: 8px;color: rgb(107, 50, 177);font-weight: 700;background: transparent;padding: 8px 16px; width: 100%">{text}</button></a>'

def highlight_columns(s, columns):
    styles = ['' for _ in range(len(s))]

    for col in columns:
        if col in s.name:
            styles = ['background-color: lightgreen' if i == s.name.index else '' for i in range(len(s))]

    return styles

inputdata = {"EXEC_1": {}, "ALL_EXECS":{}}
SparkErrors = []

#Start of UI
image_path = "ceat-logo.png"
st.image(image_path, caption="", width=120)

st.write("## Incentive Calculation")

col21, col22, col23 = st.columns([12, 2, 32])

with col21:
  st.text("‎") 
  st.write("Inputs")
  with st.form("DC Form"):

    with st.expander("**Files**"):
      inputdata["Service_Actuals_Data"] = st.text_input("Actuals Data", "2024Q1 - Actual Sales Performance")
      inputdata["Service_Budget_Data"] = st.text_input("Budget Data", "2022-24 - CEAT Budget")
      inputdata["Service_Calc_Model"] = st.text_input("Calc Model", "Incentive Calculator")
      inputdata["Service_KPIs_and_Criteria"] = st.text_input("KPIs and Criteria", "2023 - KPIs & Incentive Criteria")
    
    with st.expander("**Employee**"):
      inputdata["Exec1_Employee_ID"] = st.text_input("Enter Employee ID", 636718)

    with st.expander("**Evaluation Period**"):
      inputdata["Quarter"] = st.text_input("Quarter", "Q2")
      inputdata["Year"] = st.text_input("Year", 2022)

    with st.expander("**Set Filename for Reports**"):
      inputdata["EXEC_1"]["ReportName"] = st.text_input("Individual Report", "EXEC_1")
      inputdata["ALL_EXECS"]["ReportName"] = st.text_input("Group Report", "ALL_EXECS")

    with st.expander("**API Key**"):
      bearerToken = st.text_input("API Token", "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJwaUppeFpjYTJEZzVBZ0FneUZxUzU5d0RKV09lMC03VENBbUpZWktFTXRrIn0.eyJleHAiOjE3MDU0MDEzMTUsImlhdCI6MTcwNTM5NDExNSwiYXV0aF90aW1lIjoxNzA1Mzk0MTE0LCJqdGkiOiI2NzgzNjc2ZS1kYTUwLTQ3OWEtYWNhZS1kYjJmNTAzOGVmZGMiLCJpc3MiOiJodHRwczovL2tleWNsb2FrLnVhdC5qcC5jb2hlcmVudC5nbG9iYWwvYXV0aC9yZWFsbXMvbnR0ZGF0YSIsImF1ZCI6InByb2R1Y3QtZmFjdG9yeSIsInN1YiI6ImNlMWNlYzgxLWFjZDQtNGMwYi05NDNmLWRjMTE5Mzg2MTRiZiIsInR5cCI6IkJlYXJlciIsImF6cCI6InByb2R1Y3QtZmFjdG9yeSIsIm5vbmNlIjoiNjhhNDQ2ODEtMjBlMi00YzI1LWFlNGQtMGEwMjY3YjkyYmMwIiwic2Vzc2lvbl9zdGF0ZSI6IjVmMTkxNjZiLTI0MjQtNGZmZi1hM2U4LTQzZDcyYjlmMTczYyIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9tb2RlbGluZy1jZW50ZXIuZGV2LmNvaGVyZW50Lmdsb2JhbCIsImh0dHBzOi8vbW9kZWxpbmctY2VudGVyLnVzLmNvaGVyZW50Lmdsb2JhbCIsImh0dHBzOi8vc2EudWF0LmpwLmNvaGVyZW50Lmdsb2JhbCIsImh0dHBzOi8vc2Euc3RhZ2luZy5jb2hlcmVudC5nbG9iYWwiLCJodHRwczovL3Byb2R1Y3RmYWN0b3J5LnVhdC5qcC5jb2hlcmVudC5nbG9iYWwiLCJodHRwczovL3NwYXJrLnVhdC5qcC5jb2hlcmVudC5nbG9iYWwiLCJodHRwczovL3NwYXJrLXVzZXItbWFuYWdlci51YXQuanAuY29oZXJlbnQuZ2xvYmFsIiwiaHR0cHM6Ly9tb2RlbGluZy1jZW50ZXIuc3RhZ2luZy5jb2hlcmVudC5nbG9iYWwiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIl19LCJzY29wZSI6Im9wZW5pZCBvZmZsaW5lX2FjY2VzcyBzcGFyayBwcm9maWxlIiwic2lkIjoiNWYxOTE2NmItMjQyNC00ZmZmLWEzZTgtNDNkNzJiOWYxNzNjIiwibmFtZSI6Ik1hcmsgQmFuYXJpYSIsImdyb3VwcyI6WyJ1c2VyOnBmIl0sInJlYWxtIjoibnR0ZGF0YSIsInByZWZlcnJlZF91c2VybmFtZSI6Im1hcmsuYmFuYXJpYUBjb2hlcmVudC5nbG9iYWwiLCJnaXZlbl9uYW1lIjoiTWFyayIsImZhbWlseV9uYW1lIjoiQmFuYXJpYSIsInVzZXJfY3JlYXRlZF90aW1lc3RhbXAiOjE3MDUwNTI5NzkzNTMsInJlbGF0aW9uIjoicGFydG5lciJ9.eLRV_GLn27jLyrMbPnlo9SGzBJduS95q25qHi-Ncb946Zf6BQSN3gXxJFQ0KVg0TPSNVpAfEUDPckQrYgg2z_tbKIbXalk2wNWe7HrRtzDQQnHrvWlg39il9ZMj4m-HTnEfQ_2aZtTW4B3RKYu-0ytYSiYzOokRoAML5gQwJEK-CqQtW3FAV8XShsJ_YPAs9dsOQua97hXScIRLUa-DAuk5iGtlHIYxifRCkNRvxPyU6rGENCqXrzAyHftOuD6ltgO63g_V5DBDzJSHsdA0eB6QG5dNhn6WTvVYXF9YKIU-h0O30yfrekmtc1wBdhwdotGzhLig1eGuO5d5fKgIeBA")

    GenerateIncentiveReports_clicked = st.form_submit_button("Submit", use_container_width=True)
    if GenerateIncentiveReports_clicked:
      CallData = callSparkModel(inputdata)
      Outputs = CallData.json()['response_data']['outputs']
      SparkErrors = CallData.json()['response_data']['errors']

    # Add the style tag to change button color to blue
    st.markdown("""
    <style>
        .stButton button { /* Adjust the class name according to your button's class */
            background-color: #5169E7 !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)
  st.write("Powered by Coherent")

with col22:
  st.text("‎") 

with col23:
  st.text("‎")

  st.write("Outputs")
  ERRORBOX = st.empty()
  with st.expander("Spark Model", expanded=True):
    st.markdown('[https://excel.uat.jp.coherent.global/nttdata/api/v3/folders/SIP/services/Sales%20Incentive%20Report%20Generator/Execute](https://excel.uat.jp.coherent.global/nttdata/api/v3/folders/SIP/services/Sales%20Incentive%20Report%20Generator/Execute)')

  tab1, tab2 = st.tabs(["Individual Incentive By KPI", "All Execs Incentive By KPI"])

  with tab1:

    with st.expander("" , expanded=True):
      col41, col42, col43 = st.columns([2,1,1])
      with col41:
        EMPLOYEE = st.empty()
      with col42:
        INCENTIVE = st.empty()
      with col43:
        INCENTIVE_ADJ = st.empty()
      st.markdown('***')
      st.write("**Breakdown By KPI**")
      INDIV_BY_KPI = st.empty()
      st.markdown('***')
      st.write("**Download Report**")
      INDIV_REPORT = st.empty()
  
  with tab2:
    with st.expander("**All Results**" , expanded=True):
      col41, col42, col43, col44 = st.columns([1,1,1,1])
      with col41:
        TOTAL_INCENTIVES = st.empty()
      with col42:
        BUDGET_PER_EXEC = st.empty()
      with col43:
        ADJ_FACTOR = st.empty()
      with col44:
        ADJUSTED_TOTAL = st.empty()
      st.markdown('***')
      st.write("**Breakdown By KPI**")
      ALL_BY_KPI = st.empty()
      st.markdown('***')
      st.write("**Download Report**")
      ALL_REPORT = st.empty()


  CallData = callSparkModel(inputdata)
  Outputs = CallData.json()['response_data']['outputs']
  SparkErrors = CallData.json()['response_data']['errors']
  
  if not SparkErrors:
      # # Keys to retain
      # keys_to_retain = [
      #     "PUPSA",
      #     "Total bonuses (SV of RB + IB)",
      #     "Base Value (SV of SA)",
      #     "SV1",
      #     "ReB",
      #     "TB",
      #     "SV",
      #     "LAPR clawback",
      #     "Final Value"
      # ]

      # # Create a new dictionary containing only the desired keys
      # trimmed_data = {key: Outputs[key] for key in keys_to_retain}

    INDIV_BY_KPI_DF = Outputs["Exec1_Incentive_byKPI"]
    INDIV_BY_KPI.dataframe(INDIV_BY_KPI_DF,use_container_width=True)

    ALL_BY_KPI_DF = Outputs["All_Incentive_byKPI"]
    ALL_BY_KPI.dataframe(ALL_BY_KPI_DF,use_container_width=True)

    NAMEValue = Outputs["Exec1_Name"]
    ROLEValue = Outputs["Exec1_Role"]
    INCENTIVE_ADJValue = "{:,.0f}".format(Outputs["Exec1_Incentive_Adj"])
    INCENTIVEValue = "{:,.0f}".format(Outputs["Exec1_Incentive_unAdj"])

    EMPLOYEE.metric(label=ROLEValue, value=NAMEValue)
    INCENTIVE.metric(label='Incentive', value=INCENTIVEValue)
    INCENTIVE_ADJ.metric(label='Incentive (Adjusted)', value=INCENTIVE_ADJValue)
    
    TOTAL_INCENTIVESValue = "{:,.0f}".format(Outputs["All_Incentive_unAdj"])
    BUDGET_PER_EXECValue = "{:,.0f}".format(Outputs["Budget_perExec"])
    ADJ_FACTORValue = "{:,.2f}".format(Outputs["Adj_Factor"])
    ADJUSTED_TOTALValue = "{:,.0f}".format(Outputs["All_Incentive_Adj"])
    
    TOTAL_INCENTIVES.metric(label="Total Incentives", value=TOTAL_INCENTIVESValue)
    BUDGET_PER_EXEC.metric(label="Budget Per Executive", value=BUDGET_PER_EXECValue)
    ADJ_FACTOR.metric(label="Adjustment Factor", value=ADJ_FACTORValue)
    ADJUSTED_TOTAL.metric(label="Adjusted Total Incentives", value=ADJUSTED_TOTALValue)

    INDIV_REPORT.markdown(create_button_link(Outputs["EXEC_1"]["PDFUrl"], "Individual Incentive Report"), unsafe_allow_html=True)
    ALL_REPORT.markdown(create_button_link(Outputs["ALL_EXECS"]["PDFUrl"], "Full Incentive Report"), unsafe_allow_html=True)
    # DownloadSV.markdown(create_button_link(Outputs["SV AND PUPSA OUTPUT"]["PDFUrl"], "SV & PUP SA Report"), unsafe_allow_html=True)
    # DownloadFinalValue.markdown(create_button_link(Outputs["VAL @ AT DATE OF DEATH"]["PDFUrl"], "Val @ Date of Death Report"), unsafe_allow_html=True)
  
  else:
    error_messages = [error["message"] for error in SparkErrors if error["message"] != "#VALUE!"]
    if error_messages:
        ERRORBOX.error("\n ".join(error_messages))
