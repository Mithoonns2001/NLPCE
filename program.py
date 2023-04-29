import openai
import os
import json
# from create_files import create_file_structure
with open("files/api.txt") as f:
    openai.api_key = f.read().strip()

class Title:
    def __init__(self):
        self.projects = []



    def add_project(self, project_name):
        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt="provide short file structure with extensions and code for each files(The structure should be represented as a dictionary in Python within curly braces don't include project title, with each directory represented as a nested dictionary and each file represented as a key with value(code for the file with \\n) ,property name should be enclosed in double quotes ) and all should be generated in single line for {} ".format(project_name),
            max_tokens=2000,
            n=1,
            stop=None,
            temperature=0.9,
        )
        code = completions.choices[0].text
        self.projects.append((project_name, code))
        self.write_to_file(project_name, code)

    def remove_project(self, project_name):
        for index, project in enumerate(self.projects):
            if project[0] == project_name:
                self.projects.pop(index)
                os.remove("{}.txt".format(project_name))
                break

    def display_title(self):
        for project in self.projects:
            return(project[1])

    def write_to_file(self, project_name, code):
        with open("C:/Users/NAGARAJAN K/Videos/Captures/p1.txt".format(project_name), "w") as f:
            f.write(code)

# # def generate_code(prompt):
# #     response = openai.Completion.create(
# #         engine="text-davinci-003",
# #         prompt=prompt,
# #         max_tokens=3000,
# #         n=1,
# #         stop=None,
# #         temperature=0.5,
# #     )
# #     generated_code = response.choices[0].text
# #     return generated_code

# # input_text = "build a portfolio website using flask with list of projects and css"
# # title = Title()
# # title.add_project({input_text})
# # title.display_title()

# # a=title.display_title()
# # print(json.dumps(a, separators=(',', ':')))
# # print(a)


# title = Title()
# title.add_project('flask portfolio ')
# file_structure_w= title.display_title()

# # Find the index of the first curly brace
# brace_idx = file_structure_w.find('{')
# # Remove leading whitespace before the first curly brace
# if brace_idx > 0:
#     file_structure_w = file_structure_w[brace_idx:]
#     json_obj = json.loads(file_structure_w)
# # Dump the JSON object as a single-line string
# # retur=json.dumps(json_obj, separators=(',', ':'))

# file_structure_waste = json.dumps(json_obj, separators=(',', ':'))

# # Convert Python dictionary to JSON string

# # Convert JSON string back to Python dictionary
# file_structure = json.loads(file_structure_waste)
# print(file_structure)
# a={"flask portfolio":{"static":{"main.css":"\n.main-header {\n    background-color: #f1f1f1;\n    padding: 20px;\n    text-align: center;\n}\n\n.main-section {\n    padding: 20px;\n    background-color: #f1f1f1;\n    text-align: center;\n}\n"},"templates":{"index.html":"\n<html>\n  <head>\n    <title>Portfolio</title>\n    <link rel=\"stylesheet\" type=\"text/css\" href=\"{{ url_for('static', filename='main.css') }}\">\n  </head>\n  <body>\n    <div class=\"main-header\">\n      <h1>My Portfolio</h1>\n    </div>\n    <div class=\"main-section\">\n      <h2>Welcome to my portfolio!</h2>\n    </div>\n  </body>\n</html>\n"},"app.py":"\nfrom flask import Flask, render_template\n\napp = Flask(__name__)\n\n@app.route('/')\ndef index():\n    return render_template('index.html')\n\nif __name__ == '__main__':\n    app.run()\n"}}
# create_file_structure("nsm3", file_structure)
# # file_structure_waste = json.dumps(a, indent='')
# # print("#############\n",file_structure_waste)
# # demo='''generate code for each file in python nested dictionary form like {"file name with extension":"code with \\n", "folder/file name with extension":"code with \\n", .... }.'''
# # # Set up GPT-3 prompt
# # prompt = f"{input_text}.\n{a}.\n{demo} "
# # # p=prompt
# # # print("adfghjklaksjdvbnm", prompt)
# # generated_code = generate_code(prompt)
# # # print(generated_code)
# import json

# def json_to_single_line(json_obj):
#     # Dump the JSON object as a string with no spaces or newlines
#     return json.dumps(json_obj, separators=(',', ':'))

# # Example usage
# json_obj = {
#     "static": {
#         "css": {
#             "style.css": "h1 {\n    font-size: 3em;\n    color: #3c3c3c;\n}\n\nbody {\n    background-color: #f8f8f8;\n}"
#         },
#         "js": {
#             "index.js": "const printToDom = (divId, textToPrint) => {\n    const selectedDiv = document.getElementById(divId);\n    selectedDiv.innerHTML = textToPrint;\n}\n\nexport { printToDom };"
#         },
#         "images": {}
#     },
#     "templates": {
#         "index.html": "<!DOCTYPE html>\n<html>\n    <head>\n        <title>Flask Portfolio</title>\n        <link rel=\"stylesheet\" href=\"/static/css/style.css\">\n    </head>\n    <body>\n        <h1>Flask Portfolio</h1>\n        <script src=\"/static/js/index.js\"></script>\n    </body>\n</html>"
#     },
#     "app.py": "from flask import Flask\n\napp = Flask(__name__)\n\n@app.route('/')\ndef index():\n    return 'Flask Portfolio'\n\nif __name__ == '__main__':\n    app.run()"
# }

# single_line_json = json_to_single_line(json_obj)
# print(single_line_json)
