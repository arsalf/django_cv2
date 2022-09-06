from asyncio.windows_events import NULL
from django.shortcuts import render
from django.http import HttpResponse
import cv2
import numpy as np
from pathlib import Path
from django_cv2.settings import BASE_DIR

# Create your views here.
def index(request):
    return render(request, "index.html")

def pertemuan(request, id):

    rData = range(0, 3)    
    res = getInfoImg(rData)
    
    data = {        
        "results" : res
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
                strFormat += "<tr><th>"+str(i)+"</th><td>"+str(colors[2])+"</td><td>"+str(colors[1])+"</td><td>"+str(colors[0])+"</td></tr>"
                i += 1
        data.append( {
            "nama_file" : str(r)+".jpg",
            "res": strFormat,
            "width" : res[0].shape[1],
            "height" : res[0].shape[0],
            "rwidth" : res[1].shape[1],
            "rheight" : res[1].shape[0]
        })
    return data

def processing(file_name, scale_percent):
    path = str(Path(__file__).resolve().parent)+'\\static\\images\\'+file_name
    
    img = cv2.imread(path, cv2.IMREAD_COLOR)

    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    results = resized
    
    return results, img

def getGrayImgOpenCv(file_name):
    path = str(Path(__file__).resolve().parent)+'\\static\\images\\'+file_name
    save_path_to = str(Path(__file__).resolve().parent)+'\\static\\images\\gray\\'+file_name
    
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #save the image    
    status = cv2.imwrite(save_path_to, gray)

    if(status):
        return save_path_to

    return NULL    