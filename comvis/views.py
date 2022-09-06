from asyncio.windows_events import NULL
from django.shortcuts import render
from django.http import HttpResponse
import cv2
import numpy as np
from pathlib import Path
from django_cv2.settings import BASE_DIR
from statistics import mean
import matplotlib.image as mimg

# Create your views here.


def index(request):
    return render(request, "index.html")


def pertemuan(request, id):

    rData = range(0, 3)
    res = getInfoImg(rData)

    data = {
        "results": res
    }

    return render(request, "pertemuan/pertemuan-"+id+".html", data)


def getInfoImg(rData):
    data = []
    for r in rData:
        res = processing(str(r)+".jpg", 5)
        i = 1
        strFormat = ""
        for items in res[0]:
            for colors in items:
                strFormat += "<tr><th>"+str(i)+"</th><td>"+str(colors[2])+"</td><td>"+str(
                    colors[1])+"</td><td>"+str(colors[0])+"</td></tr>"
                i += 1
        imgGray = getGrayImgOpenCv(str(r)+".jpg")
        # imgGrayManual = getGrayImgManual(str(r)+".jpg")

        data.append({
            "nama_file": str(r)+".jpg",
            "res": strFormat,
            "width": res[0].shape[1],
            "height": res[0].shape[0],
            "rwidth": res[1].shape[1],
            "rheight": res[1].shape[0],
            "gray_opencv": imgGray,
        })
    getDetectedObject()
    return data


def processing(file_name, scale_percent):
    path = str(Path(__file__).resolve().parent)+'\\static\\images\\'+file_name

    img = cv2.imread(path, cv2.IMREAD_COLOR)

    results = resizeImg(img, scale_percent)

    return results, img


def resizeImg(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    return resized


def getGrayImgOpenCv(file_name):
    path = str(Path(__file__).resolve().parent)+'\\static\\images\\'+file_name
    save_path_to = str(Path(__file__).resolve().parent) + \
        '\\static\\images\\gray-opencv\\'+file_name

    img = cv2.imread(path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # save the image
    status = cv2.imwrite(save_path_to, gray)

    return status


def getGrayImgManual(file_name):
    path = str(Path(__file__).resolve().parent)+'\\static\\images\\'+file_name
    save_path_to = str(Path(__file__).resolve().parent) + \
        '\\static\\images\\gray-manual\\'+file_name

    m = mimg.imread(path)

    # determining width and height of original image
    w, h = m.shape[:2]

    # new Image dimension with 4 attribute in each pixel
    newImage = np.zeros([w, h, 3])
    print(w)
    print(h)

    for i in range(w):
        for j in range(h):
            # ratio of RGB will be between 0 and 1
            lst = [float(m[i][j][0]), float(m[i][j][1]), float(m[i][j][2])]
            avg = float(mean(lst))
            newImage[i][j][0] = avg
            newImage[i][j][1] = avg
            newImage[i][j][2] = avg
            # newImage[i][j][3] = 1 # alpha value to be 1
    print(newImage)
    # Save image using imsave
    status = cv2.imwrite(save_path_to, newImage)

    return status


def getDetectedObject():
    path = str(Path(__file__).resolve().parent) + \
        '\\static\\images\\tantangan.jpg'
    # save_path_to = str(Path(__file__).resolve().parent)+'\\static\\images\\gray-opencv\\'+file_name

    img = cv2.imread(path, cv2.IMREAD_COLOR)
    bgBGR = np.array([255, 255, 255])
    col = img.shape[1]
    row = img.shape[0]
    data_horizon = []
    data_vertical = []

    for i in range(0, row):
        for j in range(0, col):            
            # print(img[i][j])
            if(np.array_equal(img[i][j], bgBGR) == False):            
                data_horizon.append({
                    "x": i,
                    "y": j,
                    "rgb": img[i][j]
                })
    print(data_horizon[0])

    for i in range(0, col):
        for j in range(0, row):                        
            if(np.array_equal(img[j][i], bgBGR) == False):            
                data_vertical.append({
                    "x": i,
                    "y": j,
                    "rgb": img[j][i]
                })
    print(data_vertical[0])