from fastapi import FastAPI
import os
from dotenv import load_dotenv
from models import SequenceInput
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

load_dotenv()
HF_TOKEN = os.getenv('HF_TOKEN')
app = FastAPI()

MODEL_NAME = "NakornB/distilESM-2-AMP"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

@app.get('/')
def read_root():
    return {"message" :f"DistilESM-AMP is ready for prediction."}

@app.post("/predict")
def predict(input_data: SequenceInput):
    input = tokenizer(input_data.sequence, return_tensors='pt')
    with torch.no_grad():
        logits = model(**input).logits

    probabilities = torch.softmax(logits, dim=1) 
    pred_class = torch.argmax(probabilities, dim=1).item() 

    amp_prob = probabilities[0, 1].item()
    non_amp_prob = probabilities[0, 0].item()

    AMP_class = "AMP" if pred_class == 1 else "Non-AMP"
    confidence = amp_prob if pred_class == 1 else non_amp_prob

    return {"prediction": AMP_class, "confidence": confidence}
def main():
    print("Hello from backend!")


if __name__ == "__main__":
    main()


