# Blog Post Generator using OpenAI API

This application generates blog posts using OpenAI's API. It demonstrates the usage of LLM API with Python and implements token streaming.

## Setup

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the application:
```bash
python python_app.py
```

The application will:
1. Connect to OpenAI's API
2. Generate a blog post based on the given topic
3. Stream the response tokens
4. Save the generated blog post

## Note
Make sure not to commit your `.env` file to Git to keep your API key secure.