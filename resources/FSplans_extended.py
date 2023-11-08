##############################################################################
##
# This file is part of Fermi surfaces - Stack 3D project
##
# Copyright 2023 / AYMEN MAHMOUDI, FRANCE
##
# The files of this project are free and open source: you can redistribute them and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# This project is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
##
##############################################################################

__author__ = ["Aymen Mahmoudi"]
__license__ = "GPL"
__date__ = "02/09/2023"


import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from matplotlib.colors import Normalize
from mpl_toolkits import mplot3d
from math import dist

def rot_scale(img_list,file_list,N,angle,scale): 
    for i in range(N):
        (h, w) = img_list[i].shape[:2]
        center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, angle, scale)
        img_list[i] = cv2.warpAffine(img_list[i], M, (w, h))
        
    fig, axs = plt.subplots(1,N)
    fig.suptitle('Preview : Rotation = '+str(angle)+'°')

    for i in range(N):
        axs[i].imshow(img_list[i])
        axs[i].set_title(file_list[i])

    plt.tight_layout()
    return img_list


def crop(x_ini,x_fin,y_ini,y_fin,N,img_list,image_num,confirm):

    Repere_position =  [(x_ini,y_ini),(x_fin,y_ini),(x_ini,y_fin),(x_fin,y_fin)]
    crop_img = img_list[image_num-1][y_ini:y_fin, x_ini:x_fin]
    print('The image '+str(image_num)+' dimnsions are',np.shape(img_list[image_num-1]))

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(img_list[image_num-1])
    ax2.imshow(crop_img)

    for i in range(4): 
        ax1.plot(Repere_position[i][0],Repere_position[i][1], marker="o", markersize=10, markeredgecolor="blue", markerfacecolor="red")
    ax1.hlines(y =y_ini, xmin = x_ini, xmax = x_fin, color = 'r', linestyle = '--',lw = 2)
    ax1.hlines(y =y_fin, xmin = x_ini, xmax = x_fin, color = 'r', linestyle = '--',lw = 2)
    ax1.vlines(x =x_ini, ymin = y_ini, ymax = y_fin, color = 'r', linestyle = '--',lw = 2)
    ax1.vlines(x =x_fin, ymin = y_ini, ymax = y_fin, color = 'r', linestyle = '--',lw = 2)
    ax1.set_title('Ref image =  '+str(image_num))
    ax2.set_title('Cropping preview : Image '+str(image_num) )   
    
    if confirm == True :
        crop_img_list = []
        for i in range (N):
            crop_img_list.append(img_list[i][y_ini:y_fin, x_ini:x_fin]) 
        return crop_img_list