from typing import Dict, Union, Generator, Tuple
import functools
import os
from datetime import datetime
import json
import re
import time

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_t = time.perf_counter()
        f_value = func(*args, **kwargs)
        elapsed_t = time.perf_counter() - start_t
        mins = elapsed_t // 60
        print(
            f"'{func.__name__}' elapsed time: {mins} minutes, {elapsed_t - mins * 60:0.2f} seconds"
        )
        return f_value

    return wrapper_timer


def get_snippet(doc_dict: Dict) -> Tuple:
    """
    id: a string object which corresponds to each document's unique id
    doc_dict: a dict object which includes all essential elements possessed by a document
    return: a tuple object which includes three elements, including document unique id, document's title, and the first 150 characters of this document content
    """
    id = doc_dict['id']
    title = doc_dict['title']
    content = doc_dict['content_str']
    return id, title, content[:150]+'......'

def load_wapo(wapo_jl_path: Union[str, os.PathLike]) -> Generator[Dict, None, None]:
    """
    It's same with the load_wapo in HW3
    """
    counter = 0
    CLEANR = re.compile('<.*?>')
    with open(wapo_jl_path, 'r', encoding='UTF-8') as file:
        for line in file:
            if(line):
                dictData = {}
                conv = json.loads(line)
                sanitized_html = " ".join([each.get("content") for each in conv.get("contents") if each.get("type") == "sanitized_html"])
                cleantext = re.sub(CLEANR, '', sanitized_html)
                ts = int(conv.get("published_date"))/1000
                date=datetime.fromtimestamp(ts)

                dictData["id"] = counter
                dictData["title"] = conv.get("title")
                dictData["author"] = conv.get("author")
                dictData["published_date"] = date
                dictData["content_str"] = cleantext
                counter += 1

                yield dictData


if __name__ == "__main__":
    pass
