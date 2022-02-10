from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, Markup
from utils import title_match, load_wapo, get_snippet

app = Flask(__name__)
DATA_DIR = Path(__file__).parent.joinpath("pa2_data")
wapo_path = DATA_DIR.joinpath("wapo_pa2.jl")
wapo_docs = load_wapo(wapo_path)  # load and process WAPO documents
page_limit = 8 # the number of documents showing in each page

@app.route("/")
def home():
    """
    home page
    :return: a html home page which enables user to type in search query
    """
    return render_template("home.html")

@app.route("/results", methods=["POST"])
def results():
    """
    result page
    :return: a json object including all the articles whose titles include the users' search queries
    """
    query_text = request.form["query"]  # Get the raw user query from home page
    page_num = int(request.form['page_num'])  # Get the page number

    doc_ids = []
    for key,values in wapo_docs.items():
        if title_match(query_text, values.get("title")):
            doc_ids.append(key)

    global doc_results
    doc_results = [(get_snippet(str(each), wapo_docs)) for each in doc_ids]
    total_number=len(doc_results)
    print(total_number)

    doc_json ={
        "page_limit":page_limit,
        "query_text":str(query_text),
        "page_num":int(page_num),
        "doc_results":doc_results,
        "total_number":total_number
    }
    return render_template('results.html', data=doc_json)

@app.route("/results/<int:page_id>", methods=["POST"])
def next_page(page_id):
    """
    "next page" to show more results
    :param page_id: a integer which represents the number of web page users is browsing at
    :return: a json object including all the articles whose titles include the users' search queries
    """
    query_text = request.form["query"]  # Get the raw user query from home page
    total_number=int(request.form["total_number"])

    if len(doc_results) == 0:
        doc_json ={
            "page_limit":page_limit,
            "query_text":str(query_text),
            "page_num":int(page_id),
            "doc_results":doc_results,
            "total_number":0
        }
        return render_template('results.html', data=doc_json)
    else:
        doc_json ={
                "page_limit":page_limit,
                "query_text":str(query_text),
                "page_num":int(page_id),
                "doc_results":doc_results,
                "total_number":total_number
        }
        return render_template('results.html', data=doc_json)

@app.route("/doc_data/<doc_id>")
def doc_data(doc_id):
    """
    document page
    :param doc_id: the unique id of a document
    :return: a html file which includes all the elements possessed by a document
    """
    get_content = wapo_docs.get(doc_id)

    ts = int(get_content.get("published_date"))/1000
    date=datetime.fromtimestamp(ts)
    doc_content ={
        "title":str(get_content.get("title")),
        "author":str(get_content.get("author")),
        "date":date,
        "content": Markup(get_content.get("content_str"))
    }
    return render_template('doc.html', data = doc_content)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
