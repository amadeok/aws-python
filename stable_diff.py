import json
import requests, random
import io
import base64
from PIL import Image, PngImagePlugin

url = "http://127.0.0.1:7860"

payload = {
}
_response = requests.get(url=f'{url}/sdapi/v1/sd-models', json=payload)
_response.text
r = _response.json()

for i in r:
    print(i["title"])

url = "http://127.0.0.1:7860"
i = random.choice(r)["title"]
option_payload = {
    "sd_model_checkpoint": i,
    "CLIP_stop_at_last_layers": 2
}

response = requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)


response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)


r = response.json()

for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    png_payload = {
        "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    image.save('output.png', pnginfo=pnginfo)


    # https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API
# pip3 install Pillow

import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin

url = "??? put your colab web server URL here"

sample = {
  "enable_hr": False,
  "denoising_strength": 0,
  "firstphase_width": 0,
  "firstphase_height": 0,
  "prompt": "",
  "styles": ["string"],
  "seed": -1,
  "subseed": -1,
  "subseed_strength": 0,
  "seed_resize_from_h": -1,
  "seed_resize_from_w": -1,
  "sampler_name": "string",
  "batch_size": 1,
  "n_iter": 1,
  "steps": 50,
  "cfg_scale": 7,
  "width": 512,
  "height": 512,
  "restore_faces": False,
  "tiling": False,
  "negative_prompt": "string",
  "eta": 0,
  "s_churn": 0,
  "s_tmax": 0,
  "s_tmin": 0,
  "s_noise": 1,
  "override_settings": {},
  "override_settings_restore_afterwards": True,
  "sampler_index": "Euler"
}


payload = {
    "prompt": "Close up of a warrior with helmet and armour on flying dragon by Mobius Jean Giraud",
    "steps": 15,
    "negative_prompt": "3D, ugly, deformed",
    "sampler_name": "DPM++ SDE Karras",
    "cfg_scale": 7,
    "seed": 3,
    "width":640,
    "height":896
}


outputFilename = payload["prompt"].replace(':','_').replace(',', '').replace('  ', ' ').replace(' ', '.')[:100] + '.' + str(payload["seed"]) + '.' + str(payload["width"]) + 'x' + str(payload["height"]) + ".png"


response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

print("Sending request.")
r = response.json()
print("Got response")

for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    png_payload = {
        "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    print(outputFilename)
    image.save(outputFilename, pnginfo=pnginfo)