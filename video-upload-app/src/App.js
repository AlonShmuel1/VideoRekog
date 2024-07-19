import React, { useState,useRef } from 'react';
import './App.css';
import Card from './Components/Card';
import Spinner from './Animations/Spinner';

function App() {
  const [videoFile, setVideoFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);
  const [isVisible, setIsVisible] = useState(true);
  const [loading, setLoading] = useState(false); // state to manage loading
  const videoRef = useRef(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setVideoFile(file);
    }
  };

  const uploadVideo = async () => {
    if (!videoFile) {
      alert('Please select a video file first.');
      return;
    }

    const formData = new FormData();
    formData.append('video', videoFile);
    setLoading(true);
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
        setIsVisible(false)
        setVideoUrl(data.object_url);
      }
    } catch (error) {
      console.error('Error uploading the video:', error);
      alert('Error uploading the video.');
    } finally {
      setLoading(false);
    }
  };
  const skipToTimestamp = (timeStamp) => {
    if (videoRef.current) {
      videoRef.current.currentTime = timeStamp;
    }
  };
  return (
    <div className="container">
      <h2 className="uploadLabel">Upload a Video</h2>
      <div className="uploadForm" style={{ display: isVisible ? 'block' : 'none' }}>
      <input type="file" onChange={handleFileUpload} accept="video/*" />
      <button className="uploadButton" onClick={uploadVideo} disabled={loading}>{loading ? 'Uploading...' : 'Upload'}</button>
      {loading && <Spinner />} {/* show spinner when loading */}
      </div>
      {videoUrl && (
        <div>
          <h3>Video Preview:</h3>
          <video src={videoUrl} controls className="video-preview" ref={videoRef}></video>
        </div>
      )}
       <div className="card-container">
        <Card image="https://via.placeholder.com/150" label="Boy" confidence="70.5" onClick={() => skipToTimestamp(3)} />
        <Card image="https://via.placeholder.com/150" label="Boy" confidence="70.5" onClick={() => skipToTimestamp(4)} />
        <Card image="https://via.placeholder.com/150" label="Boy" confidence="70.5" onClick={() => skipToTimestamp(5)} />
        <Card image="https://via.placeholder.com/150" label="Boy" confidence="70.5" onClick={() => skipToTimestamp(6)} />
        <Card image="https://via.placeholder.com/150" label="Boy" confidence="70.5" onClick={() => skipToTimestamp(7)} />
        <Card image="https://via.placeholder.com/150" label="Boy" confidence="70.5" onClick={() => skipToTimestamp(11)} />
      </div>
    </div>
  );
}

export default App;
