import streamlit as st
import requests
import json
import pandas as pd
import datetime

st.set_page_config(layout="wide")

def callSparkModel(inputdata):

    url = "https://excel.uat.us.coherent.global/coherent/api/v3/folders/HCL/services/Results File - Phase 1 Surr & PUPs/Execute"

    payload = json.dumps({
       "request_data": {
          "inputs": {
            "Policy Number": inputdata["Policy Number"],
            "Policy Data File": inputdata["Policy Data File"],
            "Bonus Data File": inputdata["Bonus Data File"]
          }
       },
        "request_meta": {
            "compiler_type": "Neuron",
            "call_purpose": "Digital Front End",
        }
    })
    headers = {
       'Content-Type': 'application/json',
       'x-tenant-name': 'coherent',
       'SecretKey': '2277565c-9fad-4bf4-ad2b-1efe5748dd11'
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

inputdata = {}
SparkErrors = []

#Start of UI
image_path = "hcl-logo.png"
st.image(image_path, caption="", width=80)

st.write("## Surr & PUP calculations")

col21, col22, col23 = st.columns([12, 2, 32])

with col21:
  st.text("‎") 
  st.write("Inputs")
  with st.form("DC Form"):
    inputdata["Policy Number"] = st.text_input("Policy Number", "Sample A")
    inputdata["Policy Data File"] = st.text_input("Policy Data Filename", "Policy Data - 202212")
    inputdata["Bonus Data File"] = st.text_input("Bonus Data Filename", "Bonus Data - Phase 1 bonus rates")

    PolicySearch_clicked = st.form_submit_button("Submit", use_container_width=True)
    if PolicySearch_clicked:
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
    st.markdown('[https://spark.uat.us.coherent.global/coherent/products/HCL/Results%20File%20-%20Phase%201%20Surr%20&%20PUPs/apiTester/test](https://spark.uat.us.coherent.global/coherent/products/HCL/Results%20File%20-%20Phase%201%20Surr%20&%20PUPs/apiTester/test)')

  with st.expander("**" + inputdata["Policy Number"] + " Results**" , expanded=True):
    col41, col42, col43, col44, col45, col46 = st.columns([1,1,1,1,1,1])
    with col41:
      Pupsa = st.empty()
    with col42:
      SV1 = st.empty()
    with col43:
      TB = st.empty()
    with col44:
      ReB = st.empty()
    with col45:
      LAPR = st.empty()
    with col46:
      FinalValue = st.empty()
    st.markdown('***')
    TableBreakdown = st.empty()
    st.markdown('***')
    st.write("Download Reports")
    col31, col32, col33 = st.columns([1,1,1])
    with col31:
      st.text("‎")
    with col32:
      DownloadSV = st.empty()
    with col33:
      DownloadFinalValue = st.empty()
      
  with st.expander("**All Policy Data**", expanded=True):
    st.markdown('***')
    PolicyTable = st.empty()

    st.markdown('***')
    st.write("Download Reports")
    col51, col52 = st.columns([1,1])
    with col51:
      st.text("‎")
    with col52:      DownloadPolicy = st.empty()


    CallData = callSparkModel(inputdata)
    Outputs = CallData.json()['response_data']['outputs']
    SparkErrors = CallData.json()['response_data']['errors']
    
    if not SparkErrors:
      # Keys to retain
      keys_to_retain = [
          "PUPSA",
          "Total bonuses (SV of RB + IB)",
          "Base Value (SV of SA)",
          "SV1",
          "ReB",
          "TB",
          "SV",
          "LAPR clawback",
          "Final Value"
      ]

      # Create a new dictionary containing only the desired keys
      trimmed_data = {key: Outputs[key] for key in keys_to_retain}

      # TableBreakdownDf = pd.DataFrame(trimmed_data.items(), columns=['Parameter', 'Value'])
      TableBreakdownDf = Outputs["Policy_Details"]
      TableBreakdown.dataframe(TableBreakdownDf,use_container_width=True)
      
      columns_to_highlight = ["PUPSA", "Total bonuses (SV of RB + IB)", "Base Value (SV of SA)", "SV1", "ReB", "TB", "SV",  "LAPR clawback", "Final Value"]
      PolicyTableDf = pd.DataFrame(Outputs["Results_PolicyWise"])
      styled_df = PolicyTableDf.style.apply(highlight_columns, columns=columns_to_highlight, axis=0)
      PolicyTable.dataframe(styled_df,use_container_width=True)

      PupsaValue = "{:,.0f}".format(Outputs["PUPSA"])
      SV1Value = "{:,.0f}".format(Outputs["SV1"])
      TBValue = "{:,.0f}".format(Outputs["TB"])
      ReBValue = "{:,.0f}".format(Outputs["ReB"])
      LAPRValue = "{:,.0f}".format(Outputs["LAPR clawback"])
      FinalValueValue = "{:,.0f}".format(Outputs["Final Value"])

      Pupsa.metric(label='Paid-up SA', value=PupsaValue)
      SV1.metric(label='Total Value (Base Value + Total Bonuses)', value=SV1Value)
      TB.metric(label='Terminal Bonus', value=TBValue)
      ReB.metric(label='Reorganisation Bonus', value=ReBValue)
      LAPR.metric(label='LAPR Clawback', value=LAPRValue)
      FinalValue.metric(label='Final Value', value=FinalValueValue)

      DownloadPolicy.markdown(create_button_link(Outputs["POLICY DATA"]["PDFUrl"], "SV & PUPSA Report for All " + inputdata["Policy Data File"]), unsafe_allow_html=True)
      DownloadSV.markdown(create_button_link(Outputs["SV AND PUPSA OUTPUT"]["PDFUrl"], "SV & PUP SA Report"), unsafe_allow_html=True)
      DownloadFinalValue.markdown(create_button_link(Outputs["VAL @ AT DATE OF DEATH"]["PDFUrl"], "Val @ Date of Death Report"), unsafe_allow_html=True)
    
    else:
      error_messages = [error["message"] for error in SparkErrors if error["message"] != "#VALUE!"]
      if error_messages:
          ERRORBOX.error("\n ".join(error_messages))
