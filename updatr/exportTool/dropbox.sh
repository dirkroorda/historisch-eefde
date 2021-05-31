#!/bin/sh

base=`pwd`
loc=/Users/dirk/Dropbox/EenEeuwEefde

$base/osxphotos export /Users/dirk/Pictures/EEE.photoslibrary $loc --load-config $base/dropbox.toml
