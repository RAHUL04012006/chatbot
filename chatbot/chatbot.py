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

        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            raise OSError("spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")

        self.knowledge_file = "knowledge.json"
        self.load_knowledge()
        self.setup_ui()
        self.display_message(random.choice(self.knowledge.get("greetings", ["Hello! I'm here to learn."])), "Bot")

    def load_knowledge(self):
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'r') as f:
                self.knowledge = json.load(f)
        else:
            self.knowledge = {
                "concepts": {},
                "last_conversation": [],
                "greetings": ["Hello!"],
                "goodbyes": ["Goodbye!"],
                "clarifications": ["Could you clarify?"],
                "learning_acknowledgments": ["Got it, thanks!"],
                "unknown_responses": ["I don't know that yet."]
            }
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

    def normalize_text(self, text):
        """Normalize text by converting to lowercase and removing extra spaces"""
        if not text:
            return ""
        return " ".join(text.lower().split())

    def process_message(self, message):
        message = message.strip()
        self.knowledge["last_conversation"].append({
            "timestamp": datetime.now().isoformat(),
            "message": message
        })
        self.knowledge["last_conversation"] = self.knowledge["last_conversation"][-5:]

        # Get normalized tokens for matching
        normalized_msg = self.normalize_text(message)
        tokens = normalized_msg.split()
        
        # Handle "what is" questions first
        if "what" in tokens and ("is" in tokens or "are" in tokens):
            concept = self.extract_concept_from_question(message)
            if concept:
                definition = self.get_concept_definition(concept)
                if definition:
                    return definition

        # Handle learning new concepts
        if normalized_msg.startswith(("it is", "it's", "its", "that is", "this is")):
            return self.handle_new_definition(message)
        
        # Handle greetings and goodbyes
        if any(word in tokens for word in ["hi", "hello", "hey"]):
            return random.choice(self.knowledge.get("greetings"))
        if any(word in tokens for word in ["bye", "goodbye"]):
            return random.choice(self.knowledge.get("goodbyes"))
        
        return random.choice(self.knowledge.get("clarifications"))

    def extract_concept_from_question(self, message):
        """Extract concept name from a question"""
        # Remove question words and punctuation
        message = message.lower().replace("?", "").strip()
        for prefix in ["what is", "what are", "what's", "whats"]:
            if message.startswith(prefix):
                return message[len(prefix):].strip()
        return None

    def get_concept_definition(self, concept):
        """Get definition of a concept"""
        if not concept:
            return None
            
        normalized_concept = self.normalize_text(concept)
        
        # Direct lookup
        if normalized_concept in self.knowledge["concepts"]:
            return self.knowledge["concepts"][normalized_concept]
            
        # Try without articles (a, an, the)
        for article in ["a ", "an ", "the "]:
            if normalized_concept.startswith(article):
                stripped_concept = normalized_concept[len(article):]
                if stripped_concept in self.knowledge["concepts"]:
                    return self.knowledge["concepts"][stripped_concept]
                
        return None

    def handle_new_definition(self, message):
        """Handle new concept definitions"""
        # Find the last "what is" question
        last_concept = None
        for msg in reversed(self.knowledge["last_conversation"][:-1]):
            concept = self.extract_concept_from_question(msg["message"])
            if concept:
                last_concept = concept
                break
        
        if not last_concept:
            return "I'm not sure what concept you're defining. Could you ask 'What is X?' first?"
        
        # Extract the definition
        normalized_msg = self.normalize_text(message)
        for prefix in ["it is", "it's", "its", "that is", "this is"]:
            if normalized_msg.startswith(prefix):
                definition = message[len(prefix):].strip()
                if definition:
                    normalized_concept = self.normalize_text(last_concept)
                    self.knowledge["concepts"][normalized_concept] = definition
                    self.save_knowledge()
                    return random.choice(self.knowledge.get("learning_acknowledgments"))
        
        return "I didn't understand the definition. Could you rephrase it?"

if __name__ == "__main__":
    root = tk.Tk()
    app = Chatbot(root)
    root.mainloop()
