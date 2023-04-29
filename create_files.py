import json
import os

# with open('files/p1.txt', 'r') as f:
#     file_structure = json.load(f)
file_structure={
  "build_a_portfolio_website_using_flask": {
    "static": {
      "css": {
        "style.css": "body {\n  background: #fafafa;\n}\n\nh1 {\n  font-family: sans-serif;\n  font-size: 24px;\n  color: #333;\n}\n\n"
      }
    },
    "templates": {
      "layout.html": "<!DOCTYPE html>\n<html>\n  <head>\n    <meta charset=\"utf-8\">\n    <title>Portfolio</title>\n    <link rel=\"stylesheet\" href=\"/static/css/style.css\">\n  </head>\n  <body>\n    {% block content %}{% endblock %}\n  </body>\n</html>\n",
      "home.html": "{% extends \"layout.html\" %}\n\n{% block content %}\n  <h1>My Portfolio</h1>\n  <ul>\n    {% for project in projects %}\n      <li>{{ project }}</li>\n    {% endfor %}\n  </ul>\n{% endblock %}\n"
    },
    "app.py": "from flask import Flask, render_template\n\napp = Flask(__name__)\n\n@app.route('/')\ndef home():\n  projects = [\n    'Project 1',\n    'Project 2',\n    'Project 3'\n  ]\n\n  return render_template('home.html', projects=projects)\n\nif __name__ == '__main__':\n  app.run()\n"
  }
}
def create_file_structure(parent_dir, file_structure):
    for name, value in file_structure.items():
        if isinstance(value, dict):
            # If the value is a dictionary, create a subdirectory and recursively call this function.
            subdir = os.path.join(parent_dir, name)
            os.makedirs(subdir, exist_ok=True)
            create_file_structure(subdir, value)
        else:
            # If the value is a string, create a file with the specified extension and write the value to the file.
            filename, content = name, value
            filepath = os.path.join(parent_dir, filename)
            with open(filepath, 'w') as f:
                f.write(content)


# # Set the name of the root directory
# root_dir = 'projects'

# # Create the file structure in the current working directory.
# create_file_structure(root_dir, file_structure)
