import json
from datetime import datetime
import cv2
import numpy
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def overlay(img_maino, img_overlay, pos: tuple = (0, 0)):
    '''
    Overlay function to blend an overlay image onto a main image at a specified position.

    :param img_main (numpy.ndarray): The main image onto which the overlay will be applied.
    :param img_overlay (numpy.ndarray): The overlay image to be blended onto the main image.
                                        IMREAD_UNCHANGED.
    :param pos (tuple): A tuple (x, y) representing the position where the overlay should be applied.

    :return: img_main (numpy.ndarray): The main image with the overlay applied in the specified position.
    '''
    img_main = img_maino.copy()
    if img_main.shape[2] == 4:
        img_main = cv2.cvtColor(img_main, cv2.COLOR_RGBA2RGB)

    x, y = pos
    h_overlay, w_overlay, _ = img_overlay.shape
    h_main, w_main, _ = img_main.shape

    x_start = max(0, x)
    x_end = min(x + w_overlay, w_main)
    y_start = max(0, y)
    y_end = min(y + h_overlay, h_main)

    img_main_roi = img_main[y_start:y_end, x_start:x_end]
    img_overlay_roi = img_overlay[(y_start - y):(y_end - y), (x_start - x):(x_end - x)]

    if img_overlay.shape[2] == 4:
        img_a = img_overlay_roi[:, :, 3] / 255.0
        img_rgb = img_overlay_roi[:, :, :3]
        img_overlay_roi = img_rgb * img_a[:, :, np.newaxis] + img_main_roi * (1 - img_a[:, :, np.newaxis])

    img_main_roi[:, :] = img_overlay_roi

    return img_main


def create_img():
    img = np.full((2, 24 * 60 * 60, 3), (255, 255, 255), dtype=np.uint8)
    for i in range(24 * 60 * 60):
        if (i % (2 * 60 * 60)) < 60 * 60:
            img[1, i] = 166, 118, 122
        else:
            img[1, i] = 214, 152, 157
    return img


def run():
    with open('data.json') as f:
        dic = json.loads(f.read())
    at = [datetime.fromtimestamp(timestamp) for timestamp in dic['time']]
    av = dic['result']

    img_dict = {}
    for dt, v in zip(at, av):
        ymd = f'{dt.year}-{dt.month}-{dt.day}'
        if ymd not in img_dict.keys():
            img_dict[ymd] = {'img': create_img(), 'second': 0}
        x = (dt - datetime.strptime(ymd, '%Y-%m-%d')).total_seconds()
        x = int(x)
        if v:
            img_dict[ymd]['img'][0, x] = 0, 255, 0
            img_dict[ymd]['second'] += 1
        else:
            img_dict[ymd]['img'][0, x] = 0, 0, 255

    return img_dict


def show_all_res():
    img_dict = run()
    for k, v in img_dict.items():
        img = v['img']
        second = v['second']
        img = img[:, 28800:72000]
        v['show'] = cv2.resize(img, (0, 0), fx=0.03, fy=10, interpolation=cv2.INTER_NEAREST)

    mix_image = None
    for k, v in img_dict.items():
        image_pil = Image.new('RGB', (1500, 100), (200, 200, 200))
        draw = ImageDraw.Draw(image_pil)
        for i in range(8, 21):
            font = ImageFont.truetype('Roboto-Medium.ttf', 12)
            draw.text((177 + 107 * (i - 8), 55), f'{i}', font=font, fill=(0, 0, 0))

        font = ImageFont.truetype('Roboto-Medium.ttf', 25)
        draw.text((30, 15), f'{k}', font=font, fill=(0, 0, 0))
        draw.text((30, 45), f"{round(v['second'] / 60, 1)} min", font=font, fill=(0, 0, 0))

        image_np = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        image_np = overlay(image_np, v['show'], (170, 25))

        if mix_image is not None:
            mix_image = np.vstack((mix_image, image_np))
        else:
            mix_image = image_np

    cv2.imshow(f'show all result', mix_image)
    cv2.imwrite('show all result.png', mix_image)


if __name__ == '__main__':
    show_all_res()
    cv2.waitKey(0)
