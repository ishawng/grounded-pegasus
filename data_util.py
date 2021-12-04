import json
import io
import sys

from collections import defaultdict

import pandas as pd

def get_question_bodies(dataset, with_equation=False, with_answer=False):
    questions = []
    for q in dataset:
        s = q["Body"] + " : " + q["Question"]
        if with_equation:
            s += ". " + q["Equation"]
        if with_answer:
            s += ". " + str(q["Answer"])
        questions.append(s)
    
    return questions

def is_number(word):
    if all(c.isnumeric() or c == "." for c in word.replace(" ", "")):
        return True
    return False

def load_dataset(path):
    with open(path, 'r') as d:
        dataset = json.loads(d.read())
    return dataset

def output_to_src(questions, path):
    with io.open(path, 'w') as file:
        json.dump(questions, file)
    return

def main_func():
    cleaned_data, output_file = sys.argv[1], sys.argv[2]
    print("loading")
    data = load_dataset(cleaned_data)
    print("data loaded")
    questions = get_question_bodies(data)
    print(questions)
    print("outputting to .src")
    output_to_src(questions, output_file)
    return

def substitute_numbers(dataset):
    for q in dataset:
        body = q["Body"]
        cleaned_body = ["<n>" if is_number(x) else x for x in body.split(" ")]
        q["Body"] = " ".join(cleaned_body)
        question = q["Question"]
        cleaned_question = ["<n>" if is_number(x) else x for x in question.split(" ")]
        q["Question"] = " ".join(cleaned_question)
        equation = q["Equation"]
        cleaned_eq = ["<n>" if is_number(c) else c for c in equation.split(" ")]
        q["Equation"] = " ".join(cleaned_eq)
    return

def categorize_questions(dataset):
    categories = defaultdict(list)
    for q in dataset:
        categories[q["Type"]].append(q)

    return categories

def write_categories_to_files(categories):
    for cat_name, questions in categories.items():
        path_name = "datasets/nonnumeric/ASDIV_{}".format(cat_name.lower())
        output_to_src(questions, path_name)
    return

# data = load_dataset("datasets/ASDIV/ASDIV.json")
# substitute_numbers(data)
# cats = categorize_questions(data)
# write_categories_to_files(cats)

def write_to_dataframe(src_path, dst_path):
    with open(src_path, 'r') as d:
        data = json.loads(d.read())
    df = pd.json_normalize(data)
    df.to_pickle(dst_path)
    return

# write_to_dataframe("datasets/nonnumeric/SVAMP.json", "nonnumeric_SVAMP.pkl")
    


