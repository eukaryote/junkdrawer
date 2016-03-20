#!/usr/bin/env bash

# Download, compile, and install Nginx with HTTP2 enabled and LibreSSL for TLS.

set -eux -o pipefail

DEFAULT_NGINX_VERSION="1.9.12"
DEFAULT_NGINX_DIGEST="1af2eb956910ed4b11aaf525a81bc37e135907e7127948f9179f5410337da042"

LIBPCRE_VERSION="${LIBPCRE_VERSION:-8.38}"
LIBPCRE_URL="${LIBPCRE_URL:-ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-${LIBPCRE_VERSION}.tar.gz}"
LIBPCRE_DIGEST="${LIBPCRE_DIGEST:-9883e419c336c63b0cb5202b09537c140966d585e4d0da66147dc513da13e629}"

NGINX_VERSION="${NGINX_VERSION:-${DEFAULT_NGINX_VERSION}}"
NGINX_URL="${NGINX_URL:-http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz}"
NGINX_DIGEST="${NGINX_DIGEST:-${DEFAULT_NGINX_DIGEST}}"

LIBRESSL_VERSION="${LIBRESSL_VERSION:-2.2.6}"
LIBRESSL_URL="${LIBRESSL_URL:-http://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-${LIBRESSL_VERSION}.tar.gz}"
LIBRESSL_DIGEST="${LIBRESSL_DIGEST:-1ee19994cffd047d40f63ba149115dba18a681b0cc923beec301bf424b58d64f}"

NGINX_INSTALL_DIR="${NGINX_INSTALL_DIR:-/opt/nginx/${NGINX_VERSION}}"
NGINX_TMP_DIR="${NGINX_TMP_DIR:-/var/tmp/nginx}"

NGINX_LOG_DIR="${NGINX_LOG_DIR:-/var/log/nginx}"
NGINX_DEFAULT_ERROR_LOG="${NGINX_DEFAULT_ERROR_LOG:-${NGINX_LOG_DIR}/error.log}"
NGINX_DEFAULT_HTTP_LOG="${NGINX_DEFAULT_HTTP_LOG:-${NGINX_LOG_DIR}/access.log}"

NGINX_DEFAULT_USER="${NGINX_DEFAULT_USER:-www-data}"
NGINX_DEFAULT_GROUP="${NGINX_DEFAULT_GROUP:-www-data}"
NGINX_DEFAULT_PID_FILE="${NGINX_DEFAULT_PID_FILE:-/var/run/nginx/pid}"

umask 002

verify() {
    local pkg="$1"
    local digest="$2"
    cd $(dirname "${pkg}")
    cat <<EOF | sha256sum -c
${digest}  ${pkg}
EOF
}

fetch() {
    local url="$1"
    local digest="$2"
    local destdir="$3"
    local tarball=$(basename ${url})
    local origdir=$(pwd)

    cd ${TMPDIR}
    if [[ ! -f "$(basename ${url})" ]]; then
        curl -O "${url}"
    fi
    verify "${tarball}" "${digest}"
    tar -C ${destdir} -xf "${tarball}"
    cd ${origdir}
}

workdir=$(mktemp -d)
# trap "rm -rf ${workdir}" EXIT

cd ${workdir}

fetch "${LIBRESSL_URL}" "${LIBRESSL_DIGEST}" "${workdir}"
fetch "${LIBPCRE_URL}" "${LIBPCRE_DIGEST}" "${workdir}"
fetch "${NGINX_URL}" "${NGINX_DIGEST}" "${workdir}"

# manual patch for nginx-1.9.11+ and libressl-2.2.6 until 2.2.7 is released,
# which will contain the following workaround for nginx
cat <<EOF >> ${workdir}/$(basename ${LIBRESSL_URL} .tar.gz)/Makefile.am

.PHONY: install_sw
install_sw: install
EOF

cd $(basename ${NGINX_URL} .tar.gz)

./configure \
    --prefix=${NGINX_INSTALL_DIR} \
    --error-log-path=${NGINX_DEFAULT_ERROR_LOG} \
    --http-log-path=${NGINX_DEFAULT_HTTP_LOG} \
    --with-openssl=${workdir}/$(basename ${LIBRESSL_URL} .tar.gz) \
    --with-pcre=${workdir}/$(basename ${LIBPCRE_URL} .tar.gz) \
    --with-http_ssl_module \
    --with-http_v2_module \
    --with-file-aio \
    --with-threads \
    --user=${NGINX_DEFAULT_USER} \
    --group=${NGINX_DEFAULT_GROUP} \
    --pid-path=/var/run/nginx/pid \
    --http-client-body-temp-path=${NGINX_TMP_DIR}/client-body \
    --http-proxy-temp-path=${NGINX_TMP_DIR}/proxy-temp \
    --http-fastcgi-temp-path=${NGINX_TMP_DIR}/fastcgi-temp \
    --http-uwsgi-temp-path=${NGINX_TMP_DIR}/uwsgi-temp \
    --http-scgi-temp-path=${NGINX_TMP_DIR}/scgi-temp \
    --without-mail_pop3_module \
    --without-mail_smtp_module \
    --without-mail_imap_module > .build 2>&1

make >> .build 2>&1
sudo make install >> .build 2>&1
for dirpath in $(dirname ${NGINX_DEFAULT_PID_FILE}) ${NGINX_LOG_DIR}  \
        ${NGINX_TMP_DIR}/{client-body,proxy-temp,fastcgi-temp,uwsgi-temp,scgi-temp} ; do
    sudo mkdir -p -m 02755 ${dirpath}
    sudo chown ${NGINX_DEFAULT_USER}:${NGINX_DEFAULT_GROUP} ${dirpath}
done
sudo touch ${NGINX_DEFAULT_PID_FILE}
sudo chown ${NGINX_DEFAULT_USER}:${NGINX_DEFAULT_GROUP} ${NGINX_DEFAULT_PID_FILE}
sudo mv .build ${NGINX_INSTALL_DIR}
