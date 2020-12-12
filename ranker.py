import math
import sys
import time
import metapy
import pytoml
import numpy as np
import random
from rank_bm25 import BM25Okapi
import os

def tokenizer(doc):
    # prepare the tokenizer;
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok = metapy.analyzers.LengthFilter(tok, min=2, max=50)
    tok = metapy.analyzers.LowercaseFilter(tok)
    tok = metapy.analyzers.Porter2Filter(tok)
    tok = metapy.analyzers.ListFilter(tok, "lemur-stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
    # set the content;
    tok.set_content(doc.content())
    # return tokenized document;
    return [token for token in tok]

def load_ranker(cfg_file,mu):
    """
    Use this function to return the Ranker object to evaluate, 
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    
    # parse the dataset file
    cfg_file = cfg_file.replace('\\', '/')
    path = cfg_file[:cfg_file.rfind("/")]
    data_files = set()
    corpus = []
    idx = []
    path_corpus = "%s/dataset-full-corpus.txt" % (path)
    print("Loading ranker ", path_corpus)

    with open(path_corpus, "r") as fh:
        for line in fh:
            line = line[:-1]
            _, file = line.split(" ")
            data_files.add(file)

    # get all the documents in the dataset and tokenize them accordingly;
    for i, file in enumerate(data_files):
        with open(os.path.join(path, file), "rb") as fh:
            data = fh.read().decode().strip()
            doc = metapy.index.Document()
            doc.content(data)
            res = tokenizer(doc)
            corpus.append(res)
            idx.append(file)

    return {
        "ranker": BM25Okapi(corpus),
        "idx": idx,
        "path": path,
    }

def scorer(ranker,query,top_k):
    results = ranker["ranker"].get_top_n(tokenizer(query), ranker["idx"], n=top_k)
    return results
    

if __name__ == '__main__':
  
    cfg = './para_idx_data/config.toml'
    with open(cfg,'r') as f:
        print(f.read())

    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    start_time = time.time()
    import ipdb; ipdb.set_trace()
    ranker = load_ranker(cfg,2500)


    query = metapy.index.Document()
    query.content('WordNet ontology')
    res = scorer(ranker,idx,query,10,0.34)
    print(res)

