FROM python:3.12-slim

WORKDIR /workspace

COPY requirements.txt requirements_agent.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements_agent.txt

# Project files are mounted as a volume at runtime (devcontainer / compose)
