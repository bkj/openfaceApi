#!/usr/bin/env python
from glob import glob
from openface_client import OpenFaceClient

ofc = OpenFaceClient()

ofc.check_status()

for filename in glob("./test_img/*"):
  print "running on %s" % filename
  print ofc.faces_to_file(filename)