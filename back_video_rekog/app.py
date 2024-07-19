from flask import Flask, request, jsonify
import boto3
from flask_cors import CORS
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

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

# def update_label(list, label):
#     for item in list:
#         if item['name'] == label['name']:
#             item['timestamp'].append(label['timestamp'])
#             return

# Function to get label detection results
def get_label_detection(job_id):
    max_results = 10
    pagination_token = ''
    finished = False
    sure_90 = []
    almost_70 = []
    not_sure_40 = []
    # f = open("D:\\myfiles\welcome.txt", "r")
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
    while not finished:
        response = rekognition_client.get_label_detection(
            JobId=job_id,
            MaxResults=max_results,
            NextToken=pagination_token,
            SortBy='TIMESTAMP'
        )
        # Print labels detected in the video
        for label in response['Labels']:
            name = label['Label']['Name']
            confidence = int(label['Label']['Confidence'])
            timestamp = int(label['Timestamp'])
            labels = {
                "confidence": confidence,
                "name": name,
                "timestamp": [timestamp]
            }
            if confidence >= 90:
                if labels[name] in sure_90:
                    for item in sure_90:
                        if item["name"] == labels["name"]:
                            item["timestamp"].append(labels["timestamp"])
                    # label_with_same_name = next((item for item in sure_90 if item["name"] == labels[name]), None)
                    continue
                sure_90.append(labels)
            elif confidence < 90 and confidence >= 70:
                if labels[name] in almost_70:
                    for item in almost_70:
                        if item["name"] == labels["name"]:
                            item["timestamp"].append(labels["timestamp"])
                    continue
                almost_70.append(labels)
            elif confidence < 70 and confidence >= 40:
                if labels[name] in not_sure_40:
                    for item in not_sure_40:
                        if item["name"] == labels["name"]:
                            item["timestamp"].append(labels["timestamp"])
                    continue
                not_sure_40.append(labels)
            print(f"Label: {label['Label']['Name']}")
            print(f"Confidence: {label['Label']['Confidence']}")
            print(f"Timestamp: {label['Timestamp']}")
            print("----------")
        pagination_token = response.get('NextToken', None)
        finished = pagination_token is None
    # response = rekognition_client.get_label_detection(
    #     JobId=job_id,
    #     MaxResults=1,
#     SortBy='TIMESTAMP'
    # )
    respone_labels = {
        "90_100": sorted(sure_90, key=lambda x: x['confidence'], reverse=True),
        "70_90": sorted(almost_70, key=lambda x: x['confidence'], reverse=True),
        "40_70": sorted(not_sure_40, key=lambda x: x['confidence'], reverse=True)
    }
    return respone_labels
        

# Route to handle video uploads
@app.route('/upload', methods=['POST'])
def upload_video():
    print('Handle upload triggered')
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
            response_to_ui = {}
            # response_to_ui = {'labels': {'JobStatus': 'SUCCEEDED', 'VideoMetadata': {'Codec': 'h264', 'DurationMillis': 9600, 'Format': 'QuickTime / MOV', 'FrameRate': 25.0, 'FrameHeight': 1080, 'FrameWidth': 1920, 'ColorRange': 'LIMITED'}, 'NextToken': '1K4zrai2RDfjgILpKfkvmBcvjtpfl110RS3lRmXFEBZjNgZ0dHlBgOESp4DEh4RZSR17zlS7', 'Labels': [{'Timestamp': 0, 'Label': {'Name': 'Boy', 'Confidence': 90.10444641113281, 'Instances': [{'BoundingBox': {'Width': 0.1568606048822403, 'Height': 0.6204899549484253, 'Left': 0.2810244560241699, 'Top': 0.37830355763435364}, 'Confidence': 89.93324279785156}], 'Parents': [{'Name': 'Male'}, {'Name': 'Person'}], 'Aliases': [], 'Categories': [{'Name': 'Person Description'}]}}], 'LabelModelVersion': '3.0', 'JobId': '463fc0180adbad3581cc46c7cda86666d159f91e5208405cd0820f1f8c47cdca', 'Video': {'S3Object': {'Bucket': 'video-recog', 'Name': 'kfir_tennis_fat.mp4'}}, 'GetRequestMetadata': {'SortBy': 'TIMESTAMP', 'AggregateBy': 'TIMESTAMPS'}, 'ResponseMetadata': {'RequestId': '0cbfec5b-8cc7-4c45-8779-162c8e508971', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '0cbfec5b-8cc7-4c45-8779-162c8e508971', 'content-type': 'application/x-amz-json-1.1', 'content-length': '873', 'date': 'Fri, 12 Jul 2024 13:40:13 GMT'}, 'RetryAttempts': 0}}, 'object_url': 'https://video-recog.s3.amazonaws.com/kfir_tennis_fat.mp4'}
            # return response_to_ui
            s3_client.upload_fileobj(file, S3_BUCKET, file.filename)
            # Get S3 URI
            # s3_uri = f's3://{S3_BUCKET}/{file.filename}'
            # Get Object URL
            job_id = start_label_detection(S3_BUCKET, file.filename)
            print(f"Started label detection job with ID: {job_id}")
            response_to_ui['labels']= get_label_detection(job_id)
            response_to_ui['object_url'] = f'https://{S3_BUCKET}.s3.amazonaws.com/{file.filename}'
            print(response_to_ui)
            # return jsonify({'message': 'File uploaded successfully'}), 200
            return jsonify(response_to_ui), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Something went wrong'}), 500

if __name__ == '__main__':
    app.run(debug=True)