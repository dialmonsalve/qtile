#!/bin/bash

# Configuración de teclado
setxkbmap latam &


~/.screenlayout/resolution.sh

nitrogen --restore &

udiskie -t &
nm-applet &
volumeicon &
cbatticon -u 5 &

