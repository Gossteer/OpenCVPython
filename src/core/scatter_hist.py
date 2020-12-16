from tkinter import *
from array import *
import numpy as np
import os
import cv2 as cv
import difflib
import PIL
import matplotlib.pyplot as plt
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display
import pdf2image as pdf
from tkinter import filedialog

'https://matplotlib.org/gallery/lines_bars_and_markers/scatter_hist.html#sphx-glr-gallery-lines-bars-and-markers-scatter-hist-py'

files = []

left, width = 0.02, 0.75
bottom, height = 0.13, 0.75
spacing = 0.05

rect_scatter = [left, bottom, width, height]
rect_histy = [left + width - spacing, bottom, 0.2, height]

result_image_gloval = 0
result_metric_global = 1

def OCRRender(FirstFile, SecondFile):
    #Colors parameters
    global result_image_gloval
    hsv_min = np.array((217, 217, 217), np.uint8)
    hsv_max = np.array((0, 0, 0), np.uint8)
    #Read files to cv
    image = cv.imread(FirstFile)
    imagetwo = cv.imread(SecondFile)
    result = cv.imread("./images/Test/3.jpg")
    #Resizing images 
    resizedFirst = cv.resize(image, (3307,2339), interpolation = cv.INTER_AREA)
    resizedTwo = cv.resize(imagetwo, (3307,2339), interpolation = cv.INTER_AREA)
    result_image_gloval = cv.resize(result, (3307,2339), interpolation = cv.INTER_AREA) #Уменьшим картинку
    #hsv parameters 1
    hsv = cv.cvtColor(resizedFirst, cv.COLOR_BGR2HSV ) # меняем цветовую модель с BGR на HSV 
    thresh = cv.inRange(hsv,hsv_max , hsv_min ) # применяем цветовой фильтр
    contours, hierarchy = cv.findContours(thresh.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    #hsv parameters 2
    hsvTwo = cv.cvtColor( resizedTwo, cv.COLOR_BGR2HSV ) # меняем цветовую модель с BGR на HSV 
    threshtTwo = cv.inRange( hsvTwo,hsv_max , hsv_min ) # применяем цветовой фильтр
    contoursTwo, hierarchyTwo = cv.findContours(threshtTwo.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours( result_image_gloval, contoursTwo, -1, (0,0,255), 1, cv.LINE_AA, hierarchyTwo, 1 )
    cv.drawContours( result_image_gloval, contours, -1, (0,0,0), 1, cv.LINE_AA, hierarchy, 1 )
    cv.drawContours( result_image_gloval, contours, -1, (0,255,0), 1, cv.LINE_AA, hierarchy, 1 )
    cv.drawContours( result_image_gloval, contoursTwo, -1, (0,0,0), 1, cv.LINE_AA, hierarchyTwo, 1 )
   
    
    if(len(contours) > len(contoursTwo)):
        cv.drawContours( result_image_gloval, contours, -1, (0,0,255), 1, cv.LINE_AA, hierarchy, 1 )
        cv.drawContours( result_image_gloval, contoursTwo, -1, (0,0,0), 1, cv.LINE_AA, hierarchyTwo, 1 )
    else:
        cv.drawContours( result_image_gloval, contoursTwo, -1, (0,0,255), 1, cv.LINE_AA, hierarchyTwo, 1 )
        cv.drawContours( result_image_gloval, contours, -1, (0,0,0), 1, cv.LINE_AA, hierarchy, 1 )
        
    # #Window
    # cv.imshow('OCR results',resizedBack)
    # cv.waitKey()
    # cv.destroyAllWindows()

def get_path():
    # root = Tk()
    # root.withdraw()
    # path = filedialog.askopenfiles(initialdir = "/Documents",title = "Выберете 2 pdf/image файла",filetypes = (("Файлы форматов:","*.jpg *.png *.pdf"),("pdf files","*.pdf")))
    # # Нужна проверка на количество пришедших файлов
    # root.destroy()
    # for pathName in path:
    #     extension = pathName.name.split('.')[-1]
    #     if extension == 'pdf':
    #         files.append(ExtractPDF(pathName.name))
    #         # Найти решение для того, чтобы не сохраняя, сразу переводить фай
    #         # Если всё же сохранять, то не забывать, что может быть два pdf файла 
    #     else:
    #         files.append(pathName.name)
   
    # show(files[0], files[1])
    show("./image_buf/551.pdf.png", "./image_buf/493.pdf.png")
    # os.remove('./image_buf/buf.png')

def show(FirstFile, SecondFile):
    fig = plt.figure(num='Результат сравнения', figsize=(16, 9))
    ax = fig.add_axes(rect_scatter)
    ax_histy = fig.add_axes(rect_histy)
    ax_histy.tick_params(axis="x", labelbottom=False)

    OCRRender(FirstFile, SecondFile)
    # wondRender(FirstFile, SecondFile)
    addcomare(ax, result_image_gloval)
    # addlegeng(ax)
    # addbar(ax_histy, result_metric_global)
    plt.show()

def wondRender(FirstFile, SecondFile):
    global result_image_gloval
    global result_metric_global
    with Image(filename=FirstFile) as base:
        with Image(filename=SecondFile) as img:
            # base.fuzz = base.quantum_range * 0.2  # Threshold of 20%
            # result_image, result_metric = base.compare(img, metric='normalized_cross_correlation', highlight = Color('green'))
            result_image, result_metric = base.compare(img, metric='normalized_cross_correlation')
            result_image.save(filename='./images/Test/' + FirstFile.split('/')[-1]+SecondFile.split('/')[-1])
    result_image_gloval = result_image
    result_metric_global = result_metric    
    # with Image(filename=FirstFile) as imgg:
    #     imgg.fuzz = imgg.quantum_range * 0.1
    #     imgg.background_color = 'black'
    #     mbr = imgg.minimum_bounding_box()
    #     with Drawing() as ctx:
    #         ctx.fill_color = 'transparent'
    #         ctx.stroke_color = 'red'
    #         ctx.polygon(points=mbr['points'])
    #         ctx.fill_color = 'red'
    #         ctx.stroke_color = 'transparent'
    #         ctx.text(1, 10, '{0:.4g}°'.format(mbr['angle']))
    #         ctx(imgg)
    #     imgg.save(filename='./images/Test/kdf_black_mbr.png')
    # dissimilarity_threshold = 0.318
    # similarity_threshold = 1.0
    # with Image(filename=FirstFile) as imgg:
    #     with Image(filename=SecondFile) as reference:
    #         location, diff = imgg.similarity(reference,
    #                                         similarity_threshold, metric='normalized_cross_correlation')
    #         if diff > dissimilarity_threshold:
    #             print('Images too dissimilar to match')
    #         elif diff <= similarity_threshold:
    #             print('First match @ {left}x{top}'.format(**location))
    #         else:
    #             print('Best match @ {left}x{top}'.format(**location))
    # with Image(filename=FirstFile) as imgg:
    #     with Image(filename=SecondFile) as phase:
    #         imgg.inverse_fourier_transform(phase)
    #     imgg.save(filename='./images/Test/kdff_black_mbr.png')
    # with Image(filename=FirstFile) as imgg:
    #     objects = imgg.connected_components()
    # for cc_obj in objects:
    #     print("{0._id}: {0.size} {0.offset}".format(cc_obj))
    with Image(filename=FirstFile) as imgA:
        with Image(filename=SecondFile) as imgB:
            imgA.sequence.append(imgB)
        with imgA.complex('conjugate') as results:
            results.save(filename='./images/Test/kdfff_black_mbr.png')

def addcomare(ax, result_image):
    ax.imshow(result_image)
    # ax.set_title('/Название файлов сравнения/')

def addlegeng(ax):
    ax.plot(1, color='gray' , label='Одинаково')
    ax.plot(1,color='red', label='Разница')
    ax.legend(bbox_to_anchor=(0, 1.09), loc='upper left', borderaxespad=0.)

def addbar(ax_histy, result_metric):
    data_1 = int(round(result_metric, 2) * 100)
    data_2 = 100 - int(round(result_metric, 2) * 100)
    ax_histy.set_title('% разницы')
    ax_histy.bar(1,data_1, color='gray', bottom = data_2)
    ax_histy.bar(1,data_2, color='red')

def ExtractPDF(File):
    # print(File.split('/')[-1])
    images = pdf.convert_from_path(File,poppler_path = r"./poppler-0.68.0/bin")
    pathNewFilePng = "./image_buf/"+ File.split('/')[-1] +".png"
    images[0].save(pathNewFilePng,"png")
    return pathNewFilePng


get_path()

import matplotlib
matplotlib.figure.Figure.add_axes
matplotlib.figure.Figure.add_subplot
matplotlib.figure.Figure.add_gridspec
matplotlib.axes.Axes.scatter
matplotlib.axes.Axes.hist

