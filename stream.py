from GoogleSearchForSEO import extract_seo
import streamlit as st
import pandas as pd
import os
import base64
import time

results = []
def last_round(mp):
    if mp != "":
        st.write("✅ That's Great! You have selected the following path: ", main_path)
        st.write("✅ Now, let's scrape The data!")

    else:
        pass

main_path = ""
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; padding-bottom:30px;">
    <img src="data:image/png;base64,{}" width="100" height="100" style="margin-left: 10px; margin-top:25px">
    <h1 style="text-align: center; margin-right:95px;">Metaviz Pro SEO Tool</h1>
</div>
""".format(base64.b64encode(open("metaviz_logo.png", "rb").read()).decode()), unsafe_allow_html=True)
st.header("Drive SEO with precise URL, Email extraction", divider=True)
choice = st.selectbox("How You Wanna Scrape Data", ['Single Keyword', "By File"])
if choice == 'Single Keyword':
    keyword = st.text_input("Enter Your Keyword", placeholder="i.e. CBD Oil Capsules")
    file = st.text_input("Enter File Name", placeholder="i.e. data.csv")
    if file != "":
        main_path = file
        last_round(main_path)
        with st.spinner("Processing... Please wait."):
            extract_seo("Single Keyword", keyword, main_path)
        time.sleep(5)
        st.success("Scraping completed successfully!")
    with open(main_path, "rb") as f:
        st.download_button("Download CSV", f, main_path, mime="text/csv")         
elif choice == 'By File':
    file_path = st.file_uploader("Upload Your File", type=["csv"])
    if file_path is not None:
        df = pd.read_csv(file_path)
        column = st.selectbox("Select Column", options=df.columns.tolist())
        file = st.text_input("Enter File Name", placeholder="i.e. data.csv")
        if file != "":
            main_path = file
            last_round(main_path)
            with st.spinner("Processing... Please wait."):
                extract_seo("Single Keyword", df[column], main_path)
            time.sleep(5)
            st.success("Scraping completed successfully!")    
    with open(main_path, "rb") as f:
        st.download_button("Download CSV", f, main_path, mime="text/csv")  

    


