import cv2
from time import sleep
from ocr import check_photo
import subprocess
import numpy as np
import streamlink




def take_screenshot(video_url):
    streams = streamlink.streams(video_url)
    if 'best' in streams:
        stream_url = streams['best'].url
    else:
        raise Exception("No suitable stream found")

    command = [
        'ffmpeg',
        '-i', stream_url,
        '-vf', 'fps=1',
        '-f', 'image2pipe',
        '-pix_fmt', 'bgr24',
        '-vcodec', 'rawvideo', '-'
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    cap = cv2.VideoCapture(stream_url)
    ret, frame = cap.read()
    if ret:
        height, width, _ = frame.shape
    else:
        raise Exception("Unable to read video stream")

    cap.release()

    raw_image = process.stdout.read(width * height * 3)
    if len(raw_image) == width * height * 3:
        image = np.frombuffer(raw_image, np.uint8).reshape((height, width, 3))

        cv2.imwrite('code.png', image)
        print("get screenshot")
    else:
        print("Failed to capture image from the live stream.")

    process.terminate()


def stream_checker():
    stream_link = open("stream.link", "r").read()
    while True:
        try:
            take_screenshot(stream_link)
            res = check_photo()
            print(f'stream code ====> {res}')

            if not res == "none":
                blist = open("./stream.blacklist", "r").read().splitlines()
                if not res in blist:
                    with open("./code.txt", "w") as f:
                        f.write(res)
                    with open("./stream.blacklist", "a") as f:
                        f.write(res+"\n")

            sleep(10)
        except:
            pass


if __name__ == '__main__':
    stream_checker()
