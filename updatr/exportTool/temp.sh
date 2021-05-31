#!/bin/sh

base=`pwd`
loc=~/github/dirkroorda/historisch-eefde/_temp/temp

$base/osxphotos export /Users/dirk/Pictures/EEE.photoslibrary $loc --load-config $base/temp.toml
