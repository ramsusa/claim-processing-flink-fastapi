# Claim Processing – FastAPI + Flink + Kafka

This project implements a claim-processing pipeline using:

- FastAPI for claim ingestion, validation, enrichment, and manager actions
- Kafka as the event backbone
- Apache Flink (Java) for streaming validation and fraud scoring

## Project Structure

- `fastapi-service/` – FastAPI app
- `flink-job/` – Java Flink job (Maven)
- `README.md` – Project overview

## FastAPI Service

```bash
cd fastapi-service
pip install -r requirements.txt
uvicorn app.main:app --reload
