import numpy as np
import cv2
from google.colab.patches import cv2_imshow
from math import sqrt, atan
from math import atan, degrees

img = cv2.imread('/content/lane4.jpeg',0)

def pro(img, kernel, height,width):
  pixels = []
  
  #pixels are extracted from the image converted to grayscale
  for i in range(height):
    for j in range(width):
      pixels.append(img[i,j])

  #The pixels array is resized in accordance with the size of the image
  pixels = np.array(pixels).reshape(height,width)

  #To handle the edge cases, sentinel values are used
  #The pixels array is bound by zeros on all edges

            # 00000000
            # 0PIXELS0
            # 00000000
  #This is done to ensure that the kernel is applied to all the pixels
  #Sentinel values to ensure the edges arent missed out

  #Along the rows and columns
  pixels = np.insert(pixels , [0,height] , np.zeros(len(pixels[0])) , axis = 0)
  pixels = np.insert(pixels , [0, width] , np.zeros((len(pixels[:, 0]) ,1)) , axis = 1)
    #Convolution is applied here
  blur = []
  for i in range(1,height):
    for j in range(1,width):
      temp = pixels[i:i+3 , j:j+3]
      product = np.multiply(temp,kernel)
      blur.append(sum(sum(product)))

  blur = np.array(blur).reshape(height-1,width-1)
  return(blur)
cv2_imshow(pro(img, kernelblur, height, width))

def change(sobel1, convoluted_X, convoluted_Y, height, width):
  value = 0
  non_li = []
  from math import atan, degrees
  for i in range(1 , height-3):
    for j in range(1, width-3):
      grx = convoluted_X[i, j]
      gry = convoluted_Y[i, j]
      sob = sobel1[i, j]
      if gry == 0:
        if sob >= sobel1[i, j+1] and sob >= sobel1[i, j-1]:
          value = sob
        else:
          value = 0
      elif grx == 0:
        if sob >= sobel1[i+1, j] and sob >= sobel1[i-1, j]:
          value = sob
        else:
          value = 0
      else:
        angle = degrees(atan(gry/grx))
        if grx > 0 and gry > 0:
          gr = angle
        elif grx < 0 and gry < 0:
          gr = 180 + angle
        elif grx > 0 and gry < 0:
          gr = 360 + angle
        else:
          gr = 180 + angle
        p1 = [*range(0,22)]
        p2 = [*range(22,67)]
        p3 = [*range(67,112)]
        p4 = [*range(112,157)]
        p5 = [*range(157,202)]
        p6 = [*range(202,247)] 
        p7 = [*range(247,290)]
        p8 = [*range(290,337)]          
        p9 = [*range(337,360)]
        gr = int(gr)
        if gr in p1 or gr in p5 or gr in p9:
          if sob >= sobel1[i, j+1] and sob >= sobel1[i, j-1]:
            value = sob
          else:
              value = 0
        elif gr in p2 or gr in p6:
          if sob >= sobel1[i-1, j+1] and sob >= sobel1[i+1, j-1]:
            value = sob
          else:
              value = 0
        elif gr in p3 or gr in p7:
          if sob >= sobel1[i-1, j] and sob >= sobel1[i+1, j]:
            value = sob
          else:
              value = 0
        elif gr in p4 or gr in p8:
          if sob >= sobel1[i-1, j-1] and sob >= sobel1[i+1, j + 1]:
            value = sob
          else:
              value = 0
      non_li.append(value % 255)

  non_li = np.array(non_li).reshape(height-4, width-4)
  #cv2_imshow(non_li)
  threshold(non_li)
  #print(non_li.shape)

def threshold(non_li):
  ha, wi = non_li.shape
  #print(ha, wi)
  high = np.amax(non_li)*0.9
  low = np.amax(non_li)*0.2
  final = []
  for i in range(ha):
    for j in range(wi):
      if non_li[i,j] > high:
        final.append(255)
      elif low <= non_li[i,j] <= high:
        final.append(non_li[i,j])
        #final.append(190)
      else:
        final.append(0)

  final = np.array(final).reshape(ha, wi)

  cv2_imshow(final)


def process(img):
  height = img.shape[0]
  width= img.shape[1]
  blur = pro(img, kernelblur, height, width)
  height = height - 1
  width = width - 1
  convoluted_Y = pro(blur, kernelsobelX, height, width)
  convoluted_X = pro(blur, kernelsobelY, height, width)
  sobel1 = []
  arc = []
  for i in range(height-1):
    for j in range(width-1):
      in_x = pow(convoluted_X[i,j] ,2)
      in_y = pow(convoluted_Y[i,j] , 2)
      gr_X = convoluted_X[i,j]
      gr_Y = convoluted_Y[i,j]
      grad = sqrt(in_x + in_y)
      sobel1.append(grad) 
  sobel1 = np.array(sobel1).reshape(height-1, width-1)
  cv2_imshow(sobel1)
  height_con = convoluted_X.shape[0]
  width_con = convoluted_X.shape[1]
  convoluted_X = np.insert(convoluted_X , [0,height_con-1] , np.zeros(len(convoluted_X[0])) , axis = 0)
  convoluted_X = np.insert(convoluted_X , [0, width_con-1] , np.zeros((len(convoluted_X[:, 0]) ,1)) , axis = 1)
  convoluted_Y = np.insert(convoluted_Y , [0,height_con-1] , np.zeros(len(convoluted_Y[0])) , axis = 0)
  convoluted_Y = np.insert(convoluted_Y , [0, width_con-1] , np.zeros((len(convoluted_Y[:, 0]) ,1)) , axis = 1)
  sobel1 = np.insert(sobel1 , [0,sobel1.shape[0]-1] , np.zeros(len(sobel1[0])) , axis = 0)
  sobel1 = np.insert(sobel1 , [0, sobel1.shape[1]-1] , np.zeros((len(sobel1[:, 0]) ,1)) , axis = 1)
  non_li = change(sobel1, convoluted_X, convoluted_Y, sobel1.shape[0], sobel1.shape[1])
process(img)

