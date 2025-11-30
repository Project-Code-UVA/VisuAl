console.log("Content script is running!");

// Find all images on the page
const images = document.querySelectorAll("img");

// Convert an image to base64
async function imageToBase64(img) {
    return new Promise((resolve, reject) => {
        try {
            const canvas = document.createElement("canvas");
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0);
            resolve(canvas.toDataURL("image/png"));
        } catch (err) {
            reject(err);
        }
    });
}

// Attach a floating badge to each image
function attachBadges(imgElements, predictions) {
    imgElements.forEach((img, idx) => {
        const pred = predictions[idx];
        if (!pred || !pred.prediction) return;

        // Correct property access!
        const fakeScore = Number(pred.prediction.fake) || 0;

        // Ensure valid container
        const parent = img.parentElement;
        let container;

        if (!parent || getComputedStyle(parent).position === "static") {
            container = document.createElement("div");
            container.style.position = "relative";
            container.style.display = "inline-block";
            parent.insertBefore(container, img);
            container.appendChild(img);
        } else {
            container = parent;
            if (getComputedStyle(container).position === "static") {
                container.style.position = "relative";
            }
        }

        // Badge UI
        const badge = document.createElement("div");
        badge.textContent = `AI: ${(fakeScore * 100).toFixed(1)}%`;
        badge.style.position = "absolute";
        badge.style.top = "5px";
        badge.style.right = "5px";
        badge.style.padding = "4px 8px";
        badge.style.background = "rgba(0,0,0,0.75)";
        badge.style.color = "white";
        badge.style.fontSize = "12px";
        badge.style.borderRadius = "4px";
        badge.style.zIndex = "99999";
        badge.style.pointerEvents = "none";

        container.appendChild(badge);
    });
}

// Send images to Flask server and get predictions
async function sendImagesToServer() {
    const imageList = Array.from(images);
    if (imageList.length === 0) return;

    const base64Images = [];
    for (const img of imageList) {
        try {
            const b64 = await imageToBase64(img);
            base64Images.push(b64);
        } catch (e) {
            console.error("Failed to convert image:", e);
        }
    }

    try {
        const response = await fetch("http://localhost:5000/upload_images", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ images: base64Images })
        });

        const result = await response.json();
        console.log("Predictions:", result);

        // Ensure result is an array matching imageList
        const predictionsArray = Array.isArray(result) ? result : [result];

        attachBadges(imageList, predictionsArray);

    } catch (e) {
        console.error("Error sending images to server:", e);
    }
}

// Run it
sendImagesToServer();
