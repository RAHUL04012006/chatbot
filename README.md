NLP-Enhanced Chatbot
This project is an NLP-Enhanced Chatbot built with Python and a graphical user interface (GUI) using Tkinter. The chatbot is capable of learning new information, storing it permanently in a JSON file, and responding to questions intelligently with the help of natural language processing (NLP) using the spaCy library.

Features
User-Friendly GUI: The chatbot has a clean and intuitive Tkinter-based GUI.
Natural Language Processing: Uses spaCy for NLP tasks such as tokenization, lemmatization, and stopword removal.
Knowledge Retention: Learns new concepts during conversations and stores them in a JSON file for future use.
Intelligent Responses: Responds to user input using plain text pattern matching and predefined knowledge.
Customizable Greetings: The chatbot starts with random greetings from its knowledge base.
Handles Definitions: Can answer "What is..." questions and learn new definitions on the fly.
Small Talk: Capable of simple conversational interactions like greetings and goodbyes.
Installation
Clone the repository:

bash
git clone https://github.com/RAHUL04012006/chatbot.git
cd chatbot
Install the required dependencies:

bash
pip install spacy
python -m spacy download en_core_web_sm
Run the chatbot:

bash
python chatbot.py
Requirements
Python 3.7 or higher
Required libraries:
tkinter (comes pre-installed with Python)
spacy
json
random
os
datetime
Usage
Launch the chatbot by running the chatbot.py script.
Type your message in the input field and press Enter or click the "Send" button to interact with the chatbot.
You can ask the chatbot questions like:
"What is Python?"
"How are you?"
"What can you do?"
Teach the chatbot new concepts by replying with "It is..." or "It's...".
Knowledge File
The chatbot uses a JSON file named knowledge.json to store its knowledge base, including:

Learned concepts and definitions.
Recent conversation history (last 5 messages).
Predefined responses for greetings, goodbyes, clarifications, etc.
The knowledge file will be automatically created and updated in the working directory.

Key Functionalities
1. Handling Definitions
The chatbot extracts the concept from user input (e.g., "What is NLP?") and checks if it exists in its knowledge base.
If the concept is unknown, the chatbot requests the user to teach it by replying with "It is..." followed by the definition.
2. Learning New Concepts
The chatbot retains new definitions provided by the user and stores them in the knowledge.json file.
3. NLP Preprocessing
Uses spaCy to lemmatize and preprocess user input for better understanding.
Removes stopwords and punctuation for effective pattern matching.
4. Small Talk and Greetings
The chatbot has predefined responses for greetings, goodbyes, and small talk.
Example Interaction
Code
User: Hello
Bot: Hello! I'm here to learn.

User: What is Python?
Bot: I don't know that yet. Could you teach me?

User: It is a programming language.
Bot: Got it, thanks!

User: What is Python?
Bot: A programming language.
Notes
Ensure that the spaCy model en_core_web_sm is downloaded before running the chatbot. You can download it by running:

bash
python -m spacy download en_core_web_sm
The chatbot can handle up to 5 recent messages in its conversation history for context tracking.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Author
This chatbot was developed by RAHUL04012006. Contributions are welcome!
