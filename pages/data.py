# import libraries
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import re
from datetime import datetime


def ChangeWidgetFontSize(wgt_txt, wch_font_size = '16px'):
    
    ''' Function to change fontsize in any widget'''

    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == |wgt_txt|) 
                        { elements[i].style.fontSize='""" + wch_font_size + """';} } </script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)


# define function to upload file & select text and date columns
def select_data():

    ''' Function to upload file and select text & date columns '''

    # with open('style.css') as f:
    #     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)    

    # create a file uploader
    file = st.file_uploader("Upload a CSV file", type="csv")
    ChangeWidgetFontSize("Upload a CSV file")

    # display the uploaded file
    if file is not None:
        df = pd.read_csv(file)
        st.markdown(f'<p class"result>Uploaded data:</p>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

        # multiselect text columns
        text_cols = st.multiselect("Select text column(s)", options=df.columns.tolist())
        ChangeWidgetFontSize("Select text column(s)")
       
        # select date column
        cols = [col.replace('_', ' ').lower() for col in df.columns]
        date_idx = [cols.index(i) for i in cols if "date" in i]
        date_cols = df.columns[date_idx]
        date_col = st.selectbox("Select date column with date format YYYY-MM-DD", options=date_cols)
        ChangeWidgetFontSize("Select date column with date format YYYY-MM-DD")

        if text_cols:
            # merge multiple columns using "|"
            df['Text'] = df[text_cols].apply(lambda row: ' | '.join(row.values.astype(str)), axis=1)

            if date_col:
                st.write("Selected columns:")
                
                # extract Year, Month, Date
                df['DateTime'] = pd.to_datetime(df[date_cols[0]], format="%Y-%m-%d")
                df['Date'] = [d.date() for d in df['DateTime']]
                df['Year'] = [d.year for d in df['Date']]
                df['Month'] = [d.month for d in df['Date']]
                
                # output final dataframe
                final_df = df[['Text', 'Date', 'Year', 'Month']]
    
            return final_df


def app():
    st.markdown(f'''
                <p>
                Semantic text analytics is a technique that analyze the meaning and context of words and phrases in unstructured text data to derive insights and information. 
                It uses natural language processing (NLP) and machine learning (ML) techniques to identify patterns and relationships in text data, and to extract relevant information from it.
                </p>

                <p>
                One common use case for semantic text analytics is in topic modeling, where it is used to identify and categorize topics and themes in large volumes of text data.
                This can be useful for organizations that need to analyze large volumes of documents to identify key topics and trends.
                </p>
                ''', 
                unsafe_allow_html=True)
    st.divider()
    st.session_state.df = select_data()
    if st.session_state.df is None:
        pass
    else:
        st.dataframe(st.session_state.df, use_container_width=True)


if __name__ == "__main__":
    app()
