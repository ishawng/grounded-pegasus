import json
import io
import sys

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

def load_dataset(path):
    with open(path, 'r') as d:
        dataset = json.loads(d.read())
    return dataset

def output_to_src(questions, path):
    with io.open(path, 'w') as file:
        for q in questions:
            file.write(q + "\n")
    return

cleaned_data, output_file = sys.argv[1], sys.argv[2]

print("loading")
data = load_dataset(cleaned_data)
print("data loaded")
questions = get_question_bodies(data)
print(questions)
print("outputting to .src")
output_to_src(questions, output_file)

