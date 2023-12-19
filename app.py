import os
from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import numpy as np


app = Flask(__name__)

#load model
model = load_model('Model_tanpa_self_learning.h5')
tokenizer = Tokenizer()
label_encoder = LabelEncoder()
learning_type = ["Visual", "Auditory", "Kinesthetic"]
y = label_encoder.fit_transform(learning_type)

def model_prediction(model, Sentence):
    tokenizer.fit_on_texts(Sentence)
    input_sequence = tokenizer.texts_to_sequences(Sentence)
    input_padded = pad_sequences(input_sequence)
    prediction = model.predict(input_padded)
    predicted_labels = [learning_type[np.argmax(pred)] for pred in prediction]
    return predicted_labels[0]

#fetching api
@app.route("/")
def index():
    return jsonify({
        "status": {
            "code" : 200,
            "message" : "success fetching api"
        },
        "data": None
    }), 200

#prediction route
@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        # Handle the POST request
        json_data = request.get_json()
        sentence = json_data["sentence"]
        if sentence:
            predicted_style = model_prediction(model, sentence)
            return jsonify({
                "status": {
                    "code": 200,
                    "message": "Success predicting",
                },
                "data": {
                    "learning_type_result": predicted_style,
                }
            }), 200
        else:
            return jsonify({
                "status": {
                    "code": 400,
                    "message": "Bad Request"
                },
                "data": None
            }), 400
    else:
        return jsonify({
            "status": {
                "code": 405,
                "message": "Method Not Allowed"
            },
            "data": None
        }), 405
    
if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8080)))
