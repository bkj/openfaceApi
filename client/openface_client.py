#!/bin/env python

import os
import re
import sys
import cv2
import json
import requests
from glob import glob

class OpenFaceClient:
    def __init__(self, url="http://192.168.99.100:5000"):
        self.url = url
        
    def read_image(self, imgPath):
        bgrImg = cv2.imread(imgPath)
        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
        fltImg = rgbImg.flatten().tolist()
        return fltImg, bgrImg, rgbImg.shape
        
    def check_status(self):
        cmd = self.url + "/api/health"
        r = requests.get(cmd)
        r.raise_for_status()
        return r.json()
        
    def get_face_bb(self, imgPath):
        cmd = self.url + "/api/bbox"
        fltImg, bgrImg, dim = self.read_image(imgPath)
        payload = {'image': fltImg, 'dim': dim}
        r = requests.post(cmd, json=payload, headers= {})
        r.raise_for_status()
        return r.json(), bgrImg
        
    def img2faces(self, imgPath, margin=10):
        faces = []
        boxes, bgrImg = self.get_face_bb(imgPath)
        for i, box in enumerate(boxes['rects']):
            (top, bottom, left, right) = box
            im_sub = bgrImg[max(0, top - margin):(bottom + margin), max(0, left - margin):(right + margin), :]
            faces.append(im_sub)
        
        return faces
    
    def save_faces(self, dirPath, imgPath, faces, dirName='detected-faces'):
        outPath = os.path.join(dirPath, dirName, os.path.basename(imgPath))
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        
        paths = []
        for i,face in enumerate(faces):
            p = os.path.join(outPath, '%d.png' % i)
            cv2.imwrite(p, face)
            paths.append(p)
        
        return paths
        
    def dir2faces(self, dirPath, margin=10):
        imgPaths = glob(os.path.join(dirPath, "*"))
        for ip in imgPaths:
            if 'detected-faces' in ip:
                print >> sys.stderr, 'found detected-faces'
                return
            
        for imgPath in imgPaths:
            print 'processing %s' % imgPath
            faces = self.img2faces(imgPath, margin=margin)
            _ = self.save_faces(dirPath, imgPath, faces)
            