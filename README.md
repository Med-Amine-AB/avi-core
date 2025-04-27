# Avi Care: AI-Powered Personal Health Companion

## Project Overview

### Problem
In Morocco, wearable devices collect valuable health data (e.g., heart rate, sleep patterns, SpO2) but fail to provide actionable insights. This gap leaves users, especially in rural areas, without real-time health advice or emergency support.

### Solution
**Avi Care** is an AI-powered personal health companion that bridges this gap by:
- Collecting health data from existing wearable devices.
- Analyzing the data using AI to detect dehydration, stress, injuries, and more.
- Providing real-time actionable advice (e.g., "Hydrate now" or "Rest for potential sprain").
- Generating emergency health reports via QR codes for doctors.

Avi Care empowers users with timely health insights and improves access to healthcare, especially in underserved communities.

---

## Key Features

1. **Hydration Monitoring**  
   Detects dehydration risks and advises users to hydrate.

2. **Stress Detection**  
   Monitors stress levels and provides relaxation tips.

3. **Sleep Quality Analysis**  
   Tracks sleep patterns and offers suggestions for better rest.

4. **Early Injury Detection**  
   Identifies potential injuries based on movement and health data.

5. **Emergency Health Reports**  
   Generates QR-coded reports for doctors, enabling faster emergency response.

6. **No New Hardware Required**  
   Works seamlessly with existing wearable devices.

---

## Tech Stack

- **Backend**: Flask, Firebase  
- **Mobile App**: Flutter  
- **AI Models**: Custom models for:
  - Injury detection
  - Stress detection
  - Sleep quality analysis
  - Cardiovascular health monitoring

---

## Installation and Usage

### Prerequisites
- Python 3.8+
- Flutter SDK
- Firebase account for backend setup

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/avi-care.git
   cd avi-care/backend