# Assignment Info

COSI132A Information Retrieval Spring 2022 - Assignment 4 Building a simple Vector Space IR System


## Description

* This is documentation of the third coding assignment for course COSI 132A Information Retrieval. 
* This is a disjunctive matching search engine, i.e., a document must match at least one (non stopword) term in the query.
* This assignment aims to develop a toy search engine that empowers users to find news articles through ad hoc searching. 
  By typing in keywords or phrases, articles includes all the same token(s) will be extracted and displayed on the webpage. 
  This project uses the Flask framework to build a web server and application. 
  The web page templates developed through HTML provide a simple User Interface that enables users to interact with the backend system.
* The system should consist of two key components: 
	* An indexing module that constructs an inverted index, with term dictionary and postings lists for a corpus.
	* A run-time module that implements a Web UI for searching the corpus, returning a ranked result list and presenting selected documents.


## Getting Started

### Dependencies

* Python 3.9 is required, and dependencies include JSON, Flask, DateTime, re, and typing. Besides, a NoSQL database, which is MongoDB, has been used for persisting inverted index and documents in the local environment. 

### Dataset

* A test of 16 JSON format documents from TREC Washington Post Corpus (WAPO) were used for system diagnosis.

### Installing

* All dependencies are listed in the requirement.txt file. Anyone who wishes to run this project on a local environment could install these packages using the command: <code>pip3 install -r requirements.txt </code>.
  Other than the dependencies, the user shall also install or upgrade the MongoDB compress to the latest version.


### Executing program

* Before running this project in the terminal, the user shall be aware that all the required packages listed above shall be properly installed or upgraded to the latest version. 
  The user shall follow two steps to run this program in the local environment. 
  Firstly, the user can use the <code> python hw4.py --build --test </code> command in the terminal to create the inverted index and document length collection. 
  Then run <code> python hw4.py --run --test </code> in the environment and type http://127.0.0.1:5000/ in browser to view the web application.
  

## Difficulties encountered in this assignment

* The ranking mechanism is based on the cosine similarity scores for all documents that match a query via TF-IDF. The top 8 documents shall be returned.
* This assignment is based on a partial result of Assignment 3. It inherited the text_processing file from the previous assignment.
* In the result page, the IDF scores for each of the terms in the query shall be displayed. To the left of each title in the result list, display its cosine similarity score in 
square brackets. A list of the query terms that were found in this document shall be included in the snippet.


## Authors

* The lecturer of COSI132A provided the home template. 
* The rest functions and templates were created by Wanyue Xiao independently.

## Testing
#### System with default text processor

* ""(searching for an empty search query)
 No matching result shall be returned. The system throws a warning by displaying “0 document(s) has been returned. Please use another keyword.” on the screen.
 No terms shall be displayed regarding Valid Terms, Ignoring Terms, and Unknown Search Terms.

* “ ” (searching for whitespace character)
 No matching result shall be returned. The system throws a warning by displaying “0 document(s) has been returned. Please use another keyword.” on the screen.
 No terms shall be displayed regarding Valid Terms, Ignoring Terms, and Unknown Search Terms.

* “a” (searching for character “a”)
 No matching result shall be returned. The system throws a warning by displaying “0 document(s) has been returned. Please use another keyword.” on the screen.
 The term "a" shall be listed in Ignoring Terms. No terms shall be displayed with respect to Valid Terms and Unknown Search Terms. The next page button shall not be displayed.

* "The part” (searching for bi-gram)
 The system throws a sentence by displaying “7 document(s) have been returned.” on the screen.
 The term "the" shall be listed in Ignoring Terms. 
 The term "part" with its IDF score shall be listed in Valid Terms. 
 The next page button shall be displayed. 

* “The new token in the test” (searching for the sentence “The new token in the test”)
 The system throws a sentence by displaying “8 document(s) have been returned.” on the screen.
 The term "the" and "in" shall be listed in Ignoring Terms. 
 The term "new" and "test" with their IDF scores shall be listed in Valid Terms. 
 The term "token" shall be listed in Unknown search term. 
 The next page button shall be displayed.