import streamlit as st
import streamlit.components.v1 as components
from pages import data
from pages import analysis


def app():
    st.markdown(f'''
                <p>
                The purpose of visualizing topics over time is to analyze how topics and themes in a corpus of text data have evolved and changed over a specific period of time,
                thus gain insights into how opinion and awareness of a particular subject have changed 
                and identify key events or milestones that have influenced the subject.
                </p>
                ''', 
                unsafe_allow_html=True)
    st.divider()

    df = st.session_state.df

    # dropdown topic lists
    # menu = output_df['Name'].tolist()

    if st.button('Visualize Topic Over Time'):
        if df is None:
            st.write("Plese define data in Home tab")
        else:
            output_df, time_path = analysis.plot_topics(df, method="timeline")       
            st.write('The chart shows document similarity in 2D space.')
            image_file = open(time_path, "r")
            image = image_file.read()
            components.html(image, height=600)
            image = image_file.close()        
    

        # if st.selectbox("Select topic of interest", menu):
        #     data.ChangeWidgetFontSize("Select topic of interest")
        #     st.dataframe(output_df, use_container_width=True)
        
        

    #     output_df, time_path = analysis.semantic_cluster(df, method="timeline")
    #     st.write(output_df)
        
        # image_file = open(time_path, "r")
        # image = image_file.read()
        # components.html(image, height=600)
        # image = image_file.close()


    
    # new cell (new plot while maintaining the old ones)


if __name__ == "__main__":
    app()