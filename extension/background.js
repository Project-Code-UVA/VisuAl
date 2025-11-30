chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.images) {
        fetch('http://localhost:5000/upload_images', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ images: message.images })
        })
        .then(res => res.json())
        .then(data => {
            // Send predictions back to popup
            chrome.runtime.sendMessage({ predictions: data });
        })
        .catch(err => console.error(err));
    }
});
