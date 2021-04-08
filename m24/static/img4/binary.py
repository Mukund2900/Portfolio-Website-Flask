import base64

with open("select-arrow.png","rb") as f:
    data = f.read()
data = base64.b64encode(data)

data = data.decode("UTF-8")
print(data)