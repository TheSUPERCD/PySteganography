import cv2
import numpy as np
from pynput.keyboard import Key, Listener
import sys

if len(sys.argv) > 1:
    img_name = sys.argv[1]
else:
    print('Please enter the name if the image file which you want to restore data from')
    sys.exit(1)

img = cv2.imread(img_name)
img_shape = img.shape
img = img.reshape(-1)

decryption_scheme = int(input('Please specify the decryption scheme to be used :\n1. Text retrieval\n2. Image retrieval\n'))

if decryption_scheme == 1:
    decrypted_msg = ''
    for i in range(0, img_shape[0]*img_shape[1]*img_shape[2], 8):
        byte = ''.join([str(bit) for bit in img[i:i+8]%2])
        if byte == '00000100':
            break
        else:
            decrypted_msg += chr(int(byte, 2))
    print(decrypted_msg)

elif decryption_scheme == 2:
    decrypted_image_shape = np.zeros((3,), dtype=np.int)
    for i in range(0, 36, 12):
        shape = int(''.join([str(bit) for bit in img[i:i+12]%2]), 2)
        decrypted_image_shape[i%11] = shape

    decrypted_image = np.zeros((decrypted_image_shape[0]*decrypted_image_shape[1]*decrypted_image_shape[2], ))

    if (decrypted_image_shape[0]*decrypted_image_shape[1]*decrypted_image_shape[2]*8 + 36) <= (img_shape[0]*img_shape[1]*img_shape[2]):
        for i in range(36, decrypted_image_shape[0]*decrypted_image_shape[1]*decrypted_image_shape[2]*8 + 36, 8):
            decrypted_image[int((i-36)/8)] = int(''.join([str(bit) for bit in img[i:i+8]%2]), 2)
    else:
        print('Image decryption not possible')
        sys.exit(1)
    cv2.imwrite('decrypted.png', decrypted_image.reshape(decrypted_image_shape[0], decrypted_image_shape[1], decrypted_image_shape[2]))
            
