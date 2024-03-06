set -e

# https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
LOCAL_FILE="taxi_zone_lookup.csv"
LOCAL_PREFIX="data/raw/zones/"
LOCAL_PATH="${LOCAL_PREFIX}/${LOCAL_FILE}"

mkdir -p ${LOCAL_PREFIX}
wget ${URL} -O ${LOCAL_PATH}