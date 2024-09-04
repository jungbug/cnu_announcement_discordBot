# CNU Notice Discord Bot


## TechStack
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/discord-5865F2?style=for-the-badge&logo=discord&logoColor=white"> 

## DevOps
<img src="https://img.shields.io/badge/dotenv-ECD53F?style=for-the-badge&logo=dotenv&logoColor=white"> <img src="https://img.shields.io/badge/github_actions-181717?style=for-the-badge&logo=github&logoColor=white"/> <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">


## Usage
Please use the following command to initialize local repository:

### Clone
```bash
git clone https://github.com/dAiv-CNU/CNUNoticeDiscordBot.git
```

### Install Dependencies
```bash
poetry install
```

### Env Setting (API Keys, ...)
```bash
cp ./src/cnudicobot/driver/env/base.env ./src/cnudicobot/driver/env/.env
```
And fill the blanks in .env file

### Run Noticer
```bash
python run.py
```
