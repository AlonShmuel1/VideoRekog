from flask import Flask, request, jsonify
import boto3
from flask_cors import CORS
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Configure AWS information
S3_BUCKET = 'video-recog'
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')


# Configure AWS clients
s3_client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

rekognition_client = boto3.client(
    'rekognition',
    region_name='us-east-1',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)


# Function to start label detection
def start_label_detection(bucket, video_key):
    response = rekognition_client.start_label_detection(
        Video={'S3Object': {'Bucket': bucket, 'Name': video_key}},
    )
    return response['JobId']


# Function to get label detection results
def get_label_detection(job_id):
    # max_results = 10
    # pagination_token = ''
    # finished = False
    job_status = ''
    while 'SUCCEEDED' not in job_status:
        response = rekognition_client.get_label_detection(
            JobId=job_id,
        )
        job_status = response['JobStatus']
        if job_status == 'SUCCEEDED':
            continue
        sleep(5)
        print(response['JobStatus'])
    # while not finished:
    #     response = rekognition_client.get_label_detection(
    #         JobId=job_id,
    #         MaxResults=max_results,
    #         NextToken=pagination_token,
    #         SortBy='TIMESTAMP'
    #     )
    #     # Print labels detected in the video
    #     for label in response['Labels']:
    #         print(f"Timestamp: {label['Timestamp']}")
    #         print(f"Label: {label['Label']['Name']}")
    #         print(f"Confidence: {label['Label']['Confidence']}")
    #         print("----------")
    #     pagination_token = response.get('NextToken', None)
    #     finished = pagination_token is None
    response = rekognition_client.get_label_detection(
        JobId=job_id,
        MaxResults=1,
        SortBy='TIMESTAMP'
    )
    return response
        

# Route to handle video uploads
@app.route('/upload', methods=['POST'])
def upload_video():
    try:
        # Check if the post request has the file part
        if 'video' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['video']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file:
            # Upload file to S3 bucket
            s3_client.upload_fileobj(file, S3_BUCKET, file.filename)
            # Get S3 URI
            s3_uri = f's3://{S3_BUCKET}/{file.filename}'
            # Get Object URL
            object_url = f'https://{S3_BUCKET}.s3.amazonaws.com/{file.filename}'
            print(f"URI: {s3_uri}\nURL: {object_url}")
            job_id = start_label_detection(S3_BUCKET, file.filename)
            print(f"Started label detection job with ID: {job_id}")
            response = get_label_detection(job_id)
            print(response)
            # return jsonify({'message': 'File uploaded successfully'}), 200
            return jsonify({'message': response}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Something went wrong'}), 500

if __name__ == '__main__':
    app.run(debug=True)