import json
import glob
import os
import blocks_util

files = glob.glob("pack/assets/minecraft/blockstates/*.json")
if files != []:
    blocks_util.write_animated_cube()
    blocks_util.write_geometry_cube()

for file in files:
    print(file)
    file = file.replace("\\", "/")
    block = (file.split("/")[-1]).replace(".json", "")  # <-- BLOCK NAME EXTRACTED
    if (block == "fire"): continue
    block_material = os.getenv("BLOCK_MATERIAL")
    blocks_util.write_mapping_block(block)
    with open(file, "r") as f:
        data = json.load(f)["variants"]
        #print(data)
        for k, v in data.items():
            if not("block/original" in v["model"] or "block/tripwire_attached_n" in v["model"]):
                print("KV:", k, v["model"])
                am = blocks_util.get_am_file(v["model"])
                print("AM", am)
                if am is not None:
                    with open(am, "r") as f:
                        print("am opening")
                        data_am = json.load(f)
                        gmdl = data_am["minecraft:attachable"]["description"]["identifier"].split(":")[1]
                        geometry = blocks_util.get_geometry_block(v["model"])
                        texture = blocks_util.create_terrain_texture(gmdl, data_am["minecraft:attachable"]["description"]["textures"]["default"])
                else:
                    print("Using block name for fallback")
                    gmdl = block  # <-- USE BLOCK NAME HERE
                    print("BLOCK", block)
                    geometry = blocks_util.get_geometry_block(v["model"])
                    print("GEOMETRY", geometry)
                    default_texture = f"textures/{model.split(':')[0]}/{model.split(':')[1]}"  # <-- FALLBACK PATH
                    print("DEFAULT TEXTURE", default_texture)
                    texture = blocks_util.create_terrain_texture(gmdl, default_texture)
                    print("TEXTURE", texture)
                
                #if geometry == "geometry.cube":
                    #with open(am, "w") as f:
                        #print("cubik")
                        #data_am["minecraft:attachable"]["description"]["geometry"]["default"] = "geometry.cube"
                        #data_am["minecraft:attachable"]["description"]["animations"] = {"thirdperson_main_hand":"animation.geo_cube.thirdperson_main_hand","thirdperson_off_hand":"animation.geo_cube.thirdperson_off_hand","thirdperson_head":"animation.geo_cube.head","firstperson_main_hand":"animation.geo_cube.firstperson_main_hand","firstperson_off_hand":"animation.geo_cube.firstperson_off_hand","firstperson_head":"animation.geyser_custom.disable"}
                        #json.dump(data_am, f)
                if block == "tripwire":
                    sstate = k.split(",")
                    k = f"{sstate[0]},{sstate[4]},{sstate[1]},{sstate[2]},{sstate[6]},{sstate[3]},{sstate[5]}"
                print("almost the end")

                print("BGKTBMG", block, gmdl, k, texture, block_material, geometry)
                blocks_util.regsister_block(block, gmdl, k, texture, block_material, geometry)
