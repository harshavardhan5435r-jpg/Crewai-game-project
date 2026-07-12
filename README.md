# 🎮 CrewAI Game Generator

An AI-powered game development assistant that transforms natural language game ideas into structured game concepts and playable Python/Pygame code using CrewAI's multi-agent architecture.

## 🚀 Overview

CrewAI Game Generator leverages multiple AI agents that collaborate to design, plan, and generate simple 2D games. Instead of manually planning game mechanics and writing boilerplate code, users simply describe their game idea, and the AI produces a complete game design along with executable Python code.

This project demonstrates the practical application of Multi-Agent AI systems for software development automation.

---

## ✨ Features

- 🤖 Multi-Agent workflow using CrewAI
- 🎮 Generates complete game ideas from user prompts
- 📝 Creates detailed game mechanics and rules
- 🧠 AI-assisted game architecture planning
- 🐍 Generates Python + Pygame code
- 🌐 Exportable as a web build using Pygbag
- 🔑 Secure API key management using environment variables

---

## 🛠️ Tech Stack

- Python 3.12
- CrewAI
- OpenAI / Gemini LLM
- Serper API
- Pygame
- Pygbag
- Git & GitHub

---

## 📂 Project Structure

```
CrewAI-Game-Project/
│
├── app.py                 # CrewAI agents and workflow
├── main.py                # Application entry point
├── requirements.txt       # Project dependencies
├── build/                 # Generated web build
├── docs/                  # GitHub Pages files
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/CrewAI-Game-Project.git
```

Move into the project directory

```bash
cd CrewAI-Game-Project
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your_key
SERPER_API_KEY=your_key
GEMINI_API_KEY=your_key
```

> **Note:** Never commit your `.env` file to GitHub. Store secrets securely using GitHub Secrets when deploying.

---

## ▶️ Run Locally

```bash
python app.py
```

or

```bash
python main.py
```

---

## 🌍 Web Build

Generate the web version using Pygbag.

```bash
python -m pygbag app.py
```

The generated files will be available inside:

```
build/web/
```

---

## 📸 Screenshots

Add screenshots of the application here.

```
docs/screenshots/
```

---

## 📌 Future Improvements

- Support for multiple game genres
- Enhanced AI-generated graphics
- One-click deployment
- Multiplayer game generation
- Improved UI
- Additional AI agents for testing and optimization

---

## 👨‍💻 Author

**Harsha Vardhan**

B.Tech CSE (AI & ML)

Passionate about Artificial Intelligence, Machine Learning, Multi-Agent Systems, and Software Development.

GitHub: https://github.com/harshavardhan5435r-jpg

LinkedIn: https://www.linkedin.com/in/harshavardhan5435r

---

## ⭐ If you found this project helpful, consider giving it a star!
