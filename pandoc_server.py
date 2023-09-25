import os
import subprocess
from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)


enviornment = "PROD"
enviornment = "TEST"
url = 'http://dragonfly:8000'
if enviornment == "PROD":
    url = "http://127.0.0.1:8000"

ACCESS_KEY = "QDof4lk0TaxhX3jK"
SECRET_KEY = "0vteXQ95pTfCGaA9a5vgUVixsedmKNi1"

# use third party object storage
s3 = boto3.resource('s3', endpoint_url= url,
  aws_access_key_id = ACCESS_KEY,
  aws_secret_access_key = SECRET_KEY)


PRIMARY_BUCKET_NAME = 'syncthing'
NEW_FILE_BUCKET_NAME = 'pandoc_output'

@app.route('/pandocify', methods=['POST'])
def pandocify():
    try:
        #print("request")
        data = request.json
        # Save the file to the 
        #print('all is well here')
        filename = os.path.join("./", data['filename'])
        #print('So far so good')
        primary_bucket = s3.Bucket("syncthing")
        file_in_bucket = primary_bucket.Object(data['filename'])
        
        #response = s3.get_object(Bucket=PRIMARY_BUCKET_NAME, Key=data['filename'])
        #print('almost there')
        #file_content = response['Body'].read().decode('utf-8')
        file_content = file_in_bucket.get()['Body'].read().decode('utf-8')

        #print(file_content)
        
        with open('temp.md', 'w+') as f:
            f.write(str(file_content))
        
        print(os.getcwd())
        # Define the shell command to run on the uploaded file
        PANDOC_COMMAND_STARTER = 'pandoc '
        pandoc_engine = '--pdf-engine=xelatex ' 
        papersize_argument = '-V papersize:letterpaper '
        margin_argument = '-V geometry:margin=1.2in '
        
        pandoc_shell_command = f'{PANDOC_COMMAND_STARTER} -s -o output.pdf temp.md {pandoc_engine}{papersize_argument}{margin_argument}'
        
        shell_command = f'{pandoc_shell_command} '
        

        # Run the shell command
        result = subprocess.run(shell_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Return the output and error (if any) from the shell command
        response_data = {
            'output': result.stdout,
            'error': result.stderr,
        }
        return jsonify(response_data), 200
        #return jsonify({"status": "ok"}), 200


    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
