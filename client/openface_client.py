#!/bin/env python

import requests
import os
import re
import json
import cv2

class OpenFaceClient:
    def __init__(self, url = "http://192.168.99.100:5000"):
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
    
    def faces_to_file(self, imgPath, margin=10):
        boxes, bgrImg = self.get_face_bb(imgPath)
        for i, box in enumerate(boxes['rects']):
            print 'extracting face %i at %s' % (i, str(box))
            outpath = '%s-face-%d.png' % (re.sub('\.*?$', '', imgPath), i)
            
            (top, bottom, left, right) = box
            im_sub = bgrImg[max(0, top - margin):(bottom + margin), max(0, left - margin):(right + margin), :]
            cv2.imwrite(outpath, im_sub)
        
        return True