FROM public.ecr.aws/lambda/python:3.9

ENV MAKEFLAGS="-j1"
RUN pip install --upgrade pip setuptools wheel

# Install system dependencies required by OpenCV & MediaPipe
RUN yum install -y \
    gcc10 \
    gcc10-c++ \
    make \
    cmake \
    mesa-libGL \
    mesa-libEGL \
    libX11 \
    libXext \
    libXrender \
    libXcursor \
    libXinerama \
    libXrandr \
    && yum clean all

# Set the C++ standard to C++17 for all subsequent compilation steps

ENV CC=/usr/bin/gcc10-gcc
ENV CXX=/usr/bin/gcc10-g++
ENV CXXFLAGS="-std=c++17"

# Upgrade pip
RUN pip install --upgrade pip


# Install sentencepiece first to avoid build issues
RUN pip install sentencepiece==0.1.99

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt


# Copy Lambda handler
COPY app.py .

# Lambda entry point
CMD ["app.lambda_handler"]
