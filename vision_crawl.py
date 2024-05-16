import numpy as np
# prompt: read an image from a file and convert it so that the openai gpt can read it
from PIL import Image
import io
import base64
from openai import OpenAI
import json
import subprocess
def image_b64(file_path):
    with open(file_path, 'rb') as f:
      image_base64 = base64.b64encode(f.read()).decode('utf-8')
    return image_base64

first = True

while True:
    if first:
        prompt = f'''Answer this question: '{input("You: ")}'. Read carefully through the page before saying there is no information, else do not make things up but reply 'ANSWER_NOT_FOUND' please!'''

        with open('key.txt', 'r') as file:
            api_key = file.read().strip().split('=')[1].strip()
        model = OpenAI(api_key=api_key)
        messages = [
            {
                "role": "system",
                "content": '''You are a web crawler. Find a direct URL that likely contains answer to the user's question in this JSON format: {\"url\": \"<your url here\"}''',
            },
            {
                "role": "user",
                "content": prompt,
            }
        ]
    response = model.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        max_tokens=1024,
        #   temperature=0.9,
            response_format={"type": "json_object"},
    )
    message = response.choices[0].message
    # print("\n\n",message,"\n\n")
    # try:
    message_json = json.loads(message.content)
    # except:
    # print(f"\n|||{message.content}|||\n")
    url = message_json["url"]
    print(f"Crawling {url}")
    subprocess.run(["node", "screenshot.js", url])
    b64_image = image_b64("screenshot.jpg")
    response = model.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {"role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{b64_image}",
                },
            },
            {
                "type": "text",
                "text": prompt,
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
    print(f"GPT: {message_text}")
    if 'ANSWER_NOT_FOUND' not in message_text:
        messages.append({
            "role": "user",
            "content": "I was unable to crawl that site. Please send me a different URL please!",
        })
        first = False
        break
