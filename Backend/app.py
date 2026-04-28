from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import torch.nn.functional as F

# Initialise the app
app = FastAPI(title="Restaurant Review BERT API", version="1.0")

# Define the request payload structure
class TextRequest(BaseModel):
    text: str

# Load the fine-tuned model and tokenizer from your local directory
MODEL_NAME = "./model/" 
print(f"Loading model from {MODEL_NAME}...")
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
# Notice we are using BertForSequenceClassification now, not AutoModel!
model = BertForSequenceClassification.from_pretrained(MODEL_NAME)

# Move model to the GPU if you've got one available (makes inference lightning fast)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval() # Set to evaluation mode

@app.post("/predict")
async def predict_rating(request: TextRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Review text cannot be empty.")

    try:
        # --- 1. PRE-PROCESSING ---
        # Tokenise the input text exactly as you did in cell 13 of your notebook
        inputs = tokenizer(
            request.text, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=128 
        )
        
        # Move inputs to the same device as the model
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # --- 2. INFERENCE ---
        with torch.no_grad():
            outputs = model(**inputs)
        
        # --- 3. POST-PROCESSING ---
        # Get the raw scores (logits) and convert them to probabilities using Softmax
        logits = outputs.logits
        probabilities = F.softmax(logits, dim=-1)
        
        # Find the class with the highest probability (0 to 4)
        predicted_class = torch.argmax(probabilities, dim=-1).item()
        
        # Map the 0-4 class back to a 1-5 Star Rating, just like in your notebook
        predicted_rating = predicted_class + 1
        
        # Grab the confidence percentage for the winning class
        confidence = probabilities[0][predicted_class].item() * 100
        
        # Return a beautifully formatted JSON response
        return {
            "review": request.text, 
            "predicted_rating": f"{predicted_rating} Stars",
            "confidence_score": round(confidence, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)