# Bfu lab checker bot

## Before start

- You need to have python 3.10 or higher, pip and venv installed
- You need to have to install [PostgreSQL](https://www.postgresql.org/download/)

# Setup

> Note: if you know how to setup venv go to step 4

1. Setup your virtualenv<br/>
   `python -m venv .venv`

2. Next step activate it<br/>

- On linux systems:<br/>
  `source .venv/bin/activate`

- On Windows:<br/>
  `.venv\Scripts\activate`

3. Download required libs<br/>
   `pip install -r requirements.txt`

4. Create .env file in `data\.env` and fill it with your data<br/>
   Sample:

```ini
BOT_TOKEN = 'your bot token'

#name of your database
DB_NAME = 'bfu_lab_bot'
#database user
DB_USER = 'postgres'
#database user's password
DB_USER_PASSWORD = 'postgres'
#database host, default localhost
DB_HOST = 'localhost'
#database port, default 5432
DB_PORT = '5432'
```

5. Configure your database<br/>

   1. Move `database\create.py` to project root folder
   2. Run `python create.py`<br/>
      It will create database and tables

6. Run bot<br/>
   `python app.py`

## Database structure<br/>

![Database structure](img/db_structure.png)
