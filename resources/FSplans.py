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

'''
The loading function anable to load the figures to be stacked

'''


def load(folder_abs_path, file_list):
    img_list = []
    eng_list = []
    N = len(file_list)
    for i in range(N):
        img_list.append(cv2.cvtColor(cv2.imread(folder_abs_path+'\\'+file_list[i]), cv2.COLOR_BGR2RGB))
        eng_list.append(file_list[i][:-6])

    print('Suprposition of ' + str(N)+' pics at the energies (eV) : '+str(eng_list))
    return N,img_list, eng_list



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



def adding_axis(kx_min,kx_max,ky_min,ky_max,N,img_list):  
    # Create of a list of N couple
    xy_list = []
    for i in range(N):
        xy_list.append((np.ogrid[0:img_list[i].shape[0], 0:img_list[i].shape[1]]))

    # Create of a list of N couple
    xy_norm_list = []
    for i in range(N):
        xy_norm_list.append((np.reshape(np.linspace(kx_min, kx_max, np.shape(xy_list[i][0])[0]), (len(np.linspace(kx_min, kx_max, np.shape(xy_list[i][0])[0])), 1)), np.reshape(np.linspace(ky_min, ky_max,np.shape(xy_list[i][1])[1]), (1, len(np.linspace(ky_min, ky_max,np.shape(xy_list[i][1])[1]))))))

    for i in range(N):
        #axed_img_list.append(img_list[i].astype('float32')/255) 
        img_list[i]=img_list[i].astype('float32')/255
        
    return xy_norm_list,img_list




def plot_3D(path,img_list,eng_list,N,xy_norm_list,fig_size,box_aspect_ratio,font,preview_quality,save_preview,dpi,k_label_fontsize,
                 E_label_fontsize,grid_thickness,axis_thickness,kx_min,kx_max,ky_min,ky_max,elevation,rotation,
                 x_y_tick_spacing,k_tick_size,label_padding,z_text_pos,z_text_size,decalage,on_scale,kx_lim,ky_lim):
    
    # box settings
    fig,ax = plt.subplots(figsize=fig_size,subplot_kw={'projection':'3d'})
    fig.subplots_adjust(left=0.2, right=0.3, top=.11, bottom=.1)
    ax.set_box_aspect(aspect = box_aspect_ratio)
    plt.rcParams.update({'font.family':font})
    
     
    
    if preview_quality == 'low':
        res =100
    elif preview_quality == 'medium':
        res = 50
    elif preview_quality == 'high':
        res=10
    elif preview_quality == 'best':
        res=1
    else :
        raise Exception("Please choose a quality to be low, medium, high or best")
        
    # Z position :
    
    step = .2
    z_ax_position = [0]
    for i in range (N-1):
        if on_scale == True:
            z_ax_position.append(float(eng_list[i]))
        else:
            z_ax_position.append(z_ax_position[i]+step)
    

    for i in range(N):
        ax.plot_surface(xy_norm_list[i][0],xy_norm_list[i][1],np.atleast_2d(z_ax_position[i]), rstride=res, cstride=res ,facecolors=img_list[i],shade=False)

        
    # Axis settings
    ax.set_xlabel('$k_{y}$ ($\AA^{-1}$)', fontsize=k_label_fontsize, rotation=-15)
    ax.set_ylabel('$k_{x}$ ($\AA^{-1}$)', fontsize=k_label_fontsize, rotation=65)
    ax.zaxis.set_rotate_label(True)  # disable automatic rotation
    ax.set_zlabel('E$_{k}$ - E$_{F}$ (eV)', fontsize=E_label_fontsize, fontweight = 'bold',rotation=-30)
    
    ax.xaxis._axinfo["grid"].update({"linewidth":grid_thickness})
    ax.yaxis._axinfo["grid"].update({"linewidth":grid_thickness})
    ax.zaxis._axinfo["grid"].update({"linewidth":.2})

    #ax.set(facecolor = "white")
    
    # make the panes transparent
    ax.xaxis.set_pane_color((.2, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((.2, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((0, 1.0, 1.0, 0.0))
    # make the grid lines transparent
    ax.xaxis._axinfo["grid"]['blue'] =  (1,1,1,0)
    ax.yaxis._axinfo["grid"]['blue'] =  (1,1,1,0)
    ax.zaxis._axinfo["grid"]['blue'] =  (1,1,1,0)

    ax.tick_params(width=40)
    for axis in [ax.w_xaxis, ax.w_yaxis, ax.w_zaxis]:
        axis.line.set_linewidth(axis_thickness)
    
    
    tick_spacing_X = x_y_tick_spacing[0]
    tick_spacing_Y = x_y_tick_spacing[1]
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_y_tick_spacing[0]))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(x_y_tick_spacing[1]))

    plt.xticks(fontsize=k_tick_size, rotation=0)
    plt.yticks(fontsize=k_tick_size, rotation=0)
    #plt.zticks(fontsize=16, fontweight = 'bold',rotation=0)
    
    #ax.set_aspect('auto')
    ax.azim = rotation
    ax.elev = elevation

    #ax.tick_params(axis='z', which='major', pad=20)
    ax.xaxis.labelpad = label_padding[0]
    ax.yaxis.labelpad = label_padding[1]
    ax.zaxis.labelpad = label_padding[2]

    
    # Adding Zticks (Text)
    ax.set_ylim(ky_lim[0],ky_lim[1])
    ax.set_xlim(kx_lim[0],kx_lim[1])
    ax.set_zlim(z_ax_position[-1],z_ax_position[0])
    text_x_pos = z_text_pos[0]
    text_y_pos = z_text_pos[1]
    text_size = z_text_size
    ax.zaxis.set_tick_params(labelsize=36)
    hfont = {'fontname':font}
    text_color = 'black'
    
    
    if on_scale == True:
        ax.set_zticks(z_ax_position)
    else :
        z_annotation = []

        
        for i in range (N):
            z_annotation.append((z_ax_position[i]+decalage,eng_list[i]))
        ax.set_zticks([])
        for i in range(len(z_annotation)):
            ax.text(text_x_pos,text_y_pos, z_annotation[i][0],z_annotation[i][1],  size=text_size, color=text_color,**hfont)
    
      
    # saving

    ax.grid(True) 
    fig.tight_layout()
    if save_preview == True:
        plt.savefig(path+'\\'+'3D_superposition_preview_'+preview_quality+'_Res_'+str(dpi)+'.png', dpi= dpi, bbox_inches = 'tight')  
          



