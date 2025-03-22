# Start with an Ubuntu base image
FROM ubuntu:20.04

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    python3.5 \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Miniconda to manage Conda environments
RUN curl -sSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh \
    && bash miniconda.sh -b -p /opt/conda \
    && rm miniconda.sh

# Set environment variables for Conda
ENV PATH=/opt/conda/bin:$PATH

# Clone your Git repository to the container (for continuous polling)
RUN git clone https://github.com/wixxxez/TransactionClassificator /app


# Set working directory to the application directory
WORKDIR /app

RUN git switch prod 
# Create a Conda environment named "mono_classificator"
COPY env.yaml /app/

# Assuming you have an environment.yml file to define your Conda environment
RUN conda env create -f environment.yml

# Activate the environment and install pip packages if needed
RUN echo "conda activate mono_classificator" > ~/.bashrc
ENV PATH /opt/conda/envs/mono_classificator/bin:$PATH

# Install pip dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port for the application
EXPOSE 8000