# Assignment Info

COSI132A Information Retrieval Spring 2022 - Assignment 3 Building a simple boolean retrieval system supporting conjunctive (“AND”) queries over terms


## Description

* This is documentation of the first coding assignment for course COSI 132A Information Retrieval. 
* This assignment aims to develop a toy search engine that empowers users to find news articles through ad hoc searching. 
  By typing in keywords or phrases, articles includes all the same token(s) will be extracted and displayed on the webpage. 
  This project uses the Flask framework to build a web server and application. 
  The web page templates developed through HTML provide a simple User Interface that enables users to interact with the backend system.
* The system allows user to choose two types of processing techniques. 
  The default text processor uses the NLTK built-in word_tokenizer for sentence segmentation. Then, the system lowercase each individual corpus and stemming it by using the 
  PorterStemmer(). The other type is custom processor. The differences are the expansion of stop words and acronym recognization. 


## Getting Started

### Dependencies

* Python 3.9 is required, and dependencies include JSON, Flask, DateTime, re, and typing. Besides, a NoSQL database, which is MongoDB, has been used for persisting inverted index and documents in the local environment. 

### Dataset

* A test 12 JSON format documents from TREC Washington Post Corpus (WAPO) were used for system diagnosis.

### Installing

* All dependencies are listed in the requirement.txt file. Anyone who wishes to run this project on a local environment could install these packages using the command: <code>pip3 install -r requirements.txt </code>.
  Other than the dependencies, the user shall also install or upgrade the MongoDB compress to the latest version.


### Executing program

* Before running this project in the terminal, the user shall be aware that all the required packages listed above shall be properly installed or upgraded to the latest version. 
  The user shall follow two steps to run this program in the local environment. 
  Firstly, the user can use the <code> python hw3.py --build </code> command in the terminal to create the inverted index. 
  Then run <code> python hw3.py --run </code> in the environment and type http://127.0.0.1:5000/ in browser to view the web application.
  
* Another parameter that shall be paid attention to is the --custom_processor which controls the types of text processors in this assignment. 
  By using the <code> python hw3.py --build </code> command, the system will utilize the default text processor. If the users want to switch it to custom processor, 
  they may need to change the command by adding the --custom_processor argument (<code> python hw3.py --custom_processor --build </code>). Accordingly, the argument shall
  also need to be added into the running command (<code> python hw3.py --custom_processor --run </code>).
  

## Difficulties encountered in this assignment

* Normalization of textual tokens: Since punctuations other than dash symbol ("-") have been removed from every token, 
  the system shall distinguish some acronyms from other tokens consisting of the same group of characters, such as "U.S." and "us."
* Choosing the scope of stop words: the system uses the "English" stop words list built-in NLTK library by default. However, some conjunctive verbs 
  such as "however" and "moreover" could be included during searching for this assignment.   


## Authors

* The lecturer of COSI132A provided the home template. 
* The rest functions and templates were created by Wanyue Xiao independently.

## Testing
#### System with default text processor

* ""(searching for an empty search query)
 No matching result shall be returned. The system throws a warning by displaying “0 document(s) has been returned. Please use another keyword.” on the screen.
 No terms shall be displayed regarding Ignoring Terms and Unknown Search Terms.

* “ ” (searching for whitespace character)
 No matching result shall be returned. The system throws a warning by displaying “0 document(s) has been returned. Please use another keyword.” on the screen.
 No terms shall be displayed regarding Ignoring Terms and Unknown Search Terms.

* “a” (searching for character “a”)
 No matching result shall be returned. The system throws a warning by displaying “0 document(s) has been returned. Please use another keyword.” on the screen.
 The term "a" shall be listed in Ignoring Terms. No terms shall be displayed regarding Unknown Search Terms. The next page button shall not be displayed.

* “The American teacher holds a cake” (searching for several terms)
 No matching result shall be returned. The system throws a warning by displaying “0 document(s) has been returned. Please use another keyword.” on the screen.
 The terms "the" and "a" shall be listed in Ignoring Terms. "cake" and "teacher" shall be displayed in Unknown Search Terms. The next page button shall not be displayed.

* “The U.S. government” (searching for the sentence “The book is on the table”)
 The system throws a warning by displaying “3 document(s) have been returned.” on the screen.
 The term "the" shall be listed in Ignoring Terms. 
 The next page button shall be displayed. 
 (The text processor will normalized the acronym "U.S." to "us", which changes the meaning of term. Therefore, documents with "us" will be returned.)
 
#### System with custom text processor

* ""(searching for an empty search query)
 No matching result shall be returned. The system throws a warning by displaying “0 document(s) has been returned. Please use another keyword.” on the screen.
 No terms shall be displayed regarding Ignoring Terms and Unknown Search Terms.

* “ ” (searching for whitespace character)
 No matching result shall be returned. The system throws a warning by displaying “0 document(s) has been returned. Please use another keyword.” on the screen.
 No terms shall be displayed regarding Ignoring Terms and Unknown Search Terms.

* “a” (searching for character “a”)
 No matching result shall be returned. The system throws a warning by displaying “0 document(s) has been returned. Please use another keyword.” on the screen.
 The term "a" shall be listed in Ignoring Terms. No terms shall be displayed regarding Unknown Search Terms. The next page button shall not be displayed.

* “The American teacher holds a cake” (searching for several terms)
 No matching result shall be returned. The system throws a warning by displaying “0 document(s) has been returned. Please use another keyword.” on the screen.
 The terms "the" and "a" shall be listed in Ignoring Terms. "cake" and "teacher" shall be displayed in Unknown Search Terms. The next page button shall not be displayed.

* “The U.S. government” (searching for the sentence “The book is on the table”)
 The system throws a warning by displaying “2 document(s) have been returned.” on the screen.
 The term "the" shall be listed in Ignoring Terms. The next page button shall be displayed. 
 (The custom processor will recognized the acronym "U.S." and fetch documents with "U.S." instead of "us".)

