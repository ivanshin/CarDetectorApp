import os
import cv2 as cv
import numpy as np
from PIL import Image
from model.segnet import torch, SegNet


SHAPE_V = 500

def choose_device() -> torch.device:
    ''' Automatic choice cpu/gpu for model inference '''

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    return device


def init_model(device: torch.device) -> SegNet: 
    ''' Initialize model (SegNet) and load model weghts'''

    model = SegNet(3,2)
    model.load_state_dict(torch.load(os.path.join('model', 'model_weights_3.pth'), map_location= device))
    model = model.to(device)
    model.eval()
    return model


def process_image(model: SegNet,
                  image: Image,
                  device: torch.device) -> np.ndarray:
    ''' Process image throught SegNet'''

    image = np.asarray(image, dtype= np.float32)
    image = cv.resize(image, (224,224))
    image = torch.from_numpy(image)
    image = image / 255 / 255
    image = torch.permute(image, (2,0,1))
    image = torch.unsqueeze(image, dim=0)
    image = image.to(device)
    output = model(image)
    output = torch.squeeze(output)
    output = output * 255
    output = output.argmax(dim=0)
    output = output.to('cpu')
    output_np = cv.resize(np.uint8(output), (SHAPE_V, SHAPE_V))
    return output_np


def add_mask(image: Image, mask: np.ndarray) -> np.ndarray:
    ''' Blend original image with predicted mask '''

    original_image = image
    original_image = cv.resize(np.asarray(original_image), (SHAPE_V,SHAPE_V))
    output_np = cv.resize(np.uint8(mask), (SHAPE_V, SHAPE_V))
    image_seg = np.zeros((SHAPE_V, SHAPE_V, 3))
    image_seg = np.uint8(image_seg)

    colors = [[0, 0, 0], [255, 0, 0]] # red mask

    for c in range(2):
        image_seg[:, :, 0] += np.uint8((output_np == c)) * np.uint8(colors[c][0])
        image_seg[:, :, 1] += np.uint8((output_np == c)) * np.uint8(colors[c][1])
        image_seg[:, :, 2] += np.uint8((output_np == c)) * np.uint8(colors[c][2])

    image_seg = Image.fromarray(np.uint8(image_seg))
    old_image = Image.fromarray(np.uint8(original_image))
    
    image = Image.blend(old_image, image_seg, 0.3)

    # Remove background or empty class
    image_np = np.array(image)
    image_np[output_np == 0] = original_image[output_np == 0]
    return image_np


def cut_tiles(image: Image) -> np.ndarray:
    ''' Split image into n_tiles '''

    im = np.asarray(image)
    im = cv.resize(np.uint8(im), (SHAPE_V, SHAPE_V))
    M = im.shape[0]// 2
    N = im.shape[1]// 2
    tiles = [Image.fromarray(im[x:x+M,y:y+N]) for x in range(0,im.shape[0],M) for y in range(0,im.shape[1],N)]
    #print(tiles[0])
    return tiles


def build_image_from_tiles(tiles: list) -> np.ndarray:
    ''' Builds image from tiles '''
    
    concat_image_np = cv.vconcat([
        cv.hconcat([
            np.asarray(tiles[0]), np.asarray(tiles[1])
            ]), 
        cv.hconcat([
            np.asarray(tiles[2]), np.asarray(tiles[3])])
        ])
    return concat_image_np
