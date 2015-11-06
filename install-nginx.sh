#!/usr/bin/env bash

# Download, compile, and install Nginx, defaulting to using Nginx 1.9.6
# and the HTTP2 module with OpenSSL.

set -eux
set -o pipefail

# '0' to use OpenSSL instead of LibreSSL, or SPDY instead of HTTP2
USE_LIBRESSL="${USE_LIBRESSL:-1}"
USE_HTTP2="${USE_HTTP2:-1}"

if [[ "${USE_HTTP2}" = "0" ]]; then
    DEFAULT_NGINX_VERSION="1.9.4"
    DEFAULT_NGINX_DIGEST="479b0c03747ee6b2d4a21046f89b06d178a2881ea80cfef160451325788f2ba8"
    SPDY_MODULE_CONF="--with-http_spdy_module"
else
    DEFAULT_NGINX_VERSION="1.9.6"
    DEFAULT_NGINX_DIGEST="ed501fc6d0eff9d3bc1049cc1ba3a3ac8c602de046acb2a4c108392bbfa865ea"
    SPDY_MODULE_CONF="--with-http_v2_module"
fi

LIBPCRE_VERSION="${LIBPCRE_VERSION:-8.37}"
LIBPCRE_URL="${LIBPCRE_URL:-ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-${LIBPCRE_VERSION}.tar.gz}"
LIBPCRE_DIGEST="${LIBPCRE_DIGEST:-19d490a714274a8c4c9d131f651489b8647cdb40a159e9fb7ce17ba99ef992ab}"

NGINX_VERSION="${NGINX_VERSION:-${DEFAULT_NGINX_VERSION}}"
NGINX_URL="${NGINX_URL:-http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz}"
NGINX_DIGEST="${NGINX_DIGEST:-${DEFAULT_NGINX_DIGEST}}"

LIBRESSL_VERSION="${LIBRESSL_VERSION:-2.2.4}"
LIBRESSL_URL="${LIBRESSL_URL:-http://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-${LIBRESSL_VERSION}.tar.gz}"
LIBRESSL_DIGEST="${LIBRESSL_DIGEST:-6b409859be8654afc3862549494e097017e64c8d167f12584383586306ef9a7e}"

OPENSSL_VERSION="${OPENSSL_VERSION:-1.0.2d}"
OPENSSL_URL="${OPENSSL_URL:-https://www.openssl.org/source/openssl-${OPENSSL_VERSION}.tar.gz}"
OPENSSL_DIGEST="671c36487785628a703374c652ad2cebea45fa920ae5681515df25d9f2c9a8c8"

NGINX_INSTALL_DIR="${NGINX_INSTALL_DIR:-/opt/nginx/${NGINX_VERSION}}"

if [[ "${USE_LIBRESSL}" = "0" ]]; then
    SSL_URL="${OPENSSL_URL}"
    SSL_DIGEST="${OPENSSL_DIGEST}"
else
    SSL_URL="${LIBRESSL_URL}"
    SSL_DIGEST="${LIBRESSL_DIGEST}"
fi

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
trap "rm -rf ${workdir}" EXIT

cd ${workdir}

fetch "${SSL_URL}" "${SSL_DIGEST}" "${workdir}"
fetch "${LIBPCRE_URL}" "${LIBPCRE_DIGEST}" "${workdir}"
fetch "${NGINX_URL}" "${NGINX_DIGEST}" "${workdir}"

cd $(basename ${NGINX_URL} .tar.gz)

./configure \
    --prefix=${NGINX_INSTALL_DIR} \
    --with-openssl=${workdir}/$(basename ${SSL_URL} .tar.gz) \
    --with-pcre=${workdir}/$(basename ${LIBPCRE_URL} .tar.gz) \
    --with-http_ssl_module \
    ${SPDY_MODULE_CONF} \
    --with-file-aio \
    --without-mail_pop3_module \
    --without-mail_smtp_module \
    --without-mail_imap_module

make
sudo make install
