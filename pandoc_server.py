import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the directory where uploaded files will be saved
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if the 'file' field is in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the file to the server
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)

        # Define the shell command to run on the uploaded file
        shell_command = f'your_shell_command_here {filename}'

        # Run the shell command
        result = subprocess.run(shell_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Return the output and error (if any) from the shell command
        response_data = {
            'output': result.stdout,
            'error': result.stderr,
        }
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
