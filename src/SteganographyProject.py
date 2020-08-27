import cv2
import sys
import numpy as np

def encrypt_data(enc_file_name, img_name):
    eot = [0, 0, 0, 0, 0, 1, 0, 0]

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
        print('Your data in', enc_file_name, 'has been encoded into encrypted_text.png')



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
            print('Your data in', enc_file_name, 'has been encoded into encrypted_image.png')
        else:
            print('Not enough space for storing encrypted data')
            sys.exit(1)


    else:
        print('File type not understood !!')
        sys.exit(1)
    

def decrypt_data(img_name, decryption_scheme):
    img = cv2.imread(img_name)
    img_shape = img.shape
    img = img.reshape(-1)

    if decryption_scheme == 1:
        decrypted_msg = ''
        for i in range(0, img_shape[0]*img_shape[1]*img_shape[2], 8):
            byte = ''.join([str(bit) for bit in img[i:i+8]%2])
            if byte == '00000100':
                break
            else:
                decrypted_msg += chr(int(byte, 2))
        print('================================The Decrypted Messege is========================================\n')
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
        cv2.imwrite('image_decrypted.png', decrypted_image.reshape(decrypted_image_shape[0], decrypted_image_shape[1], decrypted_image_shape[2]))
        print('The decypted data is placed in image_decrypted.png')


if __name__ == "__main__":
    option = int(input('Enter 1 for Encrypting data or 2 for Decrypting data : '))
    if option == 1:
        enc_file_name = input('Enter the name of the file you want to encrypt : ')
        img_name = input('Enter the name of the image which will contain the data: ')
        encrypt_data(enc_file_name, img_name)
    else:
        decryption_scheme = int(input('==================Please specify the decryption scheme to be used=======================\nEnter 1 for Text retrieval and 2 for Image retrieval: '))
        img_name = input('Enter the name of the image from which data is to be extracted: ')
        decrypt_data(img_name, decryption_scheme)