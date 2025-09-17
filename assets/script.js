let backend;

new QWebChannel(qt.webChannelTransport, function(channel) {
    backend = channel.objects.backend;
});

function sendFile() {
    const input = document.getElementById("fileInput");
    if (input.files.length === 0) return alert("Select a file!");

    const file = input.files[0];
    const reader = new FileReader();
    reader.onload = function() {
        const content = reader.result;
        // Send content to Python
        backend.receiveFile(file.name, content);
    };
    reader.readAsText(file);
}

// let thankYouContent = ""

// // This function is called from Python to set the thank-you text
// function setThankYouFile(content) {
//     thankYouContent = content;
//     document.getElementById("downloadBtn").disabled = false; // enable the download button
// }

// // Trigger download when the user clicks the button
// function triggerDownload() {
//     if (!thankYouContent) return;
//     const blob = new Blob([thankYouContent], { type: 'text/plain' });
//     const link = document.createElement('a');
//     link.href = URL.createObjectURL(blob);
//     link.download = "thank_you.txt";
//     document.body.appendChild(link);
//     link.click();
//     link.remove();
//     URL.revokeObjectURL(link.href);
// }

// function downloadFile(filename, content) {
//     const blob = new Blob([content], { type: 'text/plain' });
//     const link = document.createElement('a');
//     link.href = URL.createObjectURL(blob);
//     link.download = filename;
//     document.body.appendChild(link);
//     link.click();
//     link.remove();
//     URL.revokeObjectURL(link.href);
// }