import os
import nltk
import spacy

def prequisitives():
    # nlp = spacy.load("en_core_web_sm")

    current_dir = os.path.dirname(os.path.abspath(__file__))

    nltk_data_path = os.path.join(current_dir, 'nltk_data')

    nltk.data.path.insert(0, nltk_data_path)

    nltk.download('punkt', download_dir=nltk_data_path)
    nltk.download('averaged_perceptron_tagger', download_dir=nltk_data_path)
    nltk.download('wordnet', download_dir=nltk_data_path)
    nltk.download('omw-1.4', download_dir=nltk_data_path)