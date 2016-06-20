#!/usr/bin/env python
from openface_client import OpenFaceClient

client = OpenFaceClient()
client.check_status()
client.dir2faces('./test_img')