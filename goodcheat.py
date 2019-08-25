import win32api
import win32gui
import win32process
import pymem
import sys
import os
import time
import unittest

print("Select operation.")
print("1.Add")
print("2.Subtract")
print("3.Multiply")
print("4.Divide")

# Take input from the user 
choice = "fsdf"

num1 = 5345
num2 = 763

if choice == '1':
    print(num1,"+",num2,"=", num1+num2)

elif choice == '2':
    print(num1,"-",num2,"=", num1-num2)

elif choice == '3':
    print(num1,"*",num2,"=", num1*num2)

elif choice == '4':
    print(num1,"/",num2,"=", num1/num2)
else:
       print("Invalid input")
        
# Offsets
local_offset = 0xCF4A4C
dwGlowObjectManager = 0x5247230
m_iGlowIndex = 0xA40C
m_iTeamNum = 0xF4
dwEntityList = 0x4D06DF4

# Get Process
handle = pymem.Pymem("csgo.exe")


# Client.dll
list_of_modules=handle.list_modules()
while(list_of_modules!=None):
    tmp=next(list_of_modules)
    if(tmp[0].name=="client_panorama.dll"):
        client_dll=tmp[1]
        break

# Local Player
local_player_ptr = handle.read_bytes(client_dll+local_offset,4)
local_player_ptr= int.from_bytes(local_player_ptr,byteorder='little')

glow_obj = handle.read_bytes(client_dll+dwGlowObjectManager,4)
glow_obj = int.from_bytes(glow_obj,byteorder='little')

# Actual Cheat
F6=win32api.GetKeyState(0x75)
while(win32api.GetKeyState(0x75)==F6):
    time.sleep(0.1)
    for i in range(32):
        entity = handle.read_bytes(client_dll+dwEntityList + i * 0x10,4)
        entity = int.from_bytes(entity,byteorder='little')
        if(entity!=0):
            team = handle.read_int(entity+m_iTeamNum)
            gindex=handle.read_int(entity+m_iGlowIndex)
            my_team= handle.read_int(local_player_ptr+m_iTeamNum)
            if(my_team != team):
                handle.write_float(glow_obj+((gindex*0x38)+0x4),3.0)
                handle.write_float(glow_obj+((gindex*0x38)+0x8),0.0)
                handle.write_float(glow_obj+((gindex*0x38)+0xc),0.0)
                handle.write_float(glow_obj+((gindex*0x38)+0x10),1.7)
            handle.write_uchar(glow_obj+((gindex*0x38)+0x24),1)
            handle.write_uchar(glow_obj+((gindex*0x38)+0x25),0)