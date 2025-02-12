# Use the Qt base image
FROM my-qt-base

# Set the working directory
WORKDIR /app

# Clone your GitHub repository
RUN apt update && apt install -y git && \
    git clone https://github.com/allenstetson/StetsonProjectManager.git /app

# Install Python dependencies if needed
RUN apt install -y python3 python3-pip && \
    pip3 install -r requirements.txt

# Set default command to run your app
CMD ["python3", "app.py"]
