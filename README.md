
# AI-Powered Website Incident Monitoring & RAG Assistant

## Project Overview

An AI-powered DevOps monitoring system that detects website
availability issues, retrieves relevant troubleshooting runbooks
using RAG and FAISS, generates incident analysis with a local
Ollama LLM, and sends email notifications.

## Tech Stack

- Python
- Ollama (Llama 3.2)
- LangChain
- FAISS Vector Search
- RAG (Retrieval-Augmented Generation)
- Gmail SMTP
- HTTP Monitoring
- Environment Variables

## Architecture

Website
   |
   v
Python Website Monitor
   |
   v
HTTP Error Detection
   |
   v
FAISS Runbook Retrieval
   |
   v
Ollama LLM Incident Analysis
   |
   v
Gmail Notification

## Features

- Website availability monitoring
- HTTP error detection
- Local LLM-based incident analysis
- RAG-powered troubleshooting recommendations
- FAISS vector similarity search
- Knowledge base with operational runbooks
- Gmail incident alerts
- Optional Slack webhook integration
- Duplicate incident alert suppression

## Project Structure

Project-1/
|
|-- monitor.py
|-- ai_agent.py
|-- rag_engine.py
|-- notifications.py
|-- knowledge_base/
|   |-- 503_runbook.txt
|-- requirements.txt
|-- .env
|-- .gitignore
|-- README.md

Note: The .env file contains local configuration
and must never be committed to GitHub.

## How It Works

1. The Python monitor checks a configured website.
2. When an HTTP error occurs, an incident is detected.
3. FAISS retrieves relevant troubleshooting information.
4. Ollama analyzes the incident using retrieved context.
5. The notification module sends an email alert.
6. Engineers review evidence before taking action.

## Installation

Install Python dependencies:

    python -m pip install -r requirements.txt

Install Ollama and download the required models:

    ollama pull llama3.2:3b
    ollama pull nomic-embed-text

Configure environment variables locally.

Build the FAISS index:

    python rag_engine.py

Run the monitoring system:

    python monitor.py

## Security

- Credentials are stored in environment variables.
- Secrets are excluded from Git using .gitignore.
- AI recommendations require human validation.
- No automatic production remediation is performed.

## Future Enhancements

- Multi-website monitoring
- Kubernetes logs and metrics integration
- Additional HTTP error runbooks
- LangGraph multi-agent incident workflows
- Web dashboard
- Incident history and reporting
- CI/CD pipeline integration

## Project Status

Working local prototype:
Monitoring, RAG retrieval, Ollama analysis,
and Gmail notification have been tested.
