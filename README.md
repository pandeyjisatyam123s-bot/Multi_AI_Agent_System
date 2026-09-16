# Multi-Agent Research System

A comprehensive multi-agent research system built with LangGraph, FastAPI, and Streamlit.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your API keys.
3. Run the backend API:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Run the frontend UI:
   ```bash
   streamlit run frontend/app.py
   ```
