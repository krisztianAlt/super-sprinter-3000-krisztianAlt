from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
import data_manager
import os


current_file_path = os.path.dirname(os.path.abspath(__file__))
file_name = current_file_path + '/stories.csv'
app = Flask(__name__)


# Listing
@app.route('/', methods=['POST', 'GET'])
@app.route('/list', methods=['POST', 'GET'])
def listing():
    stories = data_manager.get_table_from_file(file_name)
    for record in stories:
        for index in range(0, len(record)):
            record[index] = record[index].replace('LINEBREAK', '\r\n')
    return render_template("list.html", stories=stories)


# Add new item
@app.route('/story', methods=['POST'])
def add_new_item():
    return render_template('form.html')


# Write a new story to file
@app.route('/new_story', methods=['POST'])
def new_story_write_to_file():
    stories = data_manager.get_table_from_file(file_name)
    new_story = []
    if len(stories) < 1:
        new_id = 1
    else:
        new_id = int(stories[-1][0]) + 1
    new_story = [str(new_id),
                 request.form['story_title'],
                 request.form['user_story'],
                 request.form['acceptance_criteria'],
                 str(request.form['business_value']),
                 str(request.form['estimation']),
                 request.form['status']]
    stories.append(new_story)
    data_manager.write_table_to_file(file_name, stories)
    return redirect(url_for('listing'))


# Delete a story from file
@app.route('/delete', methods=['POST'])
def delete_story():
    stories = data_manager.get_table_from_file(file_name)
    del_id = request.form['story_id_to_delete']
    for index in range(0, len(stories)):
        if stories[index][0] == del_id:
            del_index = index
    del stories[del_index]
    data_manager.write_table_to_file(file_name, stories)
    return redirect(url_for('listing'))


# Update a story
@app.route('/story/story_id', methods=['POST'])
def update_story():
    stories = data_manager.get_table_from_file(file_name)
    for record in stories:
        if record[0] == request.form['story_id_to_update']:
            for index in range(0, len(record)):
                record[index] = record[index].replace('LINEBREAK', '\r\n')
            story_to_update = record
    return render_template("update.html", story=story_to_update)


# Update a story record in file
@app.route('/update', methods=['POST'])
def update_story_in_file():
    stories = data_manager.get_table_from_file(file_name)
    updated_story = [request.form['story_id'],
                     request.form['story_title'],
                     request.form['user_story'],
                     request.form['acceptance_criteria'],
                     str(request.form['business_value']),
                     str(request.form['estimation']),
                     request.form['status']]
    for index in range(0, len(stories)):
        if stories[index][0] == updated_story[0]:
            stories[index] = updated_story
    data_manager.write_table_to_file(file_name, stories)
    return redirect(url_for('listing'))


if __name__ == '__main__':
    app.debug = True
    app.run()
