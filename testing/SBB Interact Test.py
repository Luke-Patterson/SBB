from PIL import Image, ImageGrab
import os
import time
import pyautogui as pg
from time import sleep
from datetime import datetime
import win32gui
import cv2
import numpy as np
from skimage.metrics import structural_similarity
from scipy.signal import fftconvolve

# load hero images
start = time.time()
hero_imgs = {}
for hero in os.listdir('cards/raw/Heroes'):
    name = hero[:-4]
    img = cv2.imread('cards/raw/Heroes/'+hero)
    hero_imgs[name] = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)


# see if sbb is open
# identify which open window is storybook brawl
def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        num = hex(hwnd)
        name = win32gui.GetWindowText( hwnd )
        ctx.append(name)

result =[]
win32gui.EnumWindows( winEnumHandler, result )

try:
    sbb_index=result.index('Storybook Brawl')

except ValueError:
# if not, open storybook brawl
    file = 'C:/Users/Luke/Desktop/Storybook Brawl.url'
    os.system('"' + file + '"')

    sleep(5)

# if it is open, make it the active window
title=pg.getActiveWindowTitle()
if title!='Storybook Brawl':
    # identify which open window is storybook brawl

    result =[]
    win32gui.EnumWindows( winEnumHandler, result )

    #sbb_index=result.index('Storybook Brawl')

    # tab to storybook brawl
    pg.keyDown('alt')
    sleep(.2)
    for n in range(len(result)):
        for _ in range(n):
            pg.press('tab')
            sleep(.05)
        pg.press('enter')
        title=pg.getActiveWindowTitle()
        if title == 'Storybook Brawl':
            break

    pg.keyUp('alt')
    assert title == 'Storybook Brawl'

def screenGrab(bbox=None, save = False):
    box = ()
    if bbox!=None:
        im = ImageGrab.grab(bbox=bbox)
    else:
        im = ImageGrab.grab()
    if save:
        im.save(os.getcwd() + '/screenshots/full_snap__' + str(int(time.time())) +
            '.png', 'PNG')
    return im

#screenGrab()
# coordinates captured at 1920x1080 resolution, given at Physical
practice_brawl_coords = (1331, 640)

sleep(.5)
# click to start a practice brawl
pg.mouseDown(x=practice_brawl_coords[0], y=practice_brawl_coords[1])
sleep(.5)
pg.mouseUp(x=practice_brawl_coords[0], y=practice_brawl_coords[1])

# verify hero screen has loaded
hero_select_ref = cv2.imread("screenshots/reference/Hero Selection.png")
# see if there's a choose your hero banner in the top middle of the screen
hero_select_ref = hero_select_ref[159:319, 544:1414]
hero_select_ref = cv2.cvtColor(hero_select_ref, cv2.COLOR_BGR2GRAY)

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])

	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def verify_hero_screen(thresh = 200):
    curr_screen = screenGrab(bbox=(544,159,1414,319))
    curr_screen = cv2.cvtColor(np.array(curr_screen), cv2.COLOR_BGR2GRAY)
    diff = mse(curr_screen, hero_select_ref)
    return diff < thresh

while True:
    print('waiting for hero screen to load')
    sleep(.1)
    if verify_hero_screen():
        break


# better image comparison

def ssim(im1, im2, window, k=(0.01, 0.03), l=255):
    """See https://ece.uwaterloo.ca/~z70wang/research/ssim/"""
    # Check if the window is smaller than the images.
    for a, b in zip(window.shape, im1.shape):
        if a > b:
            return None, None
    # Values in k must be positive according to the base implementation.
    for ki in k:
        if ki < 0:
            return None, None

    c1 = (k[0] * l) ** 2
    c2 = (k[1] * l) ** 2
    window = window/numpy.sum(window)

    mu1 = fftconvolve(im1, window, mode='valid')
    mu2 = fftconvolve(im2, window, mode='valid')
    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = fftconvolve(im1 * im1, window, mode='valid') - mu1_sq
    sigma2_sq = fftconvolve(im2 * im2, window, mode='valid') - mu2_sq
    sigma12 = fftconvolve(im1 * im2, window, mode='valid') - mu1_mu2

    if c1 > 0 and c2 > 0:
        num = (2 * mu1_mu2 + c1) * (2 * sigma12 + c2)
        den = (mu1_sq + mu2_sq + c1) * (sigma1_sq + sigma2_sq + c2)
        ssim_map = num / den
    else:
        num1 = 2 * mu1_mu2 + c1
        num2 = 2 * sigma12 + c2
        den1 = mu1_sq + mu2_sq + c1


# define four hero's bounding boxes
hero_box_1 = (392, 724, 659, 779)

def identify_hero(bbox):
    curr_screen = screenGrab(bbox=bbox)
    curr_screen = cv2.cvtColor(np.array(curr_screen), cv2.COLOR_BGR2GRAY)

    for hero, img in zip(hero_imgs.keys(), hero_imgs.values()):
        score, diff = ssim(curr_screen, img)
        print("SSIM: {}".format(score))
        import pdb; pdb.set_trace()

identify_hero(hero_box_1)

# hero_box_2 = (, , , )
# hero_box_3 = (, , , )
# hero_box_4 = (, , , )

import pdb; pdb.set_trace()
