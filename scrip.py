import json
import requests
import os
import time

with open("abc.json", "r", encoding="utf8") as fs:
    data = json.loads(fs.read(), strict=False)

res = []
for item in data["data"]:
    if (
        item["xkname"] == "语文"
        and item["xk"] == "5661"
        and item["pubdate"].startswith("2022")
    ):
        res.append(item)

print(len(res))

for item in res:
    title = item["title"]
    os.makedirs(f"二年级语文课程/{title}", exist_ok=True)
    url = item["url"]
    docId = url.split("_")[1].split(".")[0]
    date = url.split("/")[-2]

    res = requests.get(f"https://zy.szedu.cn/login/getAppendixByid?docId={docId}")
    data = res.json()

    for i in data["data"]:
        name = i["name"]
        response = requests.get(
            f"https://zy.szedu.cn/jcjy/xx/enj/yw/{date}/{name}", stream=True
        )
        path = os.path.join(f"二年级语文课程/{title}", name)
        with open(path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        response.close()

    time.sleep(1)
    print(f"成功:{title}")
