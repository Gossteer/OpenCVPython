'https://imagemagick.org/script/develop.php#python'
'https://www.raymond.cc/blog/how-to-compare-the-difference-between-two-identical-looking-images/'

# from wand.image import Image

# img1 = Image(filename="./images/Test/5.png")
# img2 = Image(filename="./images/Test/6.png")

# # Normalize the two images in order to avoid exposition-related issues
# img1.normalize()
# img2.normalize()

# # Create a 64 x 64 thumbnail for every image
# img1.resize(64, 64)
# img2.resize(64, 64)

# # Compare the two images using root mean square metric
# comparison = img2.compare(img1, metric='root_mean_square')
# comparison.save(filename='./images/Test/buf.png')

import matplotlib.pyplot as plt
from wand.image import Image
from wand.display import display
import pdf2image as pdf

def render(FirstFile, SecondFile):
    with Image(filename=FirstFile) as base:
        with Image(filename=SecondFile) as img:
            base.fuzz = base.quantum_range * 0.20  # Threshold of 20%
            result_image, result_metric = base.compare(img)
            # result_image.save(filename='./images/Test/buf.png')
            plt.figure('Итог сравнения')
            plt.imshow(result_image)
            plt.show()
#             Image(filename='./images/Test/1_page.jpg')
#             with display as :
#                 pass
#             display(result_image, server_name=':0')
            
#             with result_image:
#                 display(result_image)
#                 print('lol')
#                 result_image.save(filename='./images/Test/buf.png')

# with Image(filename='./images/Test/buf.png') as img:
#     img.frame(width=10, height=10)
#     img.save(filename='lena_frame.jpg')
#     display(img)

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

fileOne = "./images/Test/5.png"
fileTwo = "./images/Test/7.png"    
# bkgrnd = "./images/Test/3.jpg" 
similarity(fileOne,fileTwo)   
render(fileOne,fileTwo)