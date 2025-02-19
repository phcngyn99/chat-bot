FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl build-essential libssl-dev net-tools
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY ./requirement.txt requirement.txt

# Upgrade pip
RUN pip install --upgrade pip
# Use --no-cache-dir to avoid cache issues
RUN pip install --no-cache-dir -r requirement.txt

RUN echo 'alias cl=clear' >> ~/.bashrc 

# CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0"]