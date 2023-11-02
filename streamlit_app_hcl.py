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

inputdata = {}

#Start of UI
image_path = "coherent-logo.png"
st.image(image_path, caption="", width=32)

st.write("## Policy Report Generation")

col21, col22, col23 = st.columns([12, 2, 32])

with col21:
  st.text("‎") 
  st.write("Enter Policy Data Source")
  with st.form("DC Form"):
    inputdata["Policy Number"] = st.text_input("Policy Number", "Sample A")
    inputdata["Policy Data File"] = st.text_input("Policy Data Filename", "Policy Data - 202212")
    inputdata["Bonus Data File"] = st.text_input("Bonus Data Filename", "Bonus Data - Phase 1 bonus rates")
    PolicySearch_clicked = st.form_submit_button("Submit", use_container_width=True)
    if PolicySearch_clicked:
      CallData = callSparkModel(inputdata)
      Outputs = CallData.json()['response_data']['outputs']

with col22:
  st.text("‎") 

with col23:
  st.text("‎")

  st.write("Results")
  with st.expander("**Results**", expanded=True):
    col41, col42, col43 = st.columns([1,1,1])
    with col41:
      Pupsa = st.empty()
    with col42:
      Bonuses = st.empty()
    with col43:
      FinalValue = st.empty()
    st.markdown('***')
    TableBreakdown = st.empty()
    st.markdown('***')
    st.write("Download Reports")
    col31, col32, col33 = st.columns([1,1,1])
    with col31:
      DownloadPolicy = st.empty()
    with col32:
      DownloadSV = st.empty()
    with col33:
      DownloadFinalValue = st.empty()
      
  with st.expander("**All Policy Data**", expanded=True):
    st.markdown('***')
    PolicyTable = st.empty()


    CallData = callSparkModel(inputdata)
    Outputs = CallData.json()['response_data']['outputs']

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

    TableBreakdownDf = pd.DataFrame(trimmed_data.items(), columns=['Parameter', 'Value'])
    TableBreakdown.dataframe(TableBreakdownDf,use_container_width=True)
    
    PolicyTableDf = pd.DataFrame(Outputs["Results_PolicyWise"])
    PolicyTable.dataframe(PolicyTableDf,use_container_width=True)

    PupsaValue = "{:,.2f}".format(Outputs["PUPSA"])
    BonusesValue = "{:,.2f}".format(Outputs["Total bonuses (SV of RB + IB)"])
    FinalValueValue = "{:,.2f}".format(Outputs["Final Value"])

    Pupsa.metric(label='PUPSA', value=PupsaValue)
    Bonuses.metric(label='Total bonuses', value=BonusesValue)
    FinalValue.metric(label='Final Value', value=FinalValueValue)

    DownloadPolicy.markdown(create_button_link(Outputs["POLICY DATA"]["PDFUrl"], "Download Policy Report"), unsafe_allow_html=True)
    DownloadSV.markdown(create_button_link(Outputs["SV AND PUPSA OUTPUT"]["PDFUrl"], "Download SV & PUPSA"), unsafe_allow_html=True)
    DownloadFinalValue.markdown(create_button_link(Outputs["VAL @ AT DATE OF DEATH"]["PDFUrl"], "Download Final Value Report"), unsafe_allow_html=True)
