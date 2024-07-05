from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# Configure S3 bucket information
S3_BUCKET = 'video-recog'
S3_ACCESS_KEY = 'admin-at-211125447444'
S3_SECRET_KEY = 'ivm4UoJ6kWlEq4IE0UAIeovkj3NyDiwNfVZt0LGkk3sSsw8lHbn6fRa2mXI='

# Configure boto3 S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY
)

# Route to handle video uploads
@app.route('/upload', methods=['POST'])
def upload_video():
    try:
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file:
            # Upload file to S3 bucket
            s3.upload_fileobj(file, S3_BUCKET, file.filename)
            return jsonify({'message': 'File uploaded successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Something went wrong'}), 500

if __name__ == '__main__':
    app.run(debug=True)