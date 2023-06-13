# Code-GPT

This project uses for demo purposes the GPT-4 model by OpenAI to connect the terminal to an GPT Agent.

## Prerequisites

Before you begin, ensure you have met the following requirements:

1. You have an OpenAI account with GPT-4 API access.

2. Your OpenAI API key is configured properly. To do this, export your OpenAI API key as an environment variable:

    ```bash
    export OPENAI_API_KEY=<your_key>
    ```

## Setting Up Virtual Environment

This project uses a Python virtual environment (venv) for dependency management. Follow the steps below to set it up:

1. Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

2. Activate the virtual environment:

    - For bash/zsh shell:

        ```bash
        source venv/bin/activate
        ```

    - For fish shell:

        ```bash
        source venv/bin/activate.fish
        ```

3. Install dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

## Running the Program

With the virtual environment activated, you can run the program using the following command:

```bash
python3 codegpt/main.py
