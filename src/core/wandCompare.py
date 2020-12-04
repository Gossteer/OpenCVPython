'https://imagemagick.org/script/develop.php#python'
'https://www.raymond.cc/blog/how-to-compare-the-difference-between-two-identical-looking-images/'

import matplotlib.pyplot as plt
from wand.image import Image
from wand.display import display
import pdf2image as pdf
import numpy as np

def render(FirstFile, SecondFile):
    with Image(filename=FirstFile) as base:
        with Image(filename=SecondFile) as img:
            base.fuzz = base.quantum_range * 0.20  # Threshold of 20%
            result_image, result_metric = base.compare(img, metric='normalized_cross_correlation')
            # result_image.save(filename='./images/Test/buf.png')
            showcompare(result_image, FirstFile, SecondFile, result_metric)

def showcompare(result_image, FirstFile, SecondFile, result_metric):
    fig, ax = plt.subplots()
    ax.plot('o-', color='gray', label='Одинаково')
    ax.plot('o-', color='red' , label='Разница')
    ax.legend()
    ax.set_title('Название файлов сравнения')
    ax.set_title('% разницы')
    ax.imshow(result_image)
    data_1 = int(round(result_metric, 2) * 100)
    data_2 = 100 - int(round(result_metric, 2) * 100)
    ax.bar(1, data_1, color='gray')
    ax.bar(1, data_2, color='red', bottom = data_1)
    fig.set_figwidth(12)    #  ширина Figure
    fig.set_figheight(6)  
    plt.show()

# def persentcompare(persent):
#     """
#     docstring
#     """
#     return x + y

def similarity(FirstFile, SecondFile):
    dissimilarity_threshold = 0.0
    similarity_threshold = 0
    with Image(filename=FirstFile) as img:
        with Image(filename=SecondFile) as reference:
            location, diff = img.similarity(reference,
                                            similarity_threshold)
            print(location)
            print(diff)
            # if diff > dissimilarity_threshold:
            #     print('Images too dissimilar to match')
            # elif diff <= similarity_threshold:
            #     print('First match @ {left}x{top}'.format(**location))
            # else:
            #     print('Best match @ {left}x{top}'.format(**location))

def ExtractPDF(File):
    images = pdf.convert_from_path(File,poppler_path = r"./poppler-0.68.0/bin")
    images[0].save("./image_buf/buf.png","png")
    return "./image_buf/buf.png"

  
# fileOne = "./images/Test/donut1.jpg"
# fileTwo = "./images/Test/donut.jpg"
 
# render(fileOne,fileTwo)

fileOne = "./images/Test/5.png"
fileTwo = "./images/Test/8.png"

render(fileOne,fileTwo)


# fileOne = "./images/Test/donut.jpg"
# fileTwo = "./images/Test/donut.jpg"

# render(fileOne,fileTwo)

# fileOne = "./images/Test/1.png"
# fileTwo = "./images/Test/2.png"

# render(fileOne,fileTwo)