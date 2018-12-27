from flask import Flask, render_template, request, abort, send_file
from werkzeug import secure_filename
import os
app = Flask(__name__)

server_path = "/Users/manikant/Documents/blob_storage/server/"
local_path = "/Users/manikant/Documents/blob_storage/local/"

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(server_path, secure_filename(f.filename)))
      return 'file uploaded successfully'

@app.route('/files/', defaults={'req_path': ''})
@app.route('/files/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = server_path

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        print(abs_path)
        f = send_file(abs_path)
        content = f.response.file.read()
        print(str(content))
        f = open(os.path.join(local_path, os.path.basename(abs_path)), "wb")
        f.write((content))
        f.close()
        # print("MMMM" + str(f.response.file.read()))
        dir = os.path.dirname(abs_path)
        files = os.listdir(dir)
        return render_template('files.html', files=files)
        

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('files.html', files=files)
		
if __name__ == '__main__':
   app.run(debug = True)