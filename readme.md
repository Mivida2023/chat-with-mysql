# Postresgl Python Chatbot with GPT-4 OR Ollama

Welcome to the GitHub repository for our tutorial on building a natural language SQL chatbot using GPT-4! 
This project guides you through the development of a chatbot that can interpret natural language queries, generate SQL queries, and fetch results from a SQL database, all in an intuitive and user-friendly way. It utilizes the power of OpenAI's GPT-4 model, integrated with a Streamlit GUI for an enhanced interaction experience.

🟡 This original repository serves as supporting material for the [YouTube video tutorial](https://youtu.be/YqqRkuizNN4) I invite you to check his great youtube channel.

## Features
- **Natural Language Processing**: Uses GPT-4 to interpret and respond to user queries in natural language.
- **SQL Query Generation**: Dynamically generates SQL queries based on the user's natural language input.
- **Database Interaction**: Connects to a SQL database to retrieve query results, demonstrating practical database interaction.
- **Streamlit GUI**: Features a user-friendly interface built with Streamlit, making it easy for users of all skill levels.
- **Python-based**: Entirely coded in Python, showcasing best practices in software development with modern technologies.

## Brief Explanation of How the Chatbot Works

The chatbot works by taking a user's natural language query, converting it into a SQL query using GPT-4, executing the query on a SQL database, and then presenting the results back to the user in natural language. This process involves several steps of data processing and interaction with the OpenAI API and a SQL database, all seamlessly integrated into a Streamlit application.

Consider the following diagram to understand how the different chains and components are built:

![Chatbot Architecture](./docs/mysql-chains.png)

## Installation
Ensure you have Python installed on your machine. Then clone this repository:

```bash
git clone [repository-link]
cd [repository-directory]
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create your own .env file with the necessary variables, including your OpenAI API key:

```bash
OPENAI_API_KEY=[your-openai-api-key]
```

## Usage
To launch the Streamlit app and interact with the chatbot:

```bash
streamlit run app.py
```

## Contributing
As this repository accompanies the [YouTube video tutorial](https://youtu.be/YqqRkuizNN4), we are primarily focused on providing a comprehensive learning experience. Contributions for bug fixes or typos are welcome.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


Happy Coding! 🚀👨‍💻🤖 and Thank You [Alejandro](https://www.youtube.com/redirect?event=channel_header&redir_token=QUFFLUhqbkZ6OGs4WkxubjhRdFFyTGpDME1KVk8zbTFod3xBQ3Jtc0ttVnFWS3BwWlFZenI2ald3QlZZZl9yczY0LTVTS2ZWczc2THVfMDlUbzFHaGE0SUNicGJONGpXNTkxYS1RWlZlRGNlOEVKUUUyc29LNFAybnRzU251ZTFxdGxQREdhMFNhYWxpTFN2b1FKOE9IRTdTaw&q=https%3A%2F%2Falejandro-ao.com%2F) 
