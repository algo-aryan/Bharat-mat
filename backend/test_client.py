import requests

payload = {
    "question": "explain the formula for positoonal encoding explain each part",
    "pdf_url": "https://arxiv.org/pdf/1706.03762.pdf"
}

res = requests.post("http://127.0.0.1:5000/chat", json=payload)
print(res.status_code)
print(res.text)

print(res.json())
