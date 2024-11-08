# ##Text and Image
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import pandas as pd
import os
import shutil
import io
from PIL import Image
from preprocessing import preprocess_text
from augmentation import augment_text
from image_preprocessing import preprocess_image
from image_augmentation import augment_image
from fastapi.responses import HTMLResponse, FileResponse
from io import BytesIO

print("Starting FastAPI App...")
app = FastAPI()

app = FastAPI()

DATA_PATH = "data/"

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ["text/csv", "text/plain", "image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only CSV, TXT, JPEG, and PNG files are allowed")
    
    file_location = os.path.join(DATA_PATH, file.filename)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    return {"filename": file.filename}

def load_data(file_location: str) -> pd.DataFrame:
    if file_location.endswith(".csv"):
        df = pd.read_csv(file_location)
    elif file_location.endswith(".txt"):
        with open(file_location, 'r') as f:
            lines = f.readlines()
        df = pd.DataFrame(lines, columns=["Text"])
    else:
        raise ValueError("Unsupported file format")
    return df

def load_image(file_location: str) -> Image:
    with open(file_location, "rb") as f:
        img = Image.open(io.BytesIO(f.read()))
    return img

@app.get("/sample/")
def show_sample(filename: str):
    file_location = os.path.join(DATA_PATH, filename)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")

    if filename.endswith(".csv") or filename.endswith(".txt"):
        df = load_data(file_location)
        sample_data = df.head(5).to_dict(orient="records")
        return {"sample_data": sample_data}
    elif filename.endswith((".jpeg", ".png", ".jpg")):
        img = load_image(file_location)
        img.show()
        return {"message": "Image sample displayed."}
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

@app.get("/preprocess/")
def preprocess_file(filename: str):
    file_location = os.path.join(DATA_PATH, filename)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")

    if filename.endswith(".csv") or filename.endswith(".txt"):
        df = load_data(file_location)
        preprocessed_data = preprocess_text(df)
        preprocessed_data = preprocessed_data.to_dict(orient="records")
        return {"preprocessed_data": preprocessed_data}
    elif filename.endswith((".jpeg", ".png", ".jpg")):
        img = load_image(file_location)
        processed_img = preprocess_image(img)
        processed_img.show()
        return {"message": "Image preprocessed (converted to grayscale)."}
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

@app.get("/augment/")
def augment_file(filename: str):
    file_location = os.path.join(DATA_PATH, filename)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")

    if filename.endswith(".csv") or filename.endswith(".txt"):
        df = load_data(file_location)
        augmented_data = augment_text(df)
        augmented_data = augmented_data.to_dict(orient="records")
        return {"augmented_data": augmented_data}
    elif filename.endswith((".jpeg", ".png", ".jpg")):
        img = load_image(file_location)
        augmented_img = augment_image(img)
        augmented_img.show()
        return {"message": "Image augmented (rotated and brightened)."}
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")


@app.get("/")
def main():
    content = """
    <html>
        <head>
            <title>Data Processing Application</title>
            <style>
                /* Base Styles */
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                }

                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background: #f5f5f7;
                    color: #1d1d1f;
                    overflow: hidden;
                }

                /* Main Container */
                .container {
                    width: 100%;
                    max-width: 700px;
                    padding: 40px;
                    background: #ffffff;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                    text-align: center;
                    transition: transform 0.3s ease;
                }

                .container:hover {
                    transform: translateY(-5px);
                }

                h2 {
                    margin-bottom: 24px;
                    font-size: 32px;
                    font-weight: 600;
                    color: #333;
                }

                /* File Upload Area */
                .file-upload {
                    margin-bottom: 30px;
                }

                input[type="file"] {
                    display: none;
                }

                .custom-file-upload {
                    padding: 12px 20px;
                    color: #0071e3;
                    background: #e6e6e9;
                    border-radius: 8px;
                    border: 1px solid #d2d2d7;
                    cursor: pointer;
                    font-size: 16px;
                    transition: background 0.3s;
                }

                .custom-file-upload:hover {
                    background: #d8d8dd;
                }

                /* Action Buttons */
                button {
                    background-color: #0071e3;
                    color: #fff;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: 500;
                    margin: 10px;
                    transition: background-color 0.3s, transform 0.3s;
                }

                button:hover {
                    background-color: #005bb5;
                    transform: translateY(-2px);
                }

                /* Output Display */
                .output {
                    margin-top: 30px;
                    padding: 20px;
                    background-color: #f9f9fb;
                    border-radius: 10px;
                    color: #333;
                    font-size: 15px;
                    line-height: 1.6;
                    text-align: left;
                    max-height: 300px;
                    overflow-y: auto;
                    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
                }

                /* Responsive Design */
                @media (max-width: 768px) {
                    .container {
                        padding: 20px;
                    }

                    h2 {
                        font-size: 28px;
                    }

                    button {
                        font-size: 14px;
                        padding: 10px 18px;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Data Processing Application</h2>
                <form id="uploadForm" class="file-upload" enctype="multipart/form-data">
                    <label for="file" class="custom-file-upload">Choose File</label>
                    <input type="file" id="file" name="file" accept=".csv, .txt, .jpeg, .jpg, .png" required>
                    <button type="button" onclick="uploadFile()">Upload File</button>
                </form>
                <button onclick="showSample()">Show Sample</button>
                <button onclick="showPreprocessed()">Show Preprocessed Data</button>
                <button onclick="showAugmented()">Show Augmented Data</button>
                <div id="output" class="output">Output will appear here...</div>
            </div>
            
            <script>
                let filename = "";

                async function uploadFile() {
                    const formData = new FormData(document.getElementById('uploadForm'));
                    const response = await fetch('/upload/', {
                        method: 'POST',
                        body: formData
                    });
                    const result = await response.json();
                    filename = result.filename;
                    document.getElementById("output").innerHTML = "<b>File uploaded:</b> " + filename;
                }

                async function showSample() {
                    if (!filename) return alert("Please upload a file first.");
                    const response = await fetch(`/sample/?filename=${filename}`);
                    const result = await response.json();

                    if (result.sample_data) {
                        let sampleHtml = "<b>Sample Data:</b><br>";
                        result.sample_data.forEach(row => {
                            sampleHtml += `<p>${row.Text || ""}</p>`;
                        });
                        document.getElementById("output").innerHTML = sampleHtml;
                    } else {
                        document.getElementById("output").innerHTML = result.message;
                    }
                }

                async function showPreprocessed() {
                    if (!filename) return alert("Please upload a file first.");
                    const response = await fetch(`/preprocess/?filename=${filename}`);
                    const result = await response.json();

                    if (result.preprocessed_data) {
                        let preprocessedHtml = "<b>Preprocessed Data:</b><br>";
                        result.preprocessed_data.forEach(row => {
                            preprocessedHtml += `<p>${row.Text || ""}</p>`;
                        });
                        document.getElementById("output").innerHTML = preprocessedHtml;
                    } else {
                        document.getElementById("output").innerHTML = result.message;
                    }
                }

                async function showAugmented() {
                    if (!filename) return alert("Please upload a file first.");
                    const response = await fetch(`/augment/?filename=${filename}`);
                    const result = await response.json();

                    if (result.augmented_data) {
                        let augmentedHtml = "<b>Augmented Data:</b><br>";
                        result.augmented_data.forEach(row => {
                            augmentedHtml += `<p>${row.Text || ""}</p>`;
                        });
                        document.getElementById("output").innerHTML = augmentedHtml;
                    } else {
                        document.getElementById("output").innerHTML = result.message;
                    }
                }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=content)



