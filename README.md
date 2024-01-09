## Poetry API Project

### Introduction
- I wanted to make a simple api that can hold my favorite poems.
- This api should have normal CRUD capabilities (Create, Read, Update, Delete)
- Output should be a json response

Long Term Goals:
- Write to .txt file with appropriately formatted poem for download. 
- Security (username:password login with specific permissions)

### Python Technology Stack 
- FastAPI (framework)
    - Uvicorn (server)
- Postgresql (database)


### Notes

SQL Commands to make my tables in postgresql (pgAdmin 🐘)

create table authors(
    id SERIAL INTEGER
    firstname VARCHAR(255),
    lastname VARCHAR(255)
)

create table poems(
	id SERIAL PRIMARY KEY,
	author_id integer REFERENCES authors(id),
	title VARCHAR(255),
	poem TEXT, 
	translator_firstname VARCHAR(255),
	translator_lastname VARCHAR(255),
	isbn VARCHAR(50)
);