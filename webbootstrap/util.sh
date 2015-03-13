black="\e[1;30m"
red="\e[1;31m"
green="\e[1;32m"
yellow="\e[1;33m"
blue="\e[1;34m"
magenta="\e[1;35m"
cyan="\e[1;36m"
white="\e[1;37m"

Reset() {
    tput sgr0;
}

cecho () {
    msg=${1:-" "}
    color=${2:-$black}

    /bin/echo -n -e $color
    /bin/echo "$msg"

    Reset
    return
}

get_python_major_version() {
    python --version 2>&1 | grep -o -E 'Python ([0-9])' | tail -c 2 | head -c 1
}

verify_digest() {
    local binary="$1"
    local filepath="$2"
    local digest="$3"

    echo "binary: ${binary}"
    echo "filepath: ${filepath}"
    echo "digest: ${digest}"

    echo "${digest}  ${filepath}" | ${binary} -c -

    [ "$?" = "0" ] || exit 1;  # in case 'errexit' isn't set
}

fetch_pkg() {
    local url="$1"
    local pkg="$2"
    local sha1="${3:-0}"

    # fetch only if necessary
    if ! tar xfO "${pkg}" 1> /dev/null 2> /dev/null ; then
        curl --progress-bar --location "${url}" -o "${pkg}"
    fi

    [ "${sha1}" = "0" ] || verify_digest sha1sum "${pkg}" "${sha1}"
}
