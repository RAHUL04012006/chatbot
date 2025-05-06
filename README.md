# NLP-Enhanced Chatbot

This repository contains a Python-based chatbot with a clean Tkinter GUI that utilizes NLP techniques for intelligent interactions. The chatbot is designed to learn new information from users, store it persistently in a JSON file, and respond to questions intelligently using plain text pattern matching. It also integrates the `spaCy` library for enhanced text processing.


<img width="444" alt="Image" src="https://github.com/user-attachments/assets/83741647-bdd6-462b-a594-f9124e4c68b7" />

## Features

- **Interactive GUI**: Built with `Tkinter` for a clean and user-friendly chat interface.
- **Knowledge Learning**: Learns new concepts from user interactions and stores them persistently in a JSON file.
- **NLP Integration**: Uses `spaCy` for natural language processing, enabling better understanding of user queries.
- **Stored Knowledge**: Retains information about concepts, greetings, goodbyes, and clarifications.
- **Dynamic Responses**: Can answer "What is/are" questions about learned concepts and handle greetings, goodbyes, and unknown inputs.
- **Customizable Responses**: Easily extendable knowledge base for greetings, goodbyes, clarifications, and learning acknowledgments.

## Installation

### Prerequisites
- Python 3.7 or higher
- Required Python libraries:
  - `tkinter` (comes pre-installed with Python on most systems)
  - `spacy`
  - `json`
  - `random`

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/RAHUL04012006/chatbot.git
   cd chatbot/chatbot
   ```

2. Install the required libraries:
   ```bash
   pip install spacy
   ```

3. Download the `spaCy` language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Run the chatbot:
   ```bash
   python chatbot.py
   ```

## How It Works

1. **Startup**: The chatbot loads its knowledge base from a `knowledge.json` file. If the file does not exist, it initializes with default values.
2. **User Interaction**: Users can type messages in the input field, and the bot responds dynamically based on its knowledge base.
3. **Learning New Concepts**:
   - Ask a question like "What is X?"
   - Provide a definition starting with phrases like "It is", "This is", etc.
   - The bot saves the concept and definition for future use.
4. **Persistent Storage**: The chatbot saves all learned concepts in the `knowledge.json` file so that the knowledge is retained across sessions.

## File Structure

```
chatbot/
├── chatbot.py          # Main chatbot script
├── knowledge.json      # File to store knowledge persistently (auto-generated)
```

## Key Functionalities

1. **Knowledge Management**:
   - `load_knowledge()`: Loads the knowledge base from `knowledge.json`.
   - `save_knowledge()`: Saves the current knowledge base to `knowledge.json`.

2. **Message Handling**:
   - `process_message(message)`: Processes user input and determines the bot's response.
   - `extract_concept_from_question(message)`: Extracts concepts from "What is/are" questions.
   - `handle_new_definition(message)`: Handles new concept definitions and stores them.

3. **Natural Language Processing**:
   - Uses the `spaCy` `en_core_web_sm` model to tokenize and process text for better understanding.

4. **GUI Elements**:
   - `ScrolledText` widget for displaying the chat history.
   - `Entry` widget for user input.
   - `Button` for sending messages.

## Example Usage

1. **Start the chatbot**:
   - The bot greets you with a random greeting (e.g., "Hello!").

2. **Ask a question**:
   - User: "What is Python?"
   - Bot: "I don't know that yet."

3. **Teach the bot**:
   - User: "It is a programming language."
   - Bot: "Got it, thanks!"

4. **Re-ask the question**:
   - User: "What is Python?"
   - Bot: "It is a programming language."

5. **End the conversation**:
   - User: "Goodbye"
   - Bot: "Goodbye!"

## Notes

- If the `spaCy` model is not installed, the chatbot will raise an error. Install the `en_core_web_sm` model using the command provided in the installation steps.
- The chatbot limits its memory of past conversations to the last 5 messages for better efficiency.

## Future Enhancements

- Add support for more complex NLP features, such as intent recognition and sentiment analysis.
- Enable integration with external APIs for dynamic knowledge updates.
- Enhance the GUI with additional customization options and themes.
- Add multilingual support using additional `spaCy` models.

---
