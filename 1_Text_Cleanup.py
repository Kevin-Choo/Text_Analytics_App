pip install spacy -q

# import dependencies
import streamlit as st
import pandas as pd
import neattext as nt
from neattext import TextCleaner 

# for file name and file encoding
import base64
import time

# for stemming and tokenization
import nltk

# for lemmatization
import spacy
import en_core_web_sm

# create an nltk word tokenizer
nltk_wt = nltk.word_tokenize

# create an nltk sentence tokenizer
nltk_st = nltk.sent_tokenize

# create a variable to capture time as string
timestr = time.strftime("%Y%m%d-%H%M%S")


# load nltk's porter stemmer algorithm
ps = nltk.porter.PorterStemmer()
# perform stemming using nltk
def basic_stemming(text, stemmer=ps):
    text = ' '.join([stemmer.stem(word) for word in text.split()])
    return text


def get_data(filename):
	raw_txt = filename.read().decode('utf-8')
	return raw_txt


def download_text(raw_txt):
	b64 = base64.b64encode(raw_txt.encode()).decode()
	new_name = "Modified_data_{}_.txt".format(timestr)
	# st.markdown("DOWNLOAD FILE")
	href = f'<a href="data:file/txt;base64,{b64}" download="{new_name}">CLICK HERE TO DOWNLOAD</a>'
	st.markdown(href,unsafe_allow_html=True)


# load spacy's English model
# nlp = spacy.load('en_core_web_sm')
nlp = en_core_web_sm.load()
# lemamtization using spaCy
def spacy_lemmatize(text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text


# stopword removal
def remove_stopwords(text, is_lower_case=False, stopwords=None):
    if not stopwords:
        stopwords = nltk.corpus.stopwords.words('english')
    tokens = nltk.word_tokenize(text)
    tokens = [token.strip() for token in tokens]
    
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopwords]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopwords]
    
    filtered_text = ' '.join(filtered_tokens)    
    return filtered_text



def main():
	# st.title("Text Cleanup Section")

	# menu = ["Text Cleaup", "Basic Text Analytics", "Advance Text Analytics", "About"]
	# choice = st.sidebar.selectbox("Menu", menu)

	# if choice == "Text Cleaup":
	if "txt" not in st.session_state:
		# st.subheader("Get your text clean up here for analysis")
		st.title("Text Cleanup Section")
		txt = st.file_uploader("Upload File", type=['txt'])
		lower_case = st.sidebar.checkbox("Lower Case")
		clean_html_tags = st.sidebar.checkbox("HTML Tags")
		clean_urls = st.sidebar.checkbox("URLs")
		clean_userhandles = st.sidebar.checkbox("Twitter Userhandles")
		clean_multiple_spaces = st.sidebar.checkbox("Multiple Spaces")
		clean_stopwords = st.sidebar.checkbox("Stopwords")
		clean_punctuations = st.sidebar.checkbox("Puntuations")
		clean_emails = st.sidebar.checkbox("Emails")
		clean_special_chars = st.sidebar.checkbox("Special Characters")
		clean_numbers = st.sidebar.checkbox("Numbers")
		clean_terms_in_brackets = st.sidebar.checkbox("Terms In Brackets")
		fix_contractions = st.sidebar.checkbox("Fix Contractions")
		clean_accents = st.sidebar.checkbox("Accented Words")
		find_stem = st.sidebar.checkbox("Stemming")
		find_lemma = st.sidebar.checkbox("Lemmatization")
		words_tokenization = st.sidebar.checkbox("Words Tokenization")
		sentences_tokenization = st.sidebar.checkbox("Sentences Tokenization")



		if txt is not None:
			# displaying txt file detail such as file size
			txt_detail = {"Filename":txt.name, "Filesize":txt.size, "Filetype":txt.type}
			st.write(txt_detail)
			# make raw_txt load only once by using get_data() and only call it once
			# raw_txt = txt.read().decode('utf-8')
			raw_txt = get_data(txt)
			col1, col2 = st.columns(2)

			with col1:
				with st.expander("Original Data"):	
					st.write(raw_txt)

            
			with col2:
				with st.expander("Modified Data"):
					# txt_df = nt.TextFrame(text=raw_txt)
					tc = TextCleaner
					tc.text = raw_txt
                    
					if lower_case:
						raw_txt = raw_txt.lower()

					if clean_html_tags:
						raw_txt = nt.remove_html_tags(raw_txt)

					if clean_urls:
						raw_txt = nt.remove_urls(raw_txt)

					if clean_userhandles:
						raw_txt = nt.remove_userhandles(raw_txt)

					if clean_multiple_spaces:
						raw_txt = nt.remove_multiple_spaces(raw_txt)

					if clean_stopwords:
						raw_txt = nt.remove_stopwords(raw_txt)

					if clean_punctuations:
						raw_txt = nt.remove_punctuations(raw_txt)

					if clean_emails:
						raw_txt = nt.remove_emails(raw_txt)

					if clean_special_chars:
						raw_txt = nt.remove_special_characters(raw_txt)

					if clean_numbers:
						raw_txt = nt.remove_numbers(raw_txt)

					if clean_terms_in_brackets:
						raw_txt = nt.remove_terms_in_bracket(raw_txt)

					if fix_contractions:
						raw_txt = nt.fix_contractions(raw_txt)

					if clean_accents:
						raw_txt = nt.remove_accents(raw_txt)

					if find_stem:
						raw_txt = basic_stemming(raw_txt, stemmer=ps)

					if find_lemma:
						raw_txt = spacy_lemmatize(raw_txt)

					if words_tokenization:
						raw_txt = nltk_wt(raw_txt)

					if sentences_tokenization:
						raw_txt = nltk_st(raw_txt)

					st.write(raw_txt)

					download_text(raw_txt)


	


if __name__ == '__main__':
	main()
