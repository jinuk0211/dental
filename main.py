import random
import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
# uvicorn main:app --reload
# Initialize the FastAPI app
app = FastAPI(
    title="Oral Health Check API",
    description="API for analyzing oral health images.",
    version="1.0.0"
)

# --- CORS Middleware ---
# This allows your HTML/JS frontend to communicate with this backend.
# The "*" allows all origins, which is fine for development.
# For production, you should restrict it to your frontend's actual domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --- Model Inference Logic ---
# In a real-world application, you would load your trained model here (e.g., TensorFlow, PyTorch).
# For this example, we will simulate the model's behavior.

def get_prediction(image_bytes: bytes):
    """
    Simulates an AI model inference process.
    
    Args:
        image_bytes: The byte content of the uploaded image.
        
    Returns:
        A dictionary containing the analysis result.
    """

    try:
        image = Image.open(io.BytesIO(image_bytes))
        # You could add size validation, e.g., image.size
    except Exception as e:
        # If the file is not a valid image, raise an error
        raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")

    possible_results = [
        {
            "status": "Healthy",
            "icon": "✅",
            "description": "Your oral health looks good! Keep up the excellent care.",
            "css_class": "result-healthy"
        },
        {
            "status": "Needs Attention",
            "icon": "⚠️",
            "description": "Some areas may need care. Consider visiting your dentist soon.",
            "css_class": "result-attention"
        },
        {
            "status": "Requires Care",
            "icon": "🚨",
            "description": "Please see a dentist as soon as possible for proper care.",
            "css_class": "result-risk"
        }
    ]
# model.eval()
# y_true, y_pred = [], []
# with torch.no_grad():
#     for images, labels in test_loader:
#         images, labels = images.to(device), labels.to(device)
#         outputs = model(images)
#         _, predicted = torch.max(outputs, 1)
#         y_true.extend(labels.cpu().numpy())
#         y_pred.extend(predicted.cpu().numpy())

# # Metrics
# accuracy = accuracy_score(y_true, y_pred)
# precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='macro')

# # Classification Report
# report = classification_report(y_true, y_pred, target_names=train_dataset.dataset.classes)    
    
    # Randomly select one of the results to simulate the model's output
    prediction = random.choice(possible_results)
    
    return prediction

# --- API Endpoint Definition ---

@app.get("/")
def read_root():
    """A simple endpoint to confirm the server is running."""
    return {"message": "Welcome to the Oral Health Check API"}

@app.post("/analyze/")
async def analyze_oral_image(file: UploadFile = File(...)):
    """
    Receives an uploaded image, runs the analysis, and returns the result.
    
    Args:
        file: An image file uploaded by the user.
        
    Returns:
        A JSON response with the prediction result.
    """
    # Ensure the uploaded file is an image
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
    
    # Read the content (bytes) of the uploaded file
    image_bytes = await file.read()
    
    # Get the simulated prediction from our function
    prediction_result = get_prediction(image_bytes)
    
    return prediction_result

# --- To run the server ---
# Open your terminal in the same directory as this file and run:
# uvicorn main:app --reload