import os
from flask import Flask, render_template, request, url_for, send_from_directory

# import our OCR function
from ocr_core import ocr_core

# define a folder to store and later serve the image
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

# function to check the file extension
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the upload page
@app.route('/', methods=['GET', 'POST'])
def home_page():
	if request.method == 'POST':
		# check if there is a file in the request
		if 'file' not in request.files:
			return render_template('home.html', msg='No file Selected')
		file = request.files['file']

		#if no file is selected
		if file.filename == '':
			return render_template('home.html', msg='No file selected')

		if file and allowed_file(file.filename):
			file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))

			#call the ocr function on it
			extracted_text = ocr_core(file)

			# extract the text and display it
			return render_template('home.html',
									msg='Successfully processed',
									extracted_text=extracted_text,
									img_src=UPLOAD_FOLDER + file.filename)

	elif request.method == 'GET':
		return render_template('home.html')

if __name__ == '__main__':
	app.run(debug=True)





