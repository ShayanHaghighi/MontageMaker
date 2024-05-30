const { createFFmpeg, fetchFile } = FFmpeg;
const ffmpeg = createFFmpeg({ log: true });

async function createMontage() {
    const fileInput = document.getElementById('fileInput');
    const montageContainer = document.getElementById('montageContainer');
    montageContainer.innerHTML = '';  // Clear previous montage

    const files = fileInput.files;

    if (files.length === 0) {
        alert('Please upload some photos!');
        return;
    }

    // Display images
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const reader = new FileReader();

        reader.onload = function(event) {
            const img = document.createElement('img');
            img.src = event.target.result;
            montageContainer.appendChild(img);
        }

        reader.readAsDataURL(file);
    }

    // Load FFmpeg
    await ffmpeg.load();

    // Write images to FFmpeg FS
    for (let i = 0; i < files.length; i++) {
        ffmpeg.FS('writeFile', `image${i}.png`, await fetchFile(files[i]));
    }

    // Create video from images
    await ffmpeg.run('-framerate', '1', '-i', 'image%d.png', '-c:v', 'libx264', '-r', '30', '-pix_fmt', 'yuv420p', 'output.mp4');

    // Read the result
    const data = ffmpeg.FS('readFile', 'output.mp4');

    // Create a URL and download the video
    const videoURL = URL.createObjectURL(new Blob([data.buffer], { type: 'video/mp4' }));
    const a = document.createElement('a');
    a.href = videoURL;
    a.download = 'montage.mp4';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
