import numpy as np
# prompt: read an image from a file and convert it so that the openai gpt can read it

from PIL import Image
import io
import base64
from openai import OpenAI

def image_b64(file_path):
    with open(file_path, 'rb') as f:
        # image_bytes = f.read()

      # Convert the image to base64
      image_base64 = base64.b64encode(f.read()).decode('utf-8')
    return image_base64
b64_image = image_b64("image.jpg")
with open('key.txt', 'r') as file:
    api_key = file.read().strip().split('=')[1].strip()
model = OpenAI(api_key=api_key)
response = model.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {"role": "user",
     "content": [
         {
             "type": "image_url",
             "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"
                           #"/content/drive/MyDrive/Personal_Project_Data/image.jpg"
             },#f"data:base64,image/jpeg;{b64_image}",
         },
         {
             "type": "text",
             "text": "What is the image about?",
         }
     ]
    }
  ],
  max_tokens=128,
  temperature=0.9,
)
# print(response)
message = response.choices[0].message
message_text = message.content
print(message_text)