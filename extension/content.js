console.log("Content script is running!");

// Find all images on the page
const images = document.querySelectorAll("img");

// Convert each image to base64
async function imageToBase64(img) {
    return new Promise((resolve) => {
        const canvas = document.createElement("canvas");
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);
        resolve(canvas.toDataURL("image/png")); // works because images are same-origin
    });
}

// Send images to Flask server
async function sendImagesToServer() {
    const base64Images = [];
    for (const img of images) {
        try {
            const b64 = await imageToBase64(img);
            base64Images.push(b64);
        } catch (e) {
            console.log("Failed to convert image:", e);
        }
    }

    if (base64Images.length === 0) return;

    try {
        const response = await fetch("http://localhost:5000/upload_images", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ images: base64Images })
        });
        const result = await response.json();
        console.log("Predictions:", result);
    } catch (e) {
        console.log("Error sending images to server:", e);
    }
}

// Run it
sendImagesToServer();
