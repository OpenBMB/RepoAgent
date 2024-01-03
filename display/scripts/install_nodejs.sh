#!/bin/bash

# 检查是否已经安装了 nvm
check_nvm_installed() {
    if [ -s "$NVM_DIR/nvm.sh" ]; then
        echo "nvm is already installed"
        return 0
    else
        echo "nvm is not installed"
        return 1
    fi
}

# 安装 nvm
install_nvm_linux() {
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
    source "$NVM_DIR/nvm.sh"
}

install_nvm_mac() {
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
    source "$NVM_DIR/nvm.sh"
}

install_nvm_windows() {
    echo "Downloading nvm for Windows..."
    curl -o nvm-setup.exe -L https://github.com/coreybutler/nvm/releases/download/1.1.12/nvm-setup.exe
    echo "Installing nvm for Windows..."
    ./nvm-setup.exe
    echo "nvm version:"
    nvm -v
    echo "nvm installation for Windows completed."
    rm -f nvm-setup.exe
}

# 安装 Node.js 10
install_nodejs() {
    nvm install 10
    nvm use 10
}

# 检查 Node.js 是否安装成功
check_node() {
    node_version=$(node -v)
    echo "Installed Node.js version: $node_version"
    if [[ "$node_version" == v10* ]]; then
        echo "Node.js 10 is installed successfully."
    else
        echo "Node.js 10 is not installed."
        exit 1
    fi
}

# 检测操作系统并安装 nvm（如果需要）
case "$OSTYPE" in
  linux-gnu*)
    if ! check_nvm_installed; then
        install_nvm_linux
    fi
    ;;
  darwin*)
    if ! check_nvm_installed; then
        install_nvm_mac
    fi
    ;;
  cygwin*|msys*|mingw*|bccwin*|wsl*)
    if ! check_nvm_installed; then
        install_nvm_windows
    fi
    ;;
  *)
    echo "Unsupported OS, You could install nvm manually"
    exit 1
    ;;
esac

# 安装 Node.js 10
install_nodejs

check_node
