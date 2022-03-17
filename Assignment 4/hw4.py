from pathlib import Path
import argparse
import ast
from flask import Flask, render_template, request
from utils import load_wapo, get_snippet
from inverted_index import build_inverted_index, query_inverted_index
from mongo_db import db, insert_docs, query_doc, drop

# read wapo corpus dataset from a jl file
app = Flask(__name__)
data_dir = Path(__file__).parent.joinpath("pa4_data")
wapo_path = data_dir.joinpath("wapo_pa4.jl")
# define the number of documents showing in each page
page_limit = 6
top_k = 8


def createDB(name:str) -> None:
    if not name in db.list_collection_names():
        """
        home page
        :return: a html home page which enables user to type in search query
        """
        insert_docs(load_wapo(wapo_path))


def countDoc(name:str) -> int:
    if name in db.list_collection_names():
        my_collection = db[name]
        total_count = my_collection.count_documents({})
        return total_count


# home page
@app.route("/")
def home():
    return render_template("home.html")


# result page
@app.route("/results", methods=["POST"])
def results():
    """
    result page
    :return: a json object including all the articles whose titles include the users' search queries
    """
    total_Doc = countDoc("doc_len_index")
    query_text = request.form["query"]  # Get the raw user query from home page
    page_num = int(request.form['page_num'])  # Get the page number from home page
    doc_ids, remove_stopwords, unknownToken, query_term, doc_report = query_inverted_index(query_text, top_k, total_Doc)
    remove_stopwords = list(set(remove_stopwords))
    unknownToken = list(set(unknownToken))

    # use query_doc to fetch matched document stored in mongoDB
    doc_result = [(query_doc(x[1]), x[0]) for x in doc_ids]
    # get snippet for each document
    doc_results = []
    for each in doc_result:
        doc_results.append( (get_snippet(each[0]), round(each[1],4), doc_report[each[0]['id']]) )
    if len(doc_result) > 0:
        doc_result = sorted(doc_result, key=lambda x: x[1])
    print(doc_result)

    print("doc_results snippet ", doc_results)

    total_number=len(doc_results)
    doc_json ={"page_limit":page_limit,
               "query_text":str(query_text),
               "page_num":int(page_num),
               "doc_results":doc_results,
               "total_number":total_number,
               "remove_sw":remove_stopwords,
               "query_term": query_term,
               "unknownToken":unknownToken
               }
    return render_template('results.html', data=doc_json)


# "next page" to show more results
@app.route("/results/<int:page_id>", methods=["POST"])
def next_page(page_id):
    """
    "next page" to show more results
    :param page_id: a integer which represents the number of web page users is browsing at
    :return: a json object including all the articles whose titles include the users' search queries
    """
    query_text = request.form["query"]  # Get the raw user query from home page
    total_number=int(request.form["total_number"])
    remove_sw = ast.literal_eval(request.form["remove_sw"])
    query_term = ast.literal_eval(request.form["query_term"])
    unknownToken = ast.literal_eval(request.form["unknownToken"])
    doc_results = ast.literal_eval(request.form["doc_results"])

    if len(doc_results) == 0:
        doc_json ={"page_limit":page_limit,
                   "query_text":str(query_text),
                   "page_num":int(page_id),
                   "doc_results":doc_results,
                   "total_number":0,
                   "remove_sw":remove_sw,
                   "query_term": query_term,
                   "unknownToken":unknownToken}
        return render_template('results.html', data=doc_json)
    else:
        doc_json ={"page_limit":page_limit,
                   "query_text":str(query_text),
                   "page_num":int(page_id),
                   "doc_results":doc_results,
                   "total_number":total_number,
                   "remove_sw":remove_sw,
                   "query_term": query_term,
                   "unknownToken":unknownToken}
        return render_template('results.html', data=doc_json)


# document page
@app.route("/doc_data/<int:doc_id>")
def doc_data(doc_id):
    """_processor - document page
    :param doc_id: the unique id of a document
    :return: a html file which includes all the elements possessed by a document
    """
    get_content = query_doc(doc_id)
    doc_content ={
        "title":str(get_content["title"]),
        "author":str(get_content["author"]),
        "date":str(get_content["published_date"]),
        "content": str(get_content["content_str"])
    }
    return render_template('doc.html', data=doc_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VS IR system")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    if args.test:
        wapo_path = data_dir.joinpath("wapo_test.jl")

    if args.build:
        print("start to reload test dataset" if args.test else "start to reload dataset")
        drop("wapo_docs")
        drop("vs_index")
        drop("doc_len_index")
        createDB("wapo_docs")
        build_inverted_index(load_wapo(wapo_path))

    if args.run:
        app.run(debug=True, port=5000)
