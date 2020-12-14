
# EducationalWeb

# Setup

The following instructions have been tested with Python3.7 on Windows.

1. You should have ElasticSearch installed and running 

   Ubuntu - https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html
   Windows - https://www.elastic.co/guide/en/elasticsearch/reference/current/windows.html
   MacOs - https://www.elastic.co/guide/en/elasticsearch/reference/current/brew.html

2. Create the index in ElasticSearch by running `python create_es_index.py` from `EducationalWeb/`

3. Download tfidf_outputs.zip from here -- https://drive.google.com/file/d/19ia7CqaHnW3KKxASbnfs2clqRIgdTFiw/view?usp=sharing
   
   Unzip the file and place the folder under `EducationalWeb/static`

4. Download cs410.zip from here -- https://drive.google.com/file/d/1Xiw9oSavOOeJsy_SIiIxPf4aqsuyuuh6/view?usp=sharing
   
   Unzip the file and place the folder under `EducationalWeb/pdf.js/static/slides/`
   
5. Download lemur-stopwords.txt from here -- https://raw.githubusercontent.com/meta-toolkit/meta/master/data/lemur-stopwords.txt

   `lemur-stopwords.txt` needs to be placed under `EducationalWeb/`
   
6. From `EducationalWeb/pdf.js/build/generic/web` , run the following command: `gulp server`

7. In another terminal, setup your python environment (requires python 3.7 - I recommend making a clean venv/conda environment) by running `pip install -r requirements.txt`.

8. Run `python app.py` from `EducationalWeb/`

9. The site should be available at http://localhost:8096/

10. Run through the examples (at the end of the video tutorial) to see the usage and benefits of the summarization.


# Motivation:

The "Explanation" feature available in the EducationalWeb system can be used to provide an explanation of the highlighted words on a given slide. The issue is the returned explanations can be too lengthy and not all that specific to the query word. One could improve these explanations by providing a more targeted, concise summary of the raw explanation return. This can be done in a few manners, I chose to look at extractive methods (using shallow NLP) and abstractive methods (using deep pre-trained NN based language models). Extractive summarization can be thought of as restating the most useful or "main" points in a document. Abstract summarization can be thought of as paraphrasing the document itself in a (typically) more concise way [1].

# Concepts of explanation "finding"
The general process to discover explanations is as follows - this is essentially a document retrieval problem given a query.
1. Preprocess corpus for future ranking on query words
2. Extract the query word from the webpage
3. With query, corpus (processed), and ranking algo (BM25 in our case), determine most likely documents
(In our case documents were provided in the repo already, they appear to be headers of chapters)
4. Take top-k (1 in our case) most likely documents
5. Given the best matched document, then run summarization on the content
6. Return the summarized "explanation" to the user

# Extractive Summary Process (ref [2])
Provided into the extractive summary process is a preprocessed document that contains a list of lists for each sentene then each word in said sentence. In the extractive summary process we utilize a vector space method "encoding" of each sentence. Each element of the vector is the count of a single unique word/"token". The similarity measure between each sentence with every other sentence is computed via cosine similarity. This gives us an MxM matrix (M=# sentences), the similarity matrix. The pagerank algorithm [5] can be used to return probabilities of "landing" on each page (sentence in our case). The sentences with the highest probabilities are most likely to occur, and are thus the most "useful". We add some additional weighting to sentences which contain the query word itself - to try to improve the likelihood of seeing the word in the explanations given.


You can run an example of abstractive summarization by running the following:

`python extractive_summarizer.py`

It will run a summary of the below input data (selected document) which resulted from the query `annotations`.


> In this section, we're going to continue our discussion of web search, particularly focusing on how to utilize links between pages to improve search. In the previous section, we talked about how to create a large index on using MapReduce on GFS. Now that we have our index, we want to see how we can improve ranking of pages on the web. Of course, standard IR models can be applied here; in fact, they are important building blocks for supporting web search, but they aren't sufficient for the following reasons. First, on the web we tend to have very different information needs. For example, people might search for a web page or entry page-this is different from the traditional library search where people are primarily interested in collecting literature information. These types of queries are often called navigational queries, where the purpose is to navigate into a particular targeted page. For such queries, we might benefit from using link information. For example, navigational queries could be facebook or yahoo finance. The user is simply trying to get to those pages without explicitly typing in the URL in the address bar of the browser. Secondly, web documents have much more information than pure text; there is hierarchical organization and annotations such as the page layout, title, or hyperlinks to other pages. These features provide an opportunity to use extra context information of the document to improve scoring. Finally, information quality greatly varies. All this means we have to consider many factors to improve the standard ranking algorithm, giving us a more robust way to rank the pages and making it more difficult for spammers to manipulate one signal to improve a single page's ranking. 


You should see:

>Secondly, web documents have much more information than pure text; there is hierarchical organization and annotations such as the page layout, title, or hyperlinks to other pages. First, on the web we tend to have very different information needs. In this section, we're going to continue our discussion of web search, particularly focusing on how to utilize links between pages to improve search.

One might notice that without any postprocessing, the resultant summary can be devoid of any context or fluidity.


# Abstractive Summary Process (ref [3])
Abstractive summary utilizes a pre-trained deep NN from HuggingFace [4]. We utilize the T5 language network to perform summarization. The T5 network has an accompanying tokenizer that ingests the raw document (sentences). We have picked the T5-small model (and tokenizer) rather than the medium/large models due to computation time (we are running locally on CPUs). The larger models 1) are more accurate and 2) have the ability to process longer documents. The small is limited to 512 tokens, which roughly translates to 500 words or ~20-30 sentences. Without going into the details ([3] can provide more information) of the generational configuration, we choose to utilize beam search to improve the summary in addition to constraining the length of the summary returned to [50,150] tokens.

You can run the following to see an example of an abstract summary (note the output might be slightly different from yours).

Input text same as for extractive summarization example.

`python abstract_summarizer.py`



>we're going to continue our discussion of web search. in the previous section, we talked about how to create a large index on using MapReduce on gfs. we want to see how we can improve ranking of pages on the web. the standard
IR models can be applied here, but they aren't sufficient for the following reasons.

Given the network we used, it was not possible to add any weighting/favoring towards generating sentences with the query word.

# Demo

The demo is provided via the video tutorial found here:

The slide used to demo can be found here (given the app is running and you can connnect to it:
http://localhost:8096/next_slide/cs-410/86/cs-410----13_week-12----02_week-12-lessons----05_12-5-contextual-text-mining-contextual-probabilistic-latent-semantic-analysis_TM-42-cplsa.txt----slide2.pdf

The word example we will go through is for `Coverage` in the above slides.

If you don't want to go through the video. Go through the installation above such that you can see the slides.  
Go to those specific set of slides (click on link).  
Highlight "coverage" in the bottom right corner and hit the box with the graduation cap on it in the top right. If you hover over the boxes it shoulds say "Explain selected text"
You should see the unmodified "Explanation"  

Now go to your text editor and open `app.py`. Modify `SUMMARIZER=""` to `SUMMARIZER="EXTRACT"`.  
Hit save file. Wait a few seconds for the page to reload.  
Highlight "coverage" again and hit the explain button. See the extractive summarized "Explanation".

Now go to your text editor and open `app.py`. Modify `SUMMARIZER="EXTRACT"` to `SUMMARIZER="ABSTRACT"`.   
Hit save file. Wait a few seconds for the page to reload.  
Highlight "coverage" again and hit the explain button. See the abstract summarized "Explanation".


[1] https://www.quora.com/Natural-Language-Processing-What-is-the-difference-between-extractive-and-abstractive-summarization  
[2] https://towardsdatascience.com/understand-text-summarization-and-create-your-own-summarizer-in-python-b26a9f09fc70  
[3] https://huggingface.co/blog/how-to-generate  
[4] https://huggingface.co/  
[5] https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf  
