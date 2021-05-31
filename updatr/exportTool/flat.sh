#!/bin/sh

base=`pwd`
loc=~/github/dirkroorda/historisch-eefde/_temp/Flat

$base/osxphotos export /Users/dirk/Pictures/EEE.photoslibrary $loc --load-config $base/flat.toml
