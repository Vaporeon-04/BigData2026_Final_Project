# AI Prompt Monetization System (B2B & B2C)
**Big Data Systems Final Project - Spring 2026**

## Overview
This repository contains the end-to-end data pipeline (Ingestion, Processing, and Delivery) for an AI Prompt generation marketplace. It addresses the "anatomical inconsistency" pain point in AI art generation by providing a curated, data-backed database of verified long-tail prompts.

## Architecture
1. **Ingestion & Processing:** `huggingface_ingestion.py` 
   - Bypasses API limitations by directly ingesting massive `.parquet` datasets from the Hugging Face open-source repository (`poloclub/diffusiondb`).
   - Cleans and filters the data based on heuristic quality thresholds (Prompt length > 100, Steps >= 30) to generate a premium commercial dataset.
2. **Storage:** `verified_prompts_db.csv`
   - The processed and structured data serving as the product database.
3. **Delivery (Working Demo):** `app.py`
   - A Streamlit web dashboard acting as the marketplace front-end. It features dynamic keyword filtering, UI image rendering, and live REST API inference integration (via Pollinations.ai) to instantly generate images based on the prompt.

## How to Reproduce Locally

### 1. Environment Setup
Ensure you have Python installed. Install the required dependencies:

    pip install -r requirements.txt

### 2. Reproduce Data Ingestion (Component 2)
To re-run the data acquisition and processing pipeline from scratch:

    python3 huggingface_ingestion.py

*Note: This will download the remote Parquet metadata and overwrite `verified_prompts_db.csv` with fresh data.*

### 3. Launch the Application
To start the interactive prompt marketplace:

    streamlit run app.py

The application will be accessible at `http://localhost:8501`.