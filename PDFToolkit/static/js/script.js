function convertPDFToJPG() {
    const fileInput = document.getElementById('pdfFileToJpg');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please upload a PDF file first.');
        return;
    }

    const formData = new FormData();
    formData.append('pdf', file);

    fetch('/convert_to_jpg', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.blob();
    })
    .then(blob => {
        const downloadLink = document.getElementById('downloadLinkJPG');
        downloadLink.href = URL.createObjectURL(blob);
        downloadLink.download = 'converted_images.zip';
        downloadLink.style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
}

function mergePDFs() {
    const fileInput = document.getElementById('pdfFilesToMerge');
    const files = fileInput.files;

    if (files.length === 0) {
        alert('Please upload PDF files first.');
        return;
    }

    const formData = new FormData();
    for (const file of files) {
        formData.append('files', file);
    }

    fetch('/merge', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.blob();
    })
    .then(blob => {
        const downloadLink = document.getElementById('downloadLinkMerge');
        downloadLink.href = URL.createObjectURL(blob);
        downloadLink.download = 'merged.pdf';
        downloadLink.style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
}

function convertPDFToDOCX() {
    const fileInput = document.getElementById('pdfFileToDocx');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please upload a PDF file first.');
        return;
    }

    const formData = new FormData();
    formData.append('pdf', file);

    fetch('/convert', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.blob();
    })
    .then(blob => {
        const downloadLink = document.getElementById('downloadLinkDOCX');
        downloadLink.href = URL.createObjectURL(blob);
        downloadLink.download = 'converted.docx';
        downloadLink.style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
}
