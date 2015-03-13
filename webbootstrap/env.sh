BINDIR="$(cd $(dirname ${BASH_SOURCE[0]:-$0}) && pwd -P)"

NODE_INSTALL_DIR="${NODE_INSTALL_DIR:-/opt/node/0.10.29}"
PHANTOMJS_INSTALL_DIR="${PHANTOMJS_INSTALL_DIR:-/opt/phantomjs/1.9.7}"

extra_paths=(
    "${NODE_INSTALL_DIR}"/bin
    "${PHANTOMJS_INSTALL_DIR}"/bin
    "${BINDIR}"
)

for p in ${extra_paths[@]}; do
    PATH="${p}:${PATH}"
done
