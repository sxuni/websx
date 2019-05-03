#!/usr/bin/env bash
set -ex

# 换源
cp /var/www/websx/misc/sources.list /etc/apt/sources.list
mkdir -p /root/.pip
cp /var/www/websx/misc/pip.conf /root/.pip/pip.conf
apt-get update