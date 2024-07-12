import React, { useState } from 'react';
import './App.css';

function App() {
  const [videoFile, setVideoFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setVideoFile(file);
    }
  };

  const uploadVideo = async () => {
    console.log(process.env);
    if (!videoFile) {
      alert('Please select a video file first.');
      return;
    }

    const formData = new FormData();
    formData.append('video', videoFile);

    try {
      const uploadUrl = process.env.REACT_APP_API_URL + '/upload';
      const response = await fetch(uploadUrl, {
        method: 'POST',
        body: formData,
      });
      console.log('sent file to upload');
      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      console.log('Upload successful!', data);
      alert('Upload successful!');
      if (data.object_url) {
        setVideoUrl(data.object_url);
      }
    } catch (error) {
      console.error('Error uploading the video:', error);
      alert('Error uploading the video.');
    }
  };

  return (
    <div className="container">
      <h2 className="uploadLabel">Upload a Video</h2>
      <input type="file" onChange={handleFileUpload} accept="video/*" />
      <button className="uploadButton" onClick={uploadVideo}>Upload</button>

      {videoUrl && (
        <div>
          <h3>Video Preview:</h3>
          <video src={videoUrl} controls className="video-preview"></video>
          <p>Video URL: <a href={videoUrl} target="_blank" rel="noopener noreferrer">{videoUrl}</a></p>
        </div>
      )}
    </div>
  );
}

export default App;
