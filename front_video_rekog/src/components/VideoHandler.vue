<template>
  <div class="container">
    <h2 class="uploadLabel">Upload a Video</h2>
    <input type="file" @change="handleFileUpload" accept="video/*" />
    <button class="uploadButton" @click="uploadVideo">Upload</button>

    <div v-if="videoUrl">
      <h3>Video Preview:</h3>
      <video :src="videoUrl" controls class="video-preview"></video>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      videoFile: null,
      videoUrl: null
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.videoFile = file;
        this.videoUrl = URL.createObjectURL(file);
      }
    },
    async uploadVideo() {
      console.log(import.meta.env);
      if (!this.videoFile) {
        alert('Please select a video file first.');
        return;
      }

      // Create a FormData object to prepare the file for upload
      const formData = new FormData();
      formData.append('video', this.videoFile);

      try {
        // Replace with your actual upload URL
        const uploadUrl = import.meta.env.VITE_API_URL
        const response = await fetch(uploadUrl, {
          method: 'POST',
          body: formData
        });
        
        if (!response.ok) {
          throw new Error('Upload failed');
        }

        const data = await response.json();
        console.log('Upload successful!', data);
        alert('Upload successful!');
      } catch (error) {
        console.error('Error uploading the video:', error);
        alert('Error uploading the video.');
      }
    }
  }
};
</script>

<style scoped>
.container {
  padding: auto;
  max-width: 700px;
  margin: 50%;
  padding: 4px;
}
.uploadLabel{
  width: 100%;
  height: 100%;
  margin-bottom: 10px;
}
.uploadButton {
  background-color: indigo;
  color: white;
  padding: 0.5rem;
  font-family: sans-serif;
  border-radius: 0.3rem;
  cursor: pointer;
  margin-top: 1rem;
}
.video-preview {
  width: 100%;
  height: auto;
  margin-top: 20px;
}
</style>
