from PIL import Image
import json
import glob
import os
files = glob.glob("staging/target/rp/attachables/modelengine/**/*.json")
fdone = []
for file in files:
    if not file in fdone:
        try:
            with open(file, "r") as f:
                texture_file = json.load(f)["minecraft:attachable"]["description"]["textures"]["default"]
                texture = f"staging/target/rp/{texture_file}.png"
            im = Image.open(texture).convert("RGBA")
            im.putalpha(51)
            pixels = im.load()
            for x in range(im.height):
                for y in range(im.width):
                    if pixels[x,y] == (0,0,0,51):
                        pixels[x,y] = (0,0,0,0)
            im.save(texture)
            fdone.append(file)
        except Exception as e:
            print(e)
            print("Error texture:" + texture)