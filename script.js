function createMontage() {
    const fileInput = document.getElementById('fileInput');
    const montageContainer = document.getElementById('montageContainer');
    montageContainer.innerHTML = '';  // Clear previous montage

    const files = fileInput.files;

    if (files.length === 0) {
        alert('Please upload some photos!');
        return;
    }

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
}
