import cv2 as cv
import difflib
import numpy as np
import pdf2image as pdf
import PIL 
 
#Добавить функционал по определению оптимального сжатия изображений
#Ссылка в лоцмане на сайт

#Функция вычисления хэша
def OCRMain(FirstFile, SecondFile, Background):
    #Colors parameters
    hsv_min = np.array((217, 217, 217), np.uint8)
    hsv_max = np.array((0, 0, 0), np.uint8)
    #Read files to cv
    image = cv.imread(FirstFile)
    imagetwo = cv.imread(SecondFile)
    result = cv.imread(Background)
    #Resizing images 
    resizedFirst = cv.resize(image, (2000,1000), interpolation = cv.INTER_AREA)
    resizedTwo = cv.resize(imagetwo, (2000,1000), interpolation = cv.INTER_AREA)
    resizedBack = cv.resize(result, (2000,1000), interpolation = cv.INTER_AREA) #Уменьшим картинку
    #hsv parameters 1
    hsv = cv.cvtColor(resizedFirst, cv.COLOR_BGR2HSV ) # меняем цветовую модель с BGR на HSV 
    thresh = cv.inRange(hsv,hsv_max , hsv_min ) # применяем цветовой фильтр
    contours, hierarchy = cv.findContours(thresh.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    #hsv parameters 2
    hsvTwo = cv.cvtColor( resizedTwo, cv.COLOR_BGR2HSV ) # меняем цветовую модель с BGR на HSV 
    threshtTwo = cv.inRange( hsvTwo,hsv_max , hsv_min ) # применяем цветовой фильтр
    contoursTwo, hierarchyTwo = cv.findContours(threshtTwo.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    
    print(len(contours), len(hierarchy[0]))
    print(len(contoursTwo), len(hierarchyTwo[0]) , hierarchyTwo[0] == hierarchy[0])
    results = []
    lol = [[]]
    i = 0
    h = 0
    
    for item in contoursTwo:
        if(i < len(contours)):
            if(item not in contours[i]):
                if (len(results) != 0 and item not in results[len(results)-1]):
                    results.append(item)
                if (len(results) == 0):
                    results.append(item)
                #lol[0].append(hierarchyTwo[0][i])
        if (i >= len(contours)):
            results.append(item)
            lol[0].append(hierarchyTwo[0][i])
        i = i+1
    print(len(results))
    for items in results: 
        lol[0].append(hierarchyTwo[0][h])
        h = h+1
    #lol[0][0] = [1, -1, -1, -1]
    #resultsh = []
    #j = 0
    # for items in hierarchyTwo:
    #     if(j < len(hierarchy)):
    #         if(items in hierarchy[0][j]):
    #             resultsh.append(items)
    #     j = j+1
    print(len(results), len(lol[0]), len(np.array(lol[0])))
    print(lol[0][0], hierarchyTwo[0][0] , np.array(lol[0][0]))
    cv.drawContours( resizedBack, results, -1, (0,0,255), 1, cv.LINE_AA, np.array(lol), 1 )
    #res = [x != y for i,x in enumerate(contours) for j,y in enumerate(contoursTwo) if i != j] 
    #res1 = np.array(res)
    #print(res1)
    #print(np.isin(contours[0],contoursTwo))
    #print(contoursTwo)
    #cv.drawContours( resizedBack, contoursTwo, -1, (0,0,255), 1, cv.LINE_AA, hierarchyTwo, 1 )
    # cv.drawContours( resizedBack, contours, -1, (0,0,0), 1, cv.LINE_AA, hierarchy, 1 )
    # cv.drawContours( resizedBack, contours, -1, (0,255,0), 1, cv.LINE_AA, hierarchy, 1 )
    # cv.drawContours( resizedBack, contoursTwo, -1, (0,0,0), 1, cv.LINE_AA, hierarchyTwo, 1 )
   
    
    # if(len(contours) > len(contoursTwo)):
    #     cv.drawContours( resizedBack, contours, -1, (0,0,255), 1, cv.LINE_AA, hierarchy, 1 )
    #     cv.drawContours( resizedBack, contoursTwo, -1, (0,0,0), 1, cv.LINE_AA, hierarchyTwo, 1 )
    # else:
    #     cv.drawContours( resizedBack, contoursTwo, -1, (0,0,255), 1, cv.LINE_AA, hierarchyTwo, 1 )
    #     cv.drawContours( resizedBack, contours, -1, (0,0,0), 1, cv.LINE_AA, hierarchy, 1 )
        
    #Window
    cv.imshow('OCR results',resizedBack)
    cv.waitKey()
    cv.destroyAllWindows()
    
   
def MakeHash():
    _hash=""
    for x in range(7500):
        for y in range(3500):
            val=threshold_image[x,y]
            if val==255:
                _hash=_hash+"1"
            else:
                _hash=_hash+"0"
            
    return _hash

def MakeNewHash(hash1, hash2):
    l=len(hash1)
    resHash1 = 0
    resHash2 = 0
    i=0
    count=0
    while i<l:
        if hash1[i] == '1':
            resHash1=resHash1+1
        if hash2[i] == '1':
            resHash2=resHash2+1
        i=i+1
    return resHash1, resHash2

def CompareHash(hash1,hash2):
    l=len(hash1)
    i=0
    count=0
    while i<l:
        if hash1[i]!=hash2[i]:
            count=count+1
        i=i+1
    return count
        
def ExtractPDF(File):
    images = pdf.convert_from_path(File,poppler_path = r"./poppler-0.68.0/bin")
    images[0].save("./image_buf/buf.png","png")
    return "./image_buf/buf.png"
    
    
fileOne = "./images/Test/5.png"
fileTwo = "./images/Test/6.png"    
bkgrnd = "./images/Test/3.jpg"    
OCRMain(fileOne,fileTwo,bkgrnd)

#hash2=CalcImageHash("./images/Test/3.jpg")
#print(hash1)
#print(hash2)
#print(CompareHash(hash1, hash2))
# print(MakeNewHash(hash1,hash2))