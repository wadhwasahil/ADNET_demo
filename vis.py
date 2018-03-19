import numpy as np
import cv2
from scipy import misc
import os 
from m_util import sdmkdir,to_rgb3b

def show_heatmap_on_image(img,mask):
    #mask = np.float32(mask)/np.max(mask)
    mask[mask<150] = 0

    heatmap = cv2.applyColorMap(mask, 2)  #Jet is 2, winter is 3
    heatmap = np.float32(heatmap) / 255
    img = np.float32(img)/255
    cam = heatmap* 0.5+ np.float32(img)
    cam = cam / np.max(cam)
    return np.uint8(cam*255)

def show_plainmask_on_image(im,mask):
    mask = np.float32(mask)
    mask = mask/np.max(mask)
    mask[mask<0.5] =0
    im = np.float32(im)
    if im.ndim ==2:
        im = to_rgb3b(im)
    im = im * 0.5
    im[:,:,1] = im[:,:,1] + mask*100
    im[im>255] = 255
    return im.astype(np.uint8)
def visdir(imdir,maskdir,visdir):
    sdmkdir(visdir)    
    imlist=[]
    imnamelist=[]
    print imdir
    for root,_,fnames in sorted(os.walk(imdir)):
        print root,fnames
        for fname in fnames:
            if fname.endswith('.png'):
                pathA = os.path.join(root,fname)
                pathB = os.path.join(maskdir,fname)
                imlist.append((pathA,pathB,fname))
                imnamelist.append(fname)
    print(imlist)
    for pathA,pathB,fname in imlist:
        print fname
        A = misc.imread(pathA)
        B = misc.imread(pathB)
        vim = show_heatmap_on_image(A,B)
        #vim = show_plainmask_on_image(A,B)
        cv2.imwrite(os.path.join(visdir,fname),np.append(A,vim,axis=1))
def visdir2(imdir,GT,maskdir,visdir):
    sdmkdir(visdir)    
    imlist=[]
    imnamelist=[]
    for root,_,fnames in sorted(os.walk(imdir)):
        for fname in fnames:
            if fname.endswith('.png'):
                pathA = os.path.join(root,fname)
                pathGT = os.path.join(GT,fname)
                pathmask = os.path.join(maskdir,fname)
                imlist.append((pathA,pathGT,pathmask,fname))
                imnamelist.append(fname)
    print imnamelist
    for pathA,pathB,pathmask,fname in imlist:
        A = misc.imread(pathA)
        GT = misc.imread(pathB)
        mask = misc.imread(pathmask)
        GTv = show_plainmask_on_image(A,GT)
        #maskv = show_plainmask_on_image(A,mask)
        maskv = show_heatmap_on_image(A,mask)
        
        cv2.imwrite(os.path.join(visdir,fname),np.hstack((A,maskv,GTv)))#np.append(np.append(A,GTv,axis=1),maskv,axis=1))
def visAB(root,name):
    
    A = root + '/A/'
    B = root + '/res/' + name +'/'
    vis = root + '/vis/'+name+'/'
    visdir(A,B,vis)
def visABC(root,name):
    print('Visulizing:' + name)
    A = root + '/A/'
    B = root + '/B/'
    res = root + '/res/' + name +'/'
    vis = root + '/vis_all/'+name+'/'
    visdir2(A,B,res,vis)

root = '/gpfs/projects/LynchGroup/Train_all/CROZtrain/CROPPED/p1000/' 
#root ='/gpfs/projects/LynchGroup/Train_all/CROPPED/p1000/'
#root ='/nfs/bigbox/hieule/p1000/testing/PAUL/'
root ='/nfs/bigbox/hieule/p1000/testing/CROZ/'
visABC(root,'RGB0.5')
