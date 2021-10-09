DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source ${DIR}/env.sh

flask run --host=0.0.0.0 --port=5000
# flask run --host=0.0.0.0 --port=5000
# python3 app.py
