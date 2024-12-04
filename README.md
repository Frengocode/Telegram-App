<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/2048px-Telegram_logo.svg.png" alt="Project logo"></a>
</p>

<h3 align="center">Telegram-App</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-passed.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> A project aimed at creating a telegram-like app to gain experience in Python development.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

This project is designed to provide experience in building scalable applications with Python. The application simulates a Telegram-like messaging platform using Redis and PostgreSQL for managing messages and users. It uses FastAPI for the backend API and aims to help developers learn how to set up web applications with proper configuration and database handling.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

To run the project, you need to have the following installed:
- Python 3.10+ 
- Redis
- PostgreSQL

### Installing

1. Clone the repository:
   ```bash
   git clone https://github.com/Frengocode/Telegram-App.git
Create a virtual environment:

```bash
python -m venv venv
Activate the virtual environment:

Windows:
``` bash
Копировать код
.\venv\Scripts\activate
Linux/macOS:
bash
Копировать код
source venv/bin/activate
Install the required dependencies:

bash
Копировать код
pip install -r requirements.txt
Configure the application by editing the core/config.py file. Make sure to provide the correct values for PostgreSQL and Redis connections.

Create the necessary databases for the services. Database files are located in the database/ folder.

🔧 Running the tests <a name = "tests"></a>
You can run the unit tests to verify that everything is working correctly. The tests ensure that the application functions as expected.

Example of running tests:
bash
Копировать код
pytest
🎈 Usage <a name="usage"></a>
Once everything is set up, you can run the application with the following command:

```bash
uvicorn app.app:app --reload
This will start the application on localhost with hot-reloading enabled. You can now access it through your browser or use it with an HTTP client.

🚀 Deployment <a name = "deployment"></a>
For deploying the application on a live system, make sure you have the correct configuration files for production. You may also want to use tools like Docker for containerization and setting up production-ready environments.

⛏️ Built Using <a name = "built_using"></a>
FastAPI - Web Framework
PostgreSQL - Database
Redis - Caching and messaging system
✍️ Authors <a name = "authors"></a>
@Frengocode - Idea & Initial work
See also the list of contributors who participated in this project.

🎉 Acknowledgements <a name = "acknowledgement"></a>
Hat tip to anyone whose code was used
Inspiration: Telegram, FastAPI, Redis, PostgreSQL
