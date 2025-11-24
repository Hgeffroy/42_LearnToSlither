# 🐍 42_LearnToSlither  
*A neural network that learns to play Snake — built from scratch.*

## 🎯 Description  
**LearnToSlither** is an École 42 AI project in which you must implement a neural network capable of playing a variant of the classic **Snake** game.

I built:
- a minimal **2D Snake environment**,  
- a **fully custom QTable**,  
- a **training process**,  
- a visualization interface to watch the snake learn and play.

This project avoids using external ML frameworks (no TensorFlow/PyTorch) to ensure full understanding of neural networks.

## 🛠️ Installation  
- Ensure you have **Python 3.10+** installed.
- Install dependencies:
```bash
pip install -r requirements.txt
```

## 📌 Concepts Covered
### 🧠 Reinforcment training
- QTable
- Bellman equation
- Exploration vs Exploitation

### 🐍 Game Environment
- Snake logic (movement, collisions, food generation)
- Frame update timing
- Grid management
- Rendering (pygame)

### 📚 ML Workflow
- Training loop
- Evaluating AI performance over time
