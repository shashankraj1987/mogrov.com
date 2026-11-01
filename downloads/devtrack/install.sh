#!/usr/bin/env sh
set -e

REPO="sraj0501/Devtrack_"
INSTALL_DIR="${DEVTRACK_INSTALL_DIR:-$HOME/.local/bin}"

case "$(uname -s)" in
  Linux) os=linux ;;
  Darwin) os=darwin ;;
  *) echo "Unsupported operating system. See https://mogrov.com/downloads/devtrack/" >&2; exit 1 ;;
esac
case "$(uname -m)" in
  x86_64|amd64) arch=amd64 ;;
  arm64|aarch64) arch=arm64 ;;
  *) echo "Unsupported architecture. See https://mogrov.com/downloads/devtrack/" >&2; exit 1 ;;
esac

command -v curl >/dev/null 2>&1 || { echo "curl is required" >&2; exit 1; }
VERSION=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" |
  sed -n 's/.*"tag_name": *"\([^"]*\)".*/\1/p' | head -n 1)
[ -n "$VERSION" ] || { echo "Could not find the latest release" >&2; exit 1; }

ARCHIVE="devtrack_${os}_${arch}.tar.gz"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT
echo "Downloading DevTrack ${VERSION} for ${os}/${arch}..."
curl -fsSL "https://github.com/${REPO}/releases/download/${VERSION}/${ARCHIVE}" -o "${TMP_DIR}/${ARCHIVE}"
tar -xzf "${TMP_DIR}/${ARCHIVE}" -C "$TMP_DIR"
mkdir -p "$INSTALL_DIR"
install -m 755 "${TMP_DIR}/devtrack" "${INSTALL_DIR}/devtrack"
echo "Installed to ${INSTALL_DIR}/devtrack"
case ":${PATH}:" in
  *":${INSTALL_DIR}:"*) echo "Run: devtrack setup" ;;
  *) echo "Add ${INSTALL_DIR} to PATH, then run: devtrack setup" ;;
esac
