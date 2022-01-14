from PIL import Image
import numpy as np
import os
import cv2
import time

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images


start = time.time()

path = "/home/nikhilanand_1921cs24/Souryadip/PyHIST/output"

count = 0

for i in range(2,len([x[0] for x in os.walk(path)]),2):

    count = count + 1

    patch_path = [x[0] for x in os.walk(path)][i]

    patches_list = load_images_from_folder(patch_path)

    print("Number of patches in slide no:",count,"is :",np.array(patches_list).shape[0])

    patches_mean_list = []

    n = np.array(patches_list).shape[0]

    mse_list = []

    for j in patches_list:

        patches_mean = np.mean(j,axis = (0,1))
        patches_mean_list.append(patches_mean)
        #mse = np.square(patches_mean - arr_mean).mean()
        #mse_list.append(mse)

    overall_mean = [np.mean(k) for k in zip(*patches_mean_list)]

    print("Mean RGB of the full Whole Slide Image for slide ",count,":",overall_mean)

    for k in patches_list:

        patches_mean = np.mean(k,axis = (0,1))
        mse = np.square(patches_mean - overall_mean).mean()
        mse_list.append(mse)

    top_40_idx = sorted(range(len(mse_list)), key=lambda i: mse_list[i])[0:40]

    final_images = []

    base = os.path.basename(patch_path)

    Output_path = '/home/nikhilanand_1921cs24/Souryadip/Processed'+'/'+base 

    is_exist = os.path.exists(Output_path)

    print("Saving the images!")

    if not is_exist:

        os.makedirs(Output_path)

    for i in range(0,n):

        if i in top_40_idx:

            img = Image.fromarray(patches_list[i])
            img.save(Output_path+"/"+str(i)+'.png')

print("Process Completed!")

end = time.time()

print("Elapsed time:", end - start)