# Bharat-Mat – Tensor Troops

Bharat-Mat is a politically neutral, tech-driven **civic** platform that helps Indian voters verify information, understand reforms like One Nation One Election (ONOE), and fight AI-powered misinformation through explainable evidence and interactive simulations. 

---

## Overview

- One-stop “CitizenPortal” for election information, fact-checking, and reform explainers focused on ONOE. 
- Combines AI agents, official ECI data, and visual simulations to restore voter trust and reduce misinformation impact. 
- Designed to be scalable from a few users to millions using modular microservices and modern AI tooling. 

---

## Core Features

- **Fact Check (FC View)**  
  AI-assisted claim checker that analyzes text, images, and videos, retrieves evidence, and outputs a transparent verdict with proof. 

- **Real-time Fact Feed**  
  Scrollable feed of the latest verified updates and short, crisp information with links to underlying documents. 

- **ECI Situation Room**  
  Aggregates circulars, notifications, and public data from the official ECI website into a voter-friendly interface.   

- **ONOE Visualizer**  
  Interactive map and simulations to show how One Nation One Election impacts governance, cost, and voter experience. 

- **Campaign & Misinformation Views**  
  Campaign hub and misinformation dashboard to surface trending narratives and possible deepfakes.  

- **Chatbot Assistant**  
  Conversational interface to query rules, reforms, and verified facts in plain language. =

---

## Architecture

- **Presentation Layer**  
  React Native app (Expo, TypeScript) with navigation-based views like `FC_View`, `Feed_View`, `ECI_View`, `ONOE_View`, `Campaign_View`, `Misinformation_View`, and `Chatbot_View`. [file:1]  

- **Application Layer**  
  Backend microservices for fact-check orchestration, segmentation, embedding generation, retrieval agents, ECI processing, CMS, and state services behind an API gateway. 

- **Privacy Layer**  
  Authentication and verification services with a Zero-Knowledge Proof (ZKP) privacy shield to protect citizen identities.  

- **Data Layer**  
  Relational database (PostgreSQL/MySQL) plus additional stores like MongoDB and vector databases for retrieval-augmented generation. 

- **External Integrations**  
  DigiLocker API, Social Media APIs, ECI portal API, Twilio (WhatsApp & messaging), and LLM/embedding providers.   

---

## Data & AI Pipeline

- **Data Acquisition**  
  Scrapes or fetches public circulars and notices from the official ECI website via Selenium/API hits.  

- **Parsing & OCR**  
  Uses BeautifulSoup and Tesseract OCR to extract text from web pages and scanned PDFs.  

- **NLP Processing**  
  Performs sentence segmentation and summarization (e.g., DistilBERT) to generate concise headings and summaries for each document. 

### Claim Checking Agent

- Pre-processes viral claims with NER and modality detection (text/image/video).  
- Uses a Vision-Language Model (VLM) for frame sampling in video/image claims. 
- Generates synthetic queries, retrieves evidence from large corpora and official sources, and uses an LLM for reasoned verdicts. 

---

## Tech Stack

- **App & Frontend**  
  React Native (Expo), TypeScript, Expo Application Services (EAS), React Navigation. 

- **Backend & APIs**  
  FastAPI (Python) or Node.js (Express), REST webhooks for Twilio, modular microservices. 

- **Databases & Storage**  
  PostgreSQL, MongoDB, FAISS or Pinecone as vector DB for RAG workflows.   

- **NLP & AI**  
  LLAMA-3, Mixtral, Sentence Transformers, LangChain, LangGraph, spaCy, NLTK, DistilBERT, Vision Language Models.   

- **Messaging & Communication**  
  Twilio Messaging API, Twilio WhatsApp Business API for citizen-facing channels. 

---

## Future Directions

- Deeper integration with official election data sources for richer analytics and alerts. 
- Expanded multilingual support for Indian languages to improve reach and inclusivity. 
- More advanced simulation tools to explain additional electoral reforms and governance changes. 
