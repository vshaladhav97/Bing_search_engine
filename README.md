# Keyword Search Engine



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them:


python --version
pip install django

Setting up Mongo Database connection
1. Create a Database in MongoDB and name it "IR_DB"

# Installation

# 1.Clone the repository
git clone https://github.com/vshaladhav97/Bing_search_engine.git
cd Bing_search_engine

# 2.Set up a Python virtual environment
python -m venv venv
source venv/bin/activate

# 3.Install required packages
pip install -r requirements.txt

# 4.Run database migrations
python manage.py migrate

# 5.Run the development server
python manage.py runserver