import json
from bs4 import BeautifulSoup
import re

# Clean SVAMP dataset
svamp = open('datasets/raw/SVAMP_raw.json')
svamp_data = json.load(svamp)

svamp_list = []
for problem in svamp_data:
    body = problem['Body']
    question = problem['Question']
    equation = problem['Equation']
    answer = problem['Answer']
    problem_type = problem['Type']
    data = {'Body': body, 'Question': question, 'Equation': equation, 'Answer': answer, 'Type': problem_type}
    svamp_list.append(data)

svamp.close()
with open('datasets/SVAMP/SVAMP.json', 'w') as outfile:
    json.dump(svamp_list, outfile, indent=4)

with open('datasets/SVAMP/SVAMP_addition.json', 'w') as outfile:
    json.dump([problem for problem in svamp_list if problem['Type'] == 'Addition'], outfile, indent=4)

with open('datasets/SVAMP/SVAMP_subtraction.json', 'w') as outfile:
    json.dump([problem for problem in svamp_list if problem['Type'] == 'Subtraction'], outfile, indent=4)

# Clean ASDiv dataset
asdiv = open('datasets/raw/ASDiv_raw.xml')
asdiv_data = BeautifulSoup(asdiv, 'xml')
asdiv_problems = asdiv_data.find_all('Problem')

asdiv_list = []
num_asdiv_list = []
for problem in asdiv_problems:
    body = problem.find('Body').text
    question = problem.find('Question').text
    equation = problem.find('Formula').text
    answer = problem.find('Answer').text
    num_answer = re.sub(r'[^0-9]', '', answer)
    if num_answer == '':
        continue
    num_answer = float(num_answer)
    problem_type = problem.find('Solution-Type').text
    data = {'Body': body, 'Question': question, 'Equation': equation, 'Answer': answer, 'Type': problem_type}
    num_data = {'Body': body, 'Question': question, 'Equation': equation, 'Answer': num_answer, 'Type': problem_type}
    asdiv_list.append(data)
    num_asdiv_list.append(num_data)

asdiv.close()

with open('datasets/ASDiv/ASDiv.json', 'w') as outfile:
    json.dump(asdiv_list, outfile, indent=4)

with open('datasets/ASDiv/ASDiv_addition.json', 'w') as outfile:
    json.dump([problem for problem in asdiv_list if problem['Type'] == 'Addition'], outfile, indent=4)

with open('datasets/ASDiv/ASDiv_subtraction.json', 'w') as outfile:
    json.dump([problem for problem in asdiv_list if problem['Type'] == 'Subtraction'], outfile, indent=4)

with open('datasets/ASDiv/ASDiv_numerical.json', 'w') as outfile:
    json.dump(num_asdiv_list, outfile, indent=4)

with open('datasets/ASDiv/ASDiv_numerical_addition.json', 'w') as outfile:
    json.dump([problem for problem in num_asdiv_list if problem['Type'] == 'Addition'], outfile, indent=4)

with open('datasets/ASDiv/ASDiv_numerical_subtraction.json', 'w') as outfile:
    json.dump([problem for problem in num_asdiv_list if problem['Type'] == 'Subtraction'], outfile, indent=4)
