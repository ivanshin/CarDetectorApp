#for debug only
import sys
sys.path.append('D:\\Projects\\Python\\CarDetector')

import io
import uvicorn
import base64
import numpy as np
from PIL import Image
from datetime import datetime
from fastapi import FastAPI, File, Request, UploadFile, Response
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from model_utils import model_utils as mu
from matplotlib import pyplot as plt
import json


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEVICE = mu.choose_device()
MODEL = mu.init_model(DEVICE)



app.mount("/static", StaticFiles(directory="webp", html=True), name="ui")
templates = Jinja2Templates(directory="webp")
#@app.get("/")
#def index():
#    return FileResponse('webp/index.html')

@app.route('/home')
async def renderReactApp(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
def upload_image(file: UploadFile ):
    # try read uploaded file and process
    try:
        contents = file.file.read()
        stream = io.BytesIO(contents)
        image = Image.open(stream)
        rgb_im = image.convert('RGB')
        tiles = mu.cut_tiles(rgb_im)

        result = []
        for tile in tiles:
            mask = mu.process_image(MODEL, tile, DEVICE)
            result.append(mu.add_mask(tile, mask))

        #mask = mu.process_image(MODEL, rgb_im, DEVICE)
        #result = mu.add_mask(image, mask)
    finally:
        file.file.close()

    result = mu.build_image_from_tiles(result)

    # get timestamp utc
    #now = datetime.utcnow()
    #timestamp_utc = (now - datetime(1970,1,1)).total_seconds()
    #plt.imsave(f'res_{ timestamp_utc }.png', result)
    img = Image.fromarray(result.astype("uint8"))
    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    #rawBytes.seek(0)
    ##print(img_base64)
    ##print(Response(content=json_str, media_type='application/json').body)
    my_string = base64.b64encode(rawBytes.getvalue())
    return Response(content=my_string, media_type='image/png')

    #my_string = base64.b64encode(result).decode('utf-8')
    #response = {}
    #response['image'] = my_string
    #response = json.dumps(response)
    #
    #return response

if __name__ == "__main__":
    uvicorn.run(app= 'app.main:app', host="0.0.0.0", port=8000, reload= True)