import numpy as np

__background_gray = None


def findMinMax(mat):
    index = mat.argmax()
    dim = mat.shape
    y = index / dim[1]
    x = index % dim[1]
    intens = mat[y][x]
    return [x,y,intens]

# demosaic, into gray.
# blue is commented out because we almost always use red and green lasers
def getGrayscaleFromBayer(m):
    r = m[0::2, 0::2]
    g = m[0::2, 1::2] #(( m[0::2, 1::2]/2 + m[1::2, 0::2]/2)).clip(0,254) #removed this for speed
    #b = m[1::2, 1::2]
    gray = 0.5*r + 0.5*g #0.4*g + 0.1*b
    return gray


def brightestPoint( mat):
    global __background_gray
    gray = getGrayscaleFromBayer( mat)
    if __background_gray == None:
        __background_gray = gray
    fg = np.minimum( np.maximum( gray - __background_gray,0),255).astype('uint8')
    mm = findMinMax( fg)
    imgshape = mat.shape
    xy = [float(mm[0]+0.5)/imgshape[1], float(mm[1]+0.5)/imgshape[0] ]
    __background_gray = 0.99*__background_gray + 0.01 * gray
    result = {"x":str(mm[0]), "y":str(mm[1]), "x1":str(xy[0]), "y1":str(xy[1]), "i":str(mm[2])}
    #print( "result brightest point: ", result)
    return result