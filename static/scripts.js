document.addEventListener('DOMContentLoaded', () => {
    const startRecordingButton = document.getElementById('startRecording');
    const stopRecordingButton = document.getElementById('stopRecording');
    const videoListElement = document.getElementById('videoList');

    startRecordingButton.addEventListener('click', () => {
        fetch('/start_recording')
            .then(response => response.json())
            .then(data => alert(data))
            .catch(error => console.error('Error starting recording:', error));
    });

    stopRecordingButton.addEventListener('click', () => {
        fetch('/stop_recording')
            .then(response => response.json())
            .then(data => {
                alert(data);
                updateVideoList();
            })
            .catch(error => console.error('Error stopping recording:', error));
    });

    function updateVideoList() {
        fetch('/list_videos')
            .then(response => response.json())
            .then(files => {
                videoListElement.innerHTML = '';
                files.forEach(file => {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `<a href="/video_storage/${file}" target="_blank">${file}</a>`;
                    videoListElement.appendChild(listItem);
                });
            })
            .catch(error => console.error('Error fetching video list:', error));
    }

    updateVideoList();
});
