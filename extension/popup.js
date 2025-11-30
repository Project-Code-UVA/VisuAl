document.getElementById('getImagesBtn').addEventListener('click', async () => {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = "Collecting images...";

    // Get the active tab
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    // Inject content script to collect images
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content.js']
    });

    // Listen for background response
    chrome.runtime.onMessage.addListener(function listener(message, sender, sendResponse) {
        if (message.predictions) {
            resultsDiv.innerHTML = ""; // clear loading
            message.predictions.forEach(item => {
                const div = document.createElement('div');
                div.className = 'image-block';
                const urlP = document.createElement('p');
                urlP.textContent = item.url;
                div.appendChild(urlP);

                const ul = document.createElement('ul');
                item.predictions.forEach(([label, prob]) => {
                    const li = document.createElement('li');
                    li.textContent = `${label}: ${(prob*100).toFixed(1)}%`;
                    ul.appendChild(li);
                });
                div.appendChild(ul);
                resultsDiv.appendChild(div);
            });

            chrome.runtime.onMessage.removeListener(listener); // remove listener
        }
    });
});
