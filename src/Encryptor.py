import cv2
import sys

eot = [0, 0, 0, 0, 0, 1, 0, 0]

if len(sys.argv) > 2:
    img_name = sys.argv[1]
    enc_file_name = sys.argv[2]
else:
    print('Please enter the name if the image file which you want to store data in')
    sys.exit(1)

img = cv2.imread(img_name)
img_shape = img.shape
img_flat = img.reshape(-1)

enc_bin = ''

if enc_file_name.split('.')[1] == 'txt':
    with open(enc_file_name) as f:
        enc_file = f.read()

    for char in list(enc_file):
        enc_bin += format(ord(char), 'b').rjust(8, '0')

    enc_bin = list(map(int, list(enc_bin)))

    for i in range(0, len(enc_bin)):
        if enc_bin[i]==0 and img_flat[i]%2 == 1:
            if img_flat[i]+1 > 255:
                img_flat[i] -= 1
            else:
                img_flat[i] += 1
        elif enc_bin[i]==1 and img_flat[i]%2 == 0:
            if img_flat[i]+1 > 255:
                img_flat[i] -= 1
            else:
                img_flat[i] += 1

    for i in range(len(enc_bin), len(enc_bin)+8):
        img_flat[i] = eot[i-len(enc_bin)]

    cv2.imwrite('encrypted_text.png', img_flat.reshape(img_shape))



elif enc_file_name.split('.')[1] == 'png' or enc_file_name.split('.')[1] == 'jpg' or enc_file_name.split('.')[1] == 'jpeg':
    enc_file = cv2.imread(enc_file_name)
    enc_file_shape = enc_file.shape
    enc_file = enc_file.reshape(-1)

    for shape in enc_file_shape:
        enc_bin += format(shape, 'b').rjust(12, '0')
    for pixel in enc_file:
        enc_bin += format(pixel, 'b').rjust(8, '0')
    
    enc_bin = list(map(int, list(enc_bin)))
    
    if enc_file_shape[0]*enc_file_shape[1]*enc_file_shape[2]*8 + 36 <= img_flat.shape[0]:
        for i in range(0, len(enc_bin)):
            if enc_bin[i]==0 and img_flat[i]%2 == 1:
                if img_flat[i]+1 > 255:
                    img_flat[i] -= 1
                else:
                    img_flat[i] += 1
            elif enc_bin[i]==1 and img_flat[i]%2 == 0:
                if img_flat[i]+1 > 255:
                    img_flat[i] -= 1
                else:
                    img_flat[i] += 1

        cv2.imwrite('encrypted_image.png', img_flat.reshape(img_shape))
    else:
        print('Not enough space for storing encrypted data')
        sys.exit(1)


else:
    print('File type not understood !!')
    sys.exit(1)


