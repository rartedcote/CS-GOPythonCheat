import pymem
import pymem.process
import pyautogui
from pynput.keyboard import Key, Listener
import win32api

entity_list = (0x4D06DF4)
glowobject_manager = (0x5247230)
glow_index = (0xA40C)
team_num = (0xF4)
crosshair_id = 0xB3AC
local_offset = 0xCF4A4C
bhop_flags = 0x104
force_jump = 0x51AA4AC

triggerOn = True
bhopOn = True 
espOn = True

pm = pymem.Pymem("csgo.exe")

list_of_modules=pm.list_modules()
while(list_of_modules!=None):
    tmp=next(list_of_modules)
    if(tmp[0].name=="client_panorama.dll"):
        client=tmp[1]
        break

def triggerBot():
    while triggerOn:
        local_player = pm.read_int(client + local_offset)
        my_team = pm.read_int(local_player + team_num)
        inCrosshair = pm.read_int(local_player + crosshair_id)

        if inCrosshair != 0:
            entity_in_crosshair = pm.read_int(client + entity_list + ((inCrosshair - 1) * 0x10))
            team_entity = pm.read_int(entity_in_crosshair + team_num)

            if my_team != team_entity:
                pyautogui.click()
        break

def bunnyHop():
        while bhopOn:
            local_player = pm.read_int(client + local_offset)
            bhop_local_flag = pm.read_int(local_player + bhop_flags)

            if bhop_local_flag == 257 and win32api.GetAsyncKeyState(0x12):
                pm.write_int(client + force_jump, 6)
            break
            

def esp():

    while espOn:
        if pm.read_int(client + entity_list) > 0:  # Check if in-game.
            glow_manager = pm.read_int(client + glowobject_manager)

            for i in range(1, 32):  # Entities 1-32 are reserved for players. 
                entity = pm.read_int(client + entity_list + i * 0x10)

                if entity:
                    entity_team_id = pm.read_int(entity + team_num)
                    entity_glow = pm.read_int(entity + glow_index)

                    if entity_team_id == 2:  # Terrorist
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))   # R 
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # B
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow

                    elif entity_team_id == 3:  # Counter-terrorist
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))   # R
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # B
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow
        break

while True:
    bunnyHop()
    esp()
    triggerBot()