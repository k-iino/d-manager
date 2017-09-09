#!/bin/sh
# 対話的に読み込む
base_dir=$(cd $(dirname "$0"); pwd)

CMD=${base_dir}/d-manager
PICKLE=${base_dir}/product_food.pickle

add_interactively_product_food(){
    $CMD add_interactively product_food -i "$1"
}

set -ue
add_interactively_product_food ${PICKLE}
