# main.py
import os
import time

from flask import Flask, jsonify, request
from llama_cpp import Llama

# --- Configuration ---
# IMPORTANT: Update this path to where you have stored your GGUF model file
MODEL_PATH = "XiYanSQL-QwenCoder-3B-2504.Q8_0.gguf"

# Set to a positive number to offload layers to the GPU.
# Use 0 to disable GPU and run on CPU only.
# Use -1 to offload all possible layers to the GPU.
N_GPU_LAYERS = -1

# --- End Configuration ---


# Initialize the Flask app
app = Flask(__name__)

# --- Model Loading ---
# Check if the model path is valid before starting the server
if not os.path.exists(MODEL_PATH):
    print(f"Error: Model file not found at '{MODEL_PATH}'")
    print(
        "Please update the MODEL_PATH variable in the script to the correct location of your GGUF model."
    )
    exit()

print("Loading model... This may take a few minutes.")
# Initialize the Llama model from the path
# This will offload layers to the Metal GPU on your M3 Mac
llm = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=N_GPU_LAYERS,
    n_ctx=32768,  # Context window size
    verbose=False,  # Set to True to see more detailed output from llama.cpp
)
print("Model loaded successfully.")

# Get the model name from the file path for the response
model_name = os.path.basename(MODEL_PATH)


# --- API Endpoint ---
@app.route("/chat/completions", methods=["POST"])
def chat_completions():
    """
    Handles chat completion requests, compatible with OpenAI's API structure.
    """
    try:
        # Get the JSON data from the request
        input_data = request.json

        # Extract parameters from the request
        messages = input_data.get("messages", [])
        temperature = input_data.get("temperature", 0.1)
        max_tokens = input_data.get("max_tokens", 1024)

        if not messages:
            return jsonify(
                {"error": "Request body must contain a 'messages' list."}
            ), 400

        print(
            f"\nReceived prompt. Generating completion for model: {model_name}."
        )

        # Call the Llama model to create a chat completion
        completion = llm.create_chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False,
            top_p=0.8,
        )

        # Add a check to ensure the response from the model is valid before processing
        if (
            not isinstance(completion, dict)
            or "choices" not in completion
            or len(completion.get("choices", [])) == 0
        ):
            error_message = f"Error: Invalid or empty response from model. Response: {completion}"
            print(error_message)
            return jsonify(
                {"error": "Failed to get a valid response from the model."}
            ), 500

        # The generated text is inside the 'choices' list in the response
        generated_text = completion["choices"][0]["message"]["content"]

        # Format the response to match the OpenAI API structure
        response = {
            "id": completion.get("id", f"chatcmpl-{int(time.time())}"),
            "object": "chat.completion",
            "created": completion.get("created", int(time.time())),
            "model": model_name,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": generated_text,
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": completion.get("usage"),
        }

        print(f"Generated Text: {generated_text}")
        return jsonify(response)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


# --- Main Execution ---
if __name__ == "__main__":
    # Note: This is a development server. For production, use a proper WSGI server like Gunicorn.
    print("Starting Flask server on http://0.0.0.0:5090")
    app.run(host="0.0.0.0", port=5090, debug=False)
