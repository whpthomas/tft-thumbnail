#!/usr/bin/python
# TFT Thumbnail for Two Trees Sapphire Pro/Plus (and MKS Robin Nano TFT35)
# This is a Prusa Slicer post processor that generates compatible preview images.
# It is released under the terms of the AGPLv3 or higher.
# 2022/10/5 Initial release @whpthomas

# Config: Marlin 2, 100x100, 200x200, PNG GCODE Thumbnails
# Post-Processing Script: /path/to/python3 /path/to/script/tft-thumbnail.py

import sys, os, io
import base64
import regex # pip install regex
from os.path import exists
from io import BytesIO
from PIL import Image # pip install Image

#src: MKS-WIFI Uploader for Prusa Slicer : https://github.com/ArtificalSUN/MKS-WIFI_PS_uploader/blob/main/MKS_WIFI_PS_upload.pyw
#src: mks-wifi plugin : https://github.com/Jeredian/mks-wifi-plugin/blob/develop/MKSPreview.py

def rgb2tft(r, g, b):
    r = r >> 3
    g = g >> 2
    b = b >> 3
    rgb = (r << 11) | (g << 5) | b
    return '{:02x}'.format(rgb & 0xFF) + '{:02x}'.format(((rgb >> 8) & 0xFF))

def generate_tft(img):
    width, height = img.size
    if(width == 100):
        res = '\n;simage:'
    else:
        res = '\n;;gimage:'
    pixels = img.convert('RGB')
    for y in range(width):
        for x in range(height):
            r, g, b = pixels.getpixel((x,y))
            res += rgb2tft(r, g, b)
        res += '\nM10086 ;'
    return res

def convertPrusaThumb2TFTThumb(inputfile, outputfile): # .......... Replace PrusaSlicer's Thumbnails with TFT's Thumbnails
    if not exists(inputfile):
        return
    
    gcode_in = open(inputfile).read() # ............................................................. load entire gcode file
    
    #regex for parsing datas with grouped part (matched)
    s_pattern = '(?<=(; thumbnail begin )([0-9]+)(x)([0-9]+) ([0-9]+)\n)(.*?)(?=; thumbnail end)'
    pattern = regex.compile(s_pattern, regex.M|regex.I|regex.S )
    gcode_out = '; Postprocessed by tft-thumbnail plugin'

    for match in pattern.finditer(gcode_in): #....................................................... find both 100x100 and 200x200 thumbnails
        th_width  = match.group(2)
        th_height = match.group(4)
        th_size   = match.group(5)
        
        try:
            th_datas  = match.group(6) # ............................................................ get image datas (base64)
            th_datas = th_datas.replace('; ', '').replace('\n', '') # ............................... without carry returns, etc
            stream = BytesIO( base64.b64decode(th_datas) ) # ........................................ decoding base64
            image = Image.open(stream).convert("RGB") # ............................................. for converting into PIL image
            stream.close()
            gcode_out += generate_tft(image) # ...................................................... prepend PIL image to TFT GCode            
        except:
            pass
    
    try:
        s_pattern = '; thumbnail begin .*; thumbnail end' # ............. remove thumbnails form Prusa GCode and append to TFT GCode
        gcode_out = gcode_out + '\n' +  regex.sub( s_pattern, '', gcode_in, flags = regex.M|regex.I|regex.S )
        fileOut = open(outputfile, "w") 
        fileOut.write(gcode_out)
        fileOut.close()
    except:
        pass

    return

def main(argv):

    inputfile = ''
    outputfile = ''
    try:  
        inputfile = sys.argv[1]
        try:
            outputfile = sys.argv[2]
        except:
            outputfile = sys.argv[1]
    except:
        print('./tft-thumbnail infile [outfile]')
        sys.exit()
    convertPrusaThumb2TFTThumb(inputfile, outputfile)


if __name__ == "__main__":
   main(sys.argv[1:])
