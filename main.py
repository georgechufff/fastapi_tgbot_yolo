import os

from fastapi import FastAPI, Request
import uvicorn
import aiohttp
import aiofiles
import requests
from ultralytics import YOLO
from shutil import rmtree

from tg_configurations.schemas import Answer
from tg_configurations.responses import responses

TG_API = os.getenv('TGA_API')
URL = os.getenv('URL')

r = requests.get(f'https://api.telegram.org/bot{TG_API}/setWebhook?url=https://{URL}')
print(r.json())


app = FastAPI()


@app.post('/')
async def read_root(request: Request):
    json = await request.json()
    obj = Answer.model_validate(json)
    print(obj)

    chat_id = obj.message.chat.id

    if obj.message.text:
        if obj.message.text in responses.keys():
            async with aiohttp.ClientSession() as session:
                async with session.post(f'https://api.telegram.org/bot{TG_API}/sendMessage',
                                        data={'chat_id': chat_id,
                                              'text': responses[obj.message.text]}) as response:
                    res = await response.json()

    elif obj.message.photo:
        file_id = obj.message.photo[-1].file_id
        data = {'file_id': file_id}

        print(os.listdir('.'))
        if 'runs' not in os.listdir('.'):
            os.makedirs('runs/detect/')

        async with aiohttp.ClientSession() as session:
            async with session.post(f'https://api.telegram.org/bot{TG_API}/getFile', data=data) as response:
                res_file_info = await response.json()
                print(res_file_info)
                if res_file_info.get('ok'):
                    path = res_file_info['result']['file_path']
                    ext = path.split('.')[-1]
                    async with session.get(f'https://api.telegram.org/file/bot{TG_API}/{path}', data=data) as dwfile:
                        async with aiofiles.open('./runs/detect/filename.png', mode='wb') as f:
                            content = await dwfile.read()
                            await f.write(content)

        model = YOLO(f'./model/yolov8n.pt')
        model.predict('./runs/detect/filename.png', conf=0.25, save=True)

        try:
            with open('./runs/detect/predict/filename.png', 'rb') as f:
                requests.post(f'https://api.telegram.org/bot{TG_API}/sendPhoto',
                              params={'chat_id': chat_id},
                              files={'photo': f, 'text': 'result'})
        except FileNotFoundError:
            async with aiohttp.ClientSession() as session:
                async with session.post(f'https://api.telegram.org/bot{TG_API}/sendMessage',
                                        data={'chat_id': chat_id,
                                              'text': responses['error']}) as response:
                    res = await response.json()

        if len(os.listdir('./runs/detect/predict')) > 0:
            rmtree('./runs/detect/predict')
        os.remove('./runs/detect/filename.png')

    return 200


if __name__ == "__main__":
    uvicorn.run('main:app', port=8080, host='0.0.0.0', reload=False)
