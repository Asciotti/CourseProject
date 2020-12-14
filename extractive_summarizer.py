#!/usr/bin/env python
# coding: utf-8
import nltk

nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

def extractive_summary(text):
    pass
 
def read_article(file_name):
    file = open(file_name, "r")
    filedata = file.readlines()
    article = sent_tokenize(filedata[0])
    sentences = []

    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    # sentences.pop()  # last sentence is actually fine
    
    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)
 
def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(file_name, query, top_n=5, add_weights_flag=True):
    stop_words = stopwords.words('english')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences =  read_article(file_name)

    # If the results are already small just return
    if len(sentences) < 6:
        sentences = [ " ".join(x) for x in sentences]
        return " ".join(sentences)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)

    # Add weighting towards the query word to increase likelihood sentence w/ that word is chosen
    weights = {}
    for i, sent in enumerate(sentences):
        if query in sent and add_weights_flag:
            weights[i] = 1
        else:
            weights[i] = 0.0001

    scores = nx.pagerank(sentence_similarity_graph, personalization=weights)
    # nx.draw(sentence_similarity_graph, with_labels=True, font_weight='bold')
    # plt.show();plt.pause(0)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    # print ("Indexes of top ranked_sentence order are ")
    # for s in ranked_sentence:
    #     print (s)
    for i in range(top_n):
      summarize_text.append(" ".join(ranked_sentence[i][1]))

    # # Step 5 - Offcourse, output the summarize texr
    # print("\n\n\nSummarize Text: \n", " ".join(summarize_text))
    summarize_text = " ".join(summarize_text)
    return summarize_text

if __name__ == '__main__':
    print(generate_summary( "para_idx_data/179.txt", 'annotations', 3))