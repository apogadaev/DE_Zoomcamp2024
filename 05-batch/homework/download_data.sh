set -e

# https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-10.csv.gz

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-10.csv.gz"
LOCAL_FILE="fhv_tripdata_2019-10.csv.gz"
LOCAL_PREFIX="data/raw/fhv/2019/10"
LOCAL_PATH="${LOCAL_PREFIX}/${LOCAL_FILE}"

mkdir -p ${LOCAL_PREFIX}
wget ${URL} -O ${LOCAL_PATH}