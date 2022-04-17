# Assignment Info
COSI132A Information Retrieval Spring 2022 - Assignment 5 Building a IR System with Elasticsearch (ES) and Embedding

## Description
* This is documentation of the fifth coding assignment for course COSI 132A Information Retrieval. 
* A TREC 2018 core corpus subset and twelve TREC topics with relevance judgments will be used for system development and result evaluation.
* In this assignment, we will provide example code for:
  - Populating and querying a corpus using ES
  - Implementing NDCG (normalized discounted cumulative gain) evaluation metric
  - Experimenting with “semantic” indexing and searching using fastText and BERT
* The system consists of several key components: 
  - Displaying the similarity score between the search query and each of the documents
  - Indexing the corpus into ES with default standard analyzer and English analyzer for the text fields
  - Integrate ES into the Flask service for interactive search. Beside the traditional lexical search, the system should also allow the user to select the text representation to use for search
  - Evaluate the performance of 12 provided TREC query pairs using NDCG. For each of the 12 query pairs, produce a result table along with a brief analysis

## Dataset
* A larger subset of TREC 2018 core corpus that has already been processed. Specifically, each document has the following fields:

| variable     | Description                                                      |
| ------------ | ---------------------------------------------------------------- |
| doc_id       | original document id from the jsonline file                      |
| title        | article title                                                    |
| author       | article authors                                                  |
| content      | main article content (HTML tags removed)                         |
| date         | publish date in the format “yyyy/MM/dd”                          |
| annotation   | annotation for its relevance to a topic                          |
| ft_vector    | fastText embedding of the content                                |
| sbert_vector | Sentence BERT embedding of the content                           |

**Notes**:
* For the annotation field, the value is stored as the format of topic_id-relevance. The relevance can be either 0, 1 or 2, which represents irrelevant, relevant or very relevant.
* The topic id can be mapped to the query pairs in the file pa5_data/pa5_queries.json.
* If the annotation field is empty, it can be considered that this document is irrelevant to any topics.

## Getting Started
### 1. Dependencies
* This repository is Python-based, and **Python 3.9** is recommended. The dependencies include JSON, Flask, DateTime, re, elasticsearch, elasticsearch-dsl, sentence-transformers, flask, numpy, and pyzmq. 

### 2. First-time Running
All dependencies are listed in the requirement.txt file. Anyone who wishes to run this project on a local environment could install these packages using the command: <code>pip3 install -r requirements.txt </code>. Before running this project in the terminal, the user shall be aware that all the required packages listed above shall be properly installed or upgraded to the latest version. 

### 3. Download all Necessary Datasets
The data directory should contain the following files.
```
data
├── pa5_queries.json
├── ideal_relevance.json
├── subset_wapo_50k_sbert_ft_filtered.jl
├── topics2018.xml
└── wiki-news-300d-1M-subword.vec
```
You need to download the pretrained fastText embedding on wiki news and put it into data folder. You can click this [link](https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M-subword.vec.zip) to download. 

### 4. Activate Elasticsearch Basics
You can  can click this [link](https://www.elastic.co/downloads/past-releases#elasticsearch) to download ES. Make sure you are choosing Elasticsearch 7.10.2. 
To start the ES engine:
```shell script
cd elasticsearch-7.10.2/
./bin/elasticsearch
```
To test your ES is running, open http://localhost:9200/ in your browser. You should be able to see the health status of your ES instance with the version number, the name and more. **Note that you should keep ES running in the backend while you are building and using your IR system.**

### 5. Activate Embedding Service
Load fasttext embeddings that are trained on wiki news. Each embedding has 300 dimensions
```shell script
python -m embedding_service.server --embedding fasttext  --model pa5_data/wiki-news-300d-1M-subword.vec
```

Load sentence BERT embeddings that are trained on msmarco. Each embedding has 768 dimensions
```shell script
python -m embedding_service.server --embedding sbert  --model msmarco-distilbert-base-v3
```

Load wapo docs into the index called "wapo_docs_50k"
```shell script
python load_es_index.py --index_name wapo_docs_50k --wapo_path pa5_data/subset_wapo_50k_sbert_ft_filtered.jl
```
**Note that you should keep all these shells running in the backend while you are building and using your IR system.**


### 6. Running the Programs
The user shall follow the following step to run this program in the local environment. Run <code> python hw5.py </code> in the environment and type http://127.0.0.1:5000/ in browser to view the web application. 

- For Evaluation: 
    Change ```TOPIC_ID``` to the topic ID you want to evaluate.
    ```shell
    sh scirpts.sh
    ```

## Evaluation Table for the 12 Example Queries

|            | Keywords        | Natural Language |    |            | Keywords        | Natural Language | 
| ---------- | --------------- | ---------------- |    | ---------- | --------------- | ---------------- |
| Vector     | 0.84557         | 0.88460          |    | Vector     | 0.84557         | 0.88460          |
| Rerank     | 0.85000         | 0.75000          |    | Rerank     | 0.85000         | 0.75000          |


|            | Keywords        | Natural Language |    |            | Keywords        | Natural Language | 
| ---------- | --------------- | ---------------- |    | ---------- | --------------- | ---------------- |
| Vector     | 0.84557         | 0.88460          |    | Vector     | 0.84557         | 0.88460          |
| Rerank     | 0.85000         | 0.75000          |    | Rerank     | 0.85000         | 0.75000          |


|            | Keywords        | Natural Language |    |            | Keywords        | Natural Language | 
| ---------- | --------------- | ---------------- |    | ---------- | --------------- | ---------------- |
| Vector     | 0.84557         | 0.88460          |    | Vector     | 0.84557         | 0.88460          |
| Rerank     | 0.85000         | 0.75000          |    | Rerank     | 0.85000         | 0.75000          |


|            | Keywords        | Natural Language |    |            | Keywords        | Natural Language | 
| ---------- | --------------- | ---------------- |    | ---------- | --------------- | ---------------- |
| Vector     | 0.84557         | 0.88460          |    | Vector     | 0.84557         | 0.88460          |
| Rerank     | 0.85000         | 0.75000          |    | Rerank     | 0.85000         | 0.75000          |


|            | Keywords        | Natural Language |    |            | Keywords        | Natural Language | 
| ---------- | --------------- | ---------------- |    | ---------- | --------------- | ---------------- |
| Vector     | 0.84557         | 0.88460          |    | Vector     | 0.84557         | 0.88460          |
| Rerank     | 0.85000         | 0.75000          |    | Rerank     | 0.85000         | 0.75000          |


|            | Keywords        | Natural Language |    |            | Keywords        | Natural Language | 
| ---------- | --------------- | ---------------- |    | ---------- | --------------- | ---------------- |
| Vector     | 0.84557         | 0.88460          |    | Vector     | 0.84557         | 0.88460          |
| Rerank     | 0.85000         | 0.75000          |    | Rerank     | 0.85000         | 0.75000          |



## Difficulties encountered in this assignment
* Spent at least 3 hours understanding the basic operations of ElasticSearch
* Spent 12 hours in total on this assignment
* Despite the 3 to 5 hours spent on learning and implementing elastic search in the Python environment, most of the time was spent on debugging
* It is confusing how to calculate the NDCG score. The formula indicates that the denominator shall be the DCG score of the ideal relevance for the search query. However, it is confusing about the concept of getting ideal relevance. Shall it be the sorted result of the actual relevance list or the top k elements from the gold relevance list extracted from the ideal_relevance.json file?


## Authors
* The lecturer of COSI132A provided the home template. 
* The rest functions and templates were created by Wanyue Xiao independently.

## Testing
###  TREC Topic for Evaluation: tunnel injury disaster
The evaluation for the key words of the topic #363 will be used for testing and demonstration.

```xml
<top>
<num> Number: 363 </num>
<title>
transportation tunnel disasters 
</title>
<desc> Description:
What disasters have occurred in tunnels used for transportation?  
</desc>
<narr> Narrative
A relevant document identifies a disaster in a tunnel used for trains, motor vehicles, or people. Wind tunnels and tunnels used for wiring, sewage, water, oil, etc. are not relevant. The cause of the problem may be fire, earthquake, flood, or explosion and can be accidental or planned. Documents that discuss tunnel disasters occurring during construction of a tunnel are relevant if lives were threatened.  
</narr>
</top>
```

#### Output
In the following table, the evaluation scores for the example query with different combinations have been displayed. The number of the retrieved document was 20. 
| Evaluation | BM25+Standard Analyzer| BM25+English Analyzer | SentenceBERT+English Analyzer | Rerank SentenceBERT+English Analyzer |
| ---------- | ----------------------| --------------------- | ----------------------------- | ------------------------------------ |
| AP         | 0.84557               | 0.88460               | 0.72598                       | 0.75250                              |
| Precision  | 0.85000               | 0.75000               | 0.70000                       | 0.75000                              |
| NDCG@20    | 0.79794               | 0.76928               | 0.66862                       | 0.63404                              |
