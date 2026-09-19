# Scalable Agentic System

## 1. Overview

This project implements a scalable agentic system that can select and execute the correct tool from a growing set of APIs.

The prototype is designed around a PayPal-style API ecosystem containing tools for:

- Invoice management
- Payments
- Disputes
- Sales reports

The architecture also includes:

- RAG / Knowledge Base search
- System capability and status search
- Multi-step workflow execution
- Parameter validation
- Error handling
- Service/category filtering
- Top-K tool selection

The design can be extended from a small number of tools to hundreds of APIs without exposing all tools to the agent at the same time.

---

## 2. Problem Statement

An agentic system may need to work with hundreds or thousands of APIs.

For example:

- Create an invoice
- Send a payment
- Check a dispute
- Get a sales report
- Search a knowledge base
- Search system capabilities

If every available tool is presented to the agent for every request, tool selection can become inefficient and inaccurate.

This project addresses that problem using routing, category filtering, tool ranking, validation, and controlled execution.

---

## 3. Example User Requests

### Invoice

```text
Create an invoice for John for $50