import base64
import requests
import os

# OpenAI API Key
api_key = "YOUR_OPENAI_API_KEY"  # Replace with your actual API key

# Function to encode the image
def encode_image(image_path):
    """
    Encodes the image file to base64.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Directory containing the images
directory_path = "./pictures"

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check if the file is an image
        full_path = os.path.join(directory_path, filename)
        print(f"Processing {filename}...")

        # Getting the base64 string
        base64_image = encode_image(full_path)  # Corrected function name here

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Prepare the payload with the encoded image
        payload = {
            "model": "gpt-4-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Identify any books in the picture. Your output will be added to my card catalogue directly, so only output only the following information, with no extranious commentary: Book title: Book Author: Book Description: "
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 4000
        }

       # Make the request to the OpenAI API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        data = response.json()

        # Extracting text from the response
        response_text = data.get('choices', [])[0].get('message', {}).get('content', '')

        # Writing to a text file
        with open('library.txt', 'a') as file:
            file.write(f"\n--- Analysis for {filename} ---\n")
            file.write(response_text)
            file.write("\n")

        print(f"Data for {filename} has been written to library.txt.")
    else:
        print(f"Skipping {filename}, not an image.")

print("All images have been processed.")
