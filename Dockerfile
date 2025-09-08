FROM python:3.9-slim

WORKDIR /

# Install ICU and other tools
RUN apt update && \
    apt -y install curl git wget libicu-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY trainer /trainer

ENTRYPOINT ["python", "-m", "trainer.task"]
