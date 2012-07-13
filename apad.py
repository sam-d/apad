import sys
import os
import subprocess

import pyexiv2
from jinja2 import Environment, FileSystemLoader

source = sys.argv[1]
destination = sys.argv[2]

files = os.listdir(source)
for i in range(len(files)):
    files[i] = os.path.join(source,files[i])
    
dates = list()
meta = []
for name in files:
    metadata = pyexiv2.ImageMetadata(name)
    metadata.read()
    dates.append(metadata['Exif.Image.DateTime'].value.date())
    meta.append([metadata['Exif.Image.DateTime'].value,metadata['Exif.Photo.FocalLengthIn35mmFilm'].value,metadata['Exif.Photo.ExposureTime'].value,metadata['Exif.Photo.FNumber'].value, metadata['Exif.Photo.ISOSpeedRatings'].value])

data = dict(zip(files,dates))
metadata = dict(zip([os.path.join(destination,os.path.basename(file)) for file in files],meta))
"""
for root, dirs, files in os.walk(source):
    dates = [pyexiv2.ImageMetadata(name).read()['Exif.Image.DateTime'] for name in files]
    data = dict(zip(files,dates))
"""

#reverse the dict
data_rev = dict()
for (k,v) in data.items():
    if v in data_rev:
        data_rev[v].append(k)
    else:
        data_rev[v] = [k]

#choose one pictures per day
final_choices = []
for (k,v) in data_rev.items():
    if len(v) > 1:
        final_choices.append(subprocess.check_output(["feh", "-F", "-G", "-A echo -n %f"] + v))
    else:
        final_choices.append(v)

#output all pictures to dir, cropped with the metadata removed
for pic in final_choices:
    subprocess.call(["convert",pic,"-resize", "1028x4000",os.path.join(destination,os.path.basename(pic))]) #only reduce larger images to be a width of 1028px

#create html, linking to pictures
env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('index.jinja2')
with open('index.html','w') as f:
    f.write(template.render(files=[os.path.join(destination,os.path.basename(pic)) for pic in final_choices],meta=metadata))

