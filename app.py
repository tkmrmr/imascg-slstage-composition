import cv2
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__, static_folder="./static/")

@app.route('/', methods=['GET', 'POST'])
def home():
    img_dir = "static/img/"
    gamma     = 1.18                            # γ値を指定
    img2gamma = np.zeros((256,1),dtype=np.uint8)
    for i in range(256):
        img2gamma[i][0] = 255 * (float(i)/255) ** (1.0 /gamma)
    if request.method == 'GET':
        img_path1 = None
        img_path2 = None
        img_path = None
    elif request.method == 'POST':
        stream1 = request.files['img1'].stream
        stream2 = request.files['img2'].stream
        img_array1 = np.asarray(bytearray(stream1.read()), dtype=np.uint8)
        img_array2 = np.asarray(bytearray(stream2.read()), dtype=np.uint8)
        img1 = cv2.imdecode(img_array1, 1)
        img1 = cv2.LUT(img1, img2gamma)
        img_path1 = img_dir + "img1.png"
        cv2.imwrite(img_path1, img1)
        img2 = cv2.imdecode(img_array2, 1)
        img2 = cv2.LUT(img2, img2gamma)
        img_path2 = img_dir + "img2.png"
        cv2.imwrite(img_path2, img2)
        # 画像処理
        img_line = img1[538:808, 1770:2433]
        dx = 1770
        dy = 538
        h, w = img_line.shape[:2]
        img2[dy:dy+h, dx:dx+w] = img_line

        img_hsv = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)

        img_hsv[:,:,(1)] = img_hsv[:,:,(1)]*1.25

        img_bgr = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR)
        img_bgr = cv2.LUT(img_bgr, img2gamma)

        img_path = img_dir + "img.png"
        cv2.imwrite(img_path, img_bgr)

    return render_template('index.html', img_path1=img_path1, img_path2=img_path2, img_path=img_path)

if __name__ == '__main__':
    app.run(host="0.0.0.0")