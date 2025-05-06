import tkinter as tk
from tkinter import scrolledtext, ttk
import json
import random
import os
from datetime import datetime
import spacy

class Chatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("NLP-Enhanced Chatbot")
        self.root.geometry("600x450")

        # Load spaCy model
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            raise OSError("spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")

        # Load knowledge base
        self.knowledge_file = "knowledge.json"
        self.load_knowledge()

        # Set up UI
        self.setup_ui()

        # Start conversation
        self.display_message(random.choice(self.knowledge.get("greetings", ["Hello! I'm here to learn."])), "Bot")

    def load_knowledge(self):
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'r') as f:
                self.knowledge = json.load(f)
        else:
            self.knowledge = {"concepts": {}, "last_conversation": [],
                              "greetings": ["Hello!"],
                              "goodbyes": ["Goodbye!"],
                              "clarifications": ["Could you clarify?"],
                              "learning_acknowledgments": ["Got it, thanks!"],
                              "unknown_responses": ["I don't know that yet."]}
            self.save_knowledge()

    def save_knowledge(self):
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge, f, indent=4)

    def setup_ui(self):
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=18)
        self.chat_display.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.chat_display.tag_configure("user", foreground="blue")
        self.chat_display.tag_configure("bot", foreground="green")

        self.input_field = ttk.Entry(self.root, width=50)
        self.input_field.grid(row=1, column=0, padx=10, pady=10)
        self.input_field.bind("<Return>", self.send_message)

        send_button = ttk.Button(self.root, text="Send", command=self.send_message)
        send_button.grid(row=1, column=1, padx=10, pady=10)

    def display_message(self, message, sender="User"):
        tag = "user" if sender == "User" else "bot"
        self.chat_display.insert(tk.END, f"{sender}: {message}\n", tag)
        self.chat_display.see(tk.END)

    def send_message(self, event=None):
        message = self.input_field.get().strip()
        if not message:
            return
        self.display_message(message)
        response = self.process_message(message)
        self.display_message(response, "Bot")
        self.input_field.delete(0, tk.END)

    def nlp_preprocess(self, message):
        doc = self.nlp(message)
        tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
        return tokens, doc

    def process_message(self, message):
        # Track last 5 messages
        self.knowledge["last_conversation"].append({"timestamp": datetime.now().isoformat(), "message": message})
        self.knowledge["last_conversation"] = self.knowledge["last_conversation"][-5:]

        tokens, doc = self.nlp_preprocess(message)

        # Goodbye intent
        if any(tok in tokens for tok in ["bye", "goodbye", "see"]):
            return random.choice(self.knowledge.get("goodbyes"))

        # Small talk
        if any(tok in tokens for tok in ["how", "are"]) and "you" in tokens:
            return "I'm doing well, thanks for asking!"
        if "what" in tokens and "can" in tokens and "do" in tokens:
            return "I can learn concepts and answer questions about them!"

        # Definition question
        if "what" in tokens and "is" in tokens:
            return self.handle_definition_question(doc)

        # Teaching new definition
        if message.lower().startswith("it is") or message.lower().startswith("it's"):
            return self.handle_new_definition(doc)

        # Default
        return random.choice(self.knowledge.get("clarifications"))

    def handle_definition_question(self, doc):
        # extract noun chunks as concept candidates
        chunks = [chunk.text.lower() for chunk in doc.noun_chunks]
        for chunk in chunks:
            if chunk in self.knowledge["concepts"]:
                return self.knowledge["concepts"][chunk]
        return "I don't know that yet. Could you teach me?"

    def handle_new_definition(self, doc):
        # Expect structure: "It is <definition>"
        # Attempt to find last question concept
        last_q = None
        for msg in reversed(self.knowledge["last_conversation"][:-1]):
            if "what is" in msg["message"].lower():
                last_q = msg["message"].split("what is")[-1].strip().lower()
                break

        # Capture definition text
        definition = "".join([token.text_with_ws for token in doc if token.text.lower() not in ["it", "is", "its"]]).strip()
        if last_q:
            self.knowledge["concepts"][last_q] = definition
            self.save_knowledge()
            return random.choice(self.knowledge.get("learning_acknowledgments"))
        return "Could you clarify what concept this definition is for?"

if __name__ == "__main__":
    root = tk.Tk()
    app = Chatbot(root)
    root.mainloop()

# Requirements:
# pip install spacy
# python -m spacy download en_core_web_sm

