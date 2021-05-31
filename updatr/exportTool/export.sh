#!/bin/sh


base=`pwd`
today=`date '+%Y-%m-%dT%H-%M-%S'`
# today='2021-05-27T12-57-44'

mkdir -p ../EenEeuwEefde/Modified/$today

cd ../EenEeuwEefde/Modified/$today

python3 $base/updates.py bu ~/github/dirkroorda/historisch-eefde/_temp '../../Flat'

$base/osxphotos export /Users/dirk/Pictures/EEE.photoslibrary $base/../EenEeuwEefde/Flat --load-config $base/flickr.toml

python3 $base/updates.py up ~/github/dirkroorda/historisch-eefde/_temp '../../Flat'

$base/osxphotos export /Users/dirk/Pictures/EEE.photoslibrary /Users/dirk/Dropbox/EenEeuwEefde --load-config $base/dropbox.toml
