from tkinter import *
from array import *
import numpy as np
import os
import matplotlib.pyplot as plt
from wand.image import Image
from wand.display import display
import pdf2image as pdf
from tkinter import filedialog

'https://matplotlib.org/gallery/lines_bars_and_markers/scatter_hist.html#sphx-glr-gallery-lines-bars-and-markers-scatter-hist-py'

files = []

left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
spacing = 0.001

rect_scatter = [left - 0.03, bottom, width, height]
rect_histy = [left + width + spacing, bottom, 0.2, height]

def get_path():
    root = Tk()
    root.withdraw()
    path = filedialog.askopenfiles(initialdir = "/Documents",title = "Выберете 2 pdf/image файла",filetypes = (("Файлы форматов:","*.jpg *.png *.pdf"),("pdf files","*.pdf")))
    # Нужна проверка на количество пришедших файлов
    root.destroy()
    for pathName in path:
        extension = pathName.name.split('.')[-1]
        if extension == 'pdf':
            files.append(ExtractPDF(pathName.name))
            # Найти решение для того, чтобы не сохраняя, сразу переводить фай
            # Если всё же сохранять, то не забывать, что может быть два pdf файла 
        else:
            files.append(pathName.name)
    render(files[0], files[1])
    os.remove('./image_buf/buf.png')

def render(FirstFile, SecondFile):
    fig = plt.figure(num='Результат сравнения', figsize=(12, 8))
    ax = fig.add_axes(rect_scatter)
    ax_histy = fig.add_axes(rect_histy)
    ax_histy.tick_params(axis="x", labelbottom=False)

    with Image(filename=FirstFile) as base:
        with Image(filename=SecondFile) as img:
            base.fuzz = base.quantum_range * 0.20  # Threshold of 20%
            result_image, result_metric = base.compare(img, metric='normalized_cross_correlation')
            # result_image.save(filename='./images/Test/buf.png')
    addcomare(ax, result_image)
    addlegeng(ax)
    addbar(ax_histy, result_metric)

    plt.show()

def addcomare(ax, result_image):
    ax.imshow(result_image)
    ax.set_title('/Название файлов сравнения/')

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
    images = pdf.convert_from_path(File,poppler_path = r"./poppler-0.68.0/bin")
    images[0].save("./image_buf/buf.png","png")
    return "./image_buf/buf.png"


get_path()

import matplotlib
matplotlib.figure.Figure.add_axes
matplotlib.figure.Figure.add_subplot
matplotlib.figure.Figure.add_gridspec
matplotlib.axes.Axes.scatter
matplotlib.axes.Axes.hist

