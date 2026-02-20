""" if create then need to  virture environment and install requirements.txt
python -m venv venv , protect api for use a  .env file and use python-dotenv to load it in app.py
if need to update requirements.txt then pip freeze > requirements.txt
if need run app.py then streamlit run app.py
i used chromadb for memory and groq for llm calls, both are very easy to use and fast, no embedding model used in chromadb for now to keep it simple and fast, just storing text as is, and using hash of text as id to avoid duplicates
i used prompts.py to keep the system prompt separate and clean, and memory.py to keep memory functions separate, app.py is the main streamlit app that ties everything together, it handles user input, displays chat messages, and calls the groq client for responses, 
also manages session state for messages and user name, and uses the memory functions to save and retrieve user information
i used zero-shot prompting with the system prompt to guide the llm's behavior, and the llm is expected to follow the instructions in the system prompt to act as a communication skills coach for the user
i delete .env file before sharing code here, and added a placeholder in .env for the api key, make sure to replace it with your actual api key when running the app in .streamlit, you can also use st.secrets to manage secrets in streamlit cloud deployment
necessary .env not include when deploying to streamlit cloud, instead use st.secrets to manage secrets in streamlit cloud deployment"""