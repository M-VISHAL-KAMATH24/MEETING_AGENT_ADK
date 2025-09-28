# AI Meeting Assistant

An intelligent, multi-agent system designed to enhance meeting productivity by automating administrative tasks. This project is built using Google's **Agent Development Kit (ADK)** and leverages the power of Gemini models for natural language understanding and task delegation.

## Overview

This project demonstrates how to build a sophisticated AI assistant by composing multiple, specialized agents into a collaborative team. Instead of a single monolithic agent, we use a "society of mind" approach where a high-level **Coordinator Agent** manages and delegates tasks to its specialist team members.

## Core Architecture

The system is composed of a team of agents, each with a specific role:

### 1. The Coordinator Agent (The Manager)
This is the main point of contact for the user. Its only job is to understand the user's intent and route the request to the appropriate specialist. It acts as the "brain" of the operation, deciding who should handle each task.

### 2. The Note-Taking Agent (The Scribe)
A specialist agent focused entirely on capturing information.
- **General Notes**: It listens for commands like "take a note" or "remember that" and saves the information to a `meeting_notes.txt` file.
- **Action Item Identification**: It is also trained to identify phrases indicating a task (e.g., "I will," "we need to"). It intelligently separates these action items and saves them to a dedicated `action_items.txt` file, keeping deliverables organized.

### 3. The Agenda-Tracking Agent (The Facilitator)
This agent's role is to keep the meeting on track.
- It can read a predefined `agenda.txt` file to load the meeting's structure.
- It understands commands like "what's next?" and "read the agenda."
- It maintains the state of the meeting, correctly announcing the next topic and ensuring the discussion follows the planned sequence.

## Shared Memory

To enable seamless collaboration, the agents use a shared memory system powered by the ADK's built-in **`InMemoryMemoryService`**.
- This service acts as a temporary "digital whiteboard" for the current session.
- Every user query and agent response is stored, providing all agents with the full context of the conversation.
- When the application is closed, this memory is cleared, making it perfect for single-meeting scenarios.

## Tech Stack

- **Framework**: Google Agent Development Kit (ADK)
- **Language**: Python 3.10+
- **AI Model**: Google Gemini 2.0 Flash
- **Orchestration**: Custom `asyncio` application runner

