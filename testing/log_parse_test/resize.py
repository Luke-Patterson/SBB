#!/usr/bin/python
from pathlib import Path

import os
import cv2

# https://drive.google.com/drive/folders/1bA-tChpvQj39tN_0_72e_vJRdph1M_gI
# before running this script, you need to downlaod the assets folder and place the art folder in the
# root directory of the repo, named "ALL SBB ART"
path = Path("../All SBB ART")
dirs = os.listdir(path)


def resize():
    for item in dirs:
        # if "Card art -" in item and os.path.isfile(path.joinpath(item)): # this is if its the wiki art
        if os.path.isfile(path.joinpath(item)):
            f, e = os.path.splitext(path.joinpath(item))

            # Load image and mask
            image = cv2.imread(f + '.png', cv2.IMWRITE_PNG_STRATEGY_RLE)
            mask = cv2.imread('..\\assets\\art_mask.png', cv2.IMWRITE_PNG_STRATEGY_RLE)

            # Resize art to mask size if smaller/larger
            if image.shape != mask.shape:
                width = int(mask.shape[1])
                height = int(mask.shape[0])
                dim = (width, height)
                image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            # apply the mask
            result = cv2.bitwise_and(image, mask)

            # transparent background
            tmp = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
            b, g, r = cv2.split(result)
            rgba = [b, g, r, alpha]
            result = cv2.merge(rgba, 4)

            # crop the image
            crop_img = result[2:2045, 219:1836]
            scale_percent = 10  # percent of original size
            width = int(crop_img.shape[1] * scale_percent / 100)
            height = int(crop_img.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(crop_img, dim, interpolation=cv2.INTER_AREA)

            # save
            cv2.imwrite('..\\cards\\' + item.replace("Card art - ", "").replace("'", "_"), resized)

resize()
