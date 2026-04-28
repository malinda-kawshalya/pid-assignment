# Restaurant Review Emotion & Rating API

## Overview
This backend application serves a fine-tuned BERT sequence classification model via a high-performance FastAPI endpoint. It is designed to take raw text from restaurant reviews, predict a 1 to 5-star rating, and map that rating to a specific customer emotion. This allows for automated, intelligent routing of customer feedback and dynamic promotional triggers.

## Application Layer Mapping
The core inference engine outputs a numeric rating. To make this actionable for the business logic, the application layer maps the predicted integer to a corresponding emotional state using the following structure:

```python
emotion_map = {
    5: 'Very Happy',
    4: 'Satisfied',
    3: 'Neutral',
    2: 'Sad',
    1: 'Frustrated'
}
```

## Prerequisites & Model Setup
**⚠️ CRITICAL STEP:** This application does not pull model weights from the internet at runtime. Before building or running the application, **the final model weights must be copied to the `model/` folder** in the root of this project.

Your directory structure should look exactly like this:
```text
Backend/
├── app.py
├── requirements.txt
├── Dockerfile
└── model/                  <-- MUST CONTAIN:
    ├── config.json
    ├── model.safetensors (or pytorch_model.bin)
    ├── vocab.txt
    └── tokenizer_config.json
```

## Running the API via Docker (Recommended)
Containerising the application ensures all PyTorch and transformer dependencies are perfectly isolated.

**1. Build the Docker Image**
Open your terminal in the root directory and run:
```bash
docker build -t restaurant-bert-api .
```

**2. Run the Container**
Once built, spin up the server and map it to port 8000:
```bash
docker run -p 8000:8000 restaurant-bert-api
```
*(Pro-tip: If you are updating the model weights frequently, you can mount the local directory to avoid rebuilding the image: `docker run -p 8000:8000 -v "$(pwd)/model:/app/model" restaurant-bert-api`)*

## API Usage & Testing

### 1. Swagger UI
FastAPI automatically generates an interactive documentation page. Once the server is running, simply navigate to:
**http://localhost:8000/docs**

### 2. Testing via Postman
You can easily stress-test the inference engine using Postman:

* **Method:** `POST`
* **URL:** `http://localhost:8000/predict`
* **Headers:** `Content-Type: application/json`
* **Body (raw JSON):**
  ```json
  {
      "text": "The cheese kottu was absolutely phenomenal, but the delivery driver was incredibly rude."
  }
  ```