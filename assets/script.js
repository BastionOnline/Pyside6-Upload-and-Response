let backend;

// Setup WebChannel
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
        //  PySide automatically passes those values to your Python method receiveFile
        backend.receiveFile(file.name, content);
    };
    reader.readAsText(file);
}


// function downloadThankYou() {
//     if (backend && backend.downloadThankYouFile) {
//         backend.downloadThankYouFile();
//     }
// }
