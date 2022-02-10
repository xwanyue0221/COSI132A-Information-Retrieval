# Assignment Info

COSI132A Information Retrieval Spring 2022 - Assignment 2 Building a simple boolean search IR web app

## Description

* This is documentation of the first coding assignment for course COSI 132A Information Retrieval. 
* This assignment aims to develop a toy search engine that empowers users to find news articles through ad hoc searching. By typing in keywords or phrases, articles with the same term/token will be extracted and displayed on the webpage. This project uses the Flask framework to build a web server and application. The web page templates developed through HTML provide a simple User Interface that enables users to interact with the backend system.

## Getting Started

### Dependencies

* Python 3.9 is required, and dependencies include JSON, Flask, DateTime, and typing.

### Dataset

* 50 JSON format documents from TREC Washington Post Corpus (WAPO) were used for system diagnosis.

### Installing

* All dependencies are listed in the requirement.txt file. Anyone who wishes to run this project on a local environment could install these packages using the command: <code>pip3 install -r requirements.txt </code>.

### Executing program

* Before running this project in the terminal, the user shall be aware that all the required packages listed above shall be properly installed or upgraded to the latest version. To properly run this program on local environment, the user can use the <code> python hw2.py </code> command in terminal.

## Difficulties encountered in this assignment

* Spent a whole day to get familiar with Flask
* Before feeding the article content into the HTML template, it is necessary to use the Flask built-in MARKUP function to convert a string as safe for inclusion in HTML/XML output without needing to be escaped. 

## Authors

* The lecturer of COSI132A provided the home template. 
* The rest functions and templates were created by Wanyue Xiao independently.

## Testing

* “(searching for an empty search query)
 No matching result shall be returned. The system throws a warning by displaying “No matching result. Please use another keyword.” on the screen.

* “ ” (searching for whitespace character)
 No matching result shall be returned. The system throws a warning by displaying “No matching result. Please use another keyword.” on the screen.

* “a” (searching for character “a”)
 Seven documents shall be returned. The next page button shall not be displayed.

* “the” (searching for phrase “Iran”)
 One document shall be returned. The next page button shall not be displayed.

* “the” (searching for the sentence “The book is on the table”)
 Ten documents shall be returned on 2 pages. The next page button shall be displayed. 

