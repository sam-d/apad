#A pic a day (apad)

This is a script that takes all pictures from a source folder (the cameras
memory) and takes one pictures for each day (users choice), resizes it for the
web, generates a html page with each pictures in oder and uploads everything to
your webhost. The last step is optional

Needs ```pyexiv2 feh imagemagick```

##Usage

```
python apad.py source destination
```

destination must exist

##Details
This was a quick hack done in an evening. It needs a lot more error checking,
and a bit a care. Also don't run pylint on it :)
