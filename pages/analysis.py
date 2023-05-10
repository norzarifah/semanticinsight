from re import M
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import pickle
import nltk
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP


def semantic_analysis(df):

    nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words('english')

    sentences = df['Text'].tolist()

    vectorizer_model = CountVectorizer(stop_words=stopwords, ngram_range=(1,2))
    
    model_name = "all-MiniLM-L6-v2"
    sentence_model = SentenceTransformer(model_name)

    embeddings = sentence_model.encode(sentences, convert_to_tensor=True)
    
    umap_model = UMAP(n_neighbors=15, n_components=10, min_dist=0.0, metric='cosine')

    topic_model = BERTopic(embedding_model=sentence_model,
                           umap_model=umap_model,
                           top_n_words=3,
                           min_topic_size=5,
                           verbose=True,
                           vectorizer_model=vectorizer_model)
    topics, probs = topic_model.fit_transform(sentences)

    # save model and embeddings to models folder
    model_path = "model/output_model.pkl"
    pickle.dump(embeddings, open(model_path, "wb"))
    embeddings_path = "model/embeddings.pkl"
    pickle.dump(embeddings, open(embeddings_path, "wb"))

    return embeddings, topic_model


def plot_topics(df, method=None):

    sentences = df['Text'].tolist()
    
    # load existing model and embedgins if exist
    model_path = "models/model_output"
    embeddings_path = "models/embeddings.pkl"
    if os.path.exists(model_path) and os.path.exists(embeddings_path):
        topic_model = pickle.load(open(model_path, 'rb'))
        embeddings = pickle.load(open(embeddings_path, 'rb'))
        print("Successfully uploaded existing models")
    else:
        embeddings, topic_model = semantic_analysis(df)
        print("Successfully generate new models")


    output_df = topic_model.get_topic_info()
    reduced_embeddings = UMAP(n_neighbors=10, n_components=2, min_dist=0.0, metric='cosine').fit_transform(embeddings)

    if method == "analysis":
        fig = topic_model.visualize_documents(sentences, reduced_embeddings=reduced_embeddings)
        path = os.path.join("images", "cluster_output.html")
        fig.write_html(path)
    else:
        timeline = df["Date"].apply(lambda x: pd.to_datetime(x, format="%Y-%m-%d")).to_list()
        topics_over_time = topic_model.topics_over_time(sentences, timeline, nr_bins=10)
        fig = topic_model.visualize_topics_over_time(topics_over_time)
        path = os.path.join("images", "timeline_output.html")
        fig.write_html(path)
    
    return output_df, path


def app():
    st.markdown(f'''
                <p>
                The purpose of semantic clustering is to group similar documents together based on content and meaning, rather than just keywords or metadata.
                This can help users to quickly identify relevant information and find related documents, even if they use different terminology or phrasing.
                </p>

                <p>
                Semantic searching, on the other hand, involves using natural language processing (NLP) and machine learning (ML) techniques to analyze the meaning and context
                of a user's query, and to retrieve relevant results from a large corpus of unstructured text data.
                </p>
                ''', 
                unsafe_allow_html=True)
    st.divider()

    # retrieve the data from session state
    # df = st.session_state.df

    if st.button('Run Semantic Clustering'):
        if st.session_state.df is None:
            st.write("Plese define data in Home tab")
        else:
            output_df, cluster_path = plot_topics(st.session_state.df, method="analysis")               
            st.dataframe(output_df, use_container_width=True)
            st.write("Topic -1 refers to all outlier documents and are typically ignored.")
            st.markdown("***")
            st.write('The chart shows document similarity in 2D space.')
            image_file = open(cluster_path, "r")
            image = image_file.read()
            components.html(image, height=600)
            image = image_file.close()


if __name__ == "__main__":
    app()
