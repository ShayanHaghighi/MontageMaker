const { createFFmpeg, fetchFile } = FFmpeg;
const ffmpeg = createFFmpeg({ log: true });


var selectedImages = [];

function handleFiles(files) {
    const file = files[0]
    const montageContainer = document.getElementById('montageContainer');
    console.log("files: ");
    // console.log(file);


        const reader = new FileReader();

        reader.onload = function(event) {
            const img = document.createElement('img');
            img.src = event.target.result;
            montageContainer.appendChild(img);
        }

        reader.readAsDataURL(file);
        selectedImages.push(file);
        console.log(selectedImages)
}

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
        const imageName = `image${i}.png`;
        ffmpeg.FS('writeFile', imageName, await fetchFile(files[i]));
        console.log(`Image written: ${imageName}`);
    }

    try {
        // Create video from images, each lasting 3 seconds
        await ffmpeg.run(
            '-framerate', '1/3',        // Each frame (image) lasts 3 seconds
            '-i', 'image%d.png',        // Input pattern for images
            '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',  // Ensure dimensions are even
            '-c:v', 'libx264',          // Video codec
            '-r', '30',                 // Output frame rate
            '-pix_fmt', 'yuv420p',      // Pixel format
            'output.mp4'                // Output file name
        );

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
    } catch (e) {
        console.error('FFmpeg error:', e);
    }
}