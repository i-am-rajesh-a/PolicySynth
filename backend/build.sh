#!/bin/bash

# Install system dependencies for PyMuPDF
apt-get update
apt-get install -y \
    build-essential \
    libfreetype6-dev \
    libharfbuzz-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    libpng-dev \
    libtiff5-dev \
    libwebp-dev \
    libxcb1-dev \
    pkg-config \
    zlib1g-dev

# Install Python dependencies
pip install -r requirements.txt 