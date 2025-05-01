import tkinter as tk
from tkinter import scrolledtext, ttk
import json
import random
import os
from datetime import datetime

class Chatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Learning Chatbot")
        self.root.geometry("600x400")
        
        # Load knowledge base
        self.knowledge_file = "knowledge.json"
        self.load_knowledge()
        
        # Set up UI
        self.setup_ui()
        
        # Start conversation
        self.display_message(random.choice(self.knowledge["greetings"]), "Bot")

    def load_knowledge(self):
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'r') as f:
                self.knowledge = json.load(f)
        else:
            with open(self.knowledge_file, 'w') as f:
                json.dump({"concepts": {}, "last_conversation": []}, f)
            self.knowledge = {"concepts": {}, "last_conversation": []}

    def save_knowledge(self):
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge, f, indent=4)

    def setup_ui(self):
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=60, height=15
        )
        self.chat_display.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.chat_display.tag_configure("user", foreground="blue")
        self.chat_display.tag_configure("bot", foreground="green")

        # Input field
        self.input_field = ttk.Entry(self.root, width=50)
        self.input_field.grid(row=1, column=0, padx=10, pady=10)
        self.input_field.bind("<Return>", self.send_message)

        # Send button
        send_button = ttk.Button(self.root, text="Send", command=self.send_message)
        send_button.grid(row=1, column=1, padx=10, pady=10)

    def display_message(self, message, sender="User"):
        tag = "user" if sender == "User" else "bot"
        self.chat_display.insert(tk.END, f"{sender}: {message}\n", tag)
        self.chat_display.see(tk.END)

    def send_message(self, event=None):
        message = self.input_field.get().strip()
        if message:
            self.display_message(message)
            response = self.process_message(message)
            self.display_message(response, "Bot")
            self.input_field.delete(0, tk.END)

    def process_message(self, message):
        # Update conversation history
        self.knowledge["last_conversation"].append({
            "timestamp": datetime.now().isoformat(),
            "message": message
        })
        self.knowledge["last_conversation"] = self.knowledge["last_conversation"][-5:]

        # Check for goodbye
        if any(word in message.lower() for word in ["bye", "goodbye", "see you"]):
            return random.choice(self.knowledge["goodbyes"])

        # Check if user is teaching
        if "it's" in message.lower() or "it is" in message.lower() or "its" in message.lower():
            # Get the last question from conversation history
            last_question = None
            for msg in reversed(self.knowledge["last_conversation"]):
                if "what is" in msg["message"].lower() or "define" in msg["message"].lower():
                    last_question = msg["message"]
                    break
            
            if last_question:
                concept, definition = self.extract_definition(message)
                if concept and definition:
                    # Clean up the concept name
                    concept = concept.strip().lower()
                    self.knowledge["concepts"][concept] = definition
                    self.save_knowledge()
                    return random.choice(self.knowledge["learning_acknowledgments"])
            
            return random.choice(self.knowledge["clarifications"])

        # Check for learning
        if "is" in message.lower() or "define" in message.lower():
            concept = self.extract_concept(message)
            if concept:
                # Clean up the concept name
                concept = concept.strip().lower()
                # Check if we know about this concept
                if concept in self.knowledge["concepts"]:
                    return self.knowledge["concepts"][concept]
                else:
                    return random.choice(self.knowledge["unknown_responses"])
            else:
                return random.choice(self.knowledge["clarifications"])

        # Handle small talk
        if "how are you" in message.lower():
            return "I'm doing well, thank you! How about you?"
        elif "what can you do" in message.lower():
            return "I can learn new concepts and answer questions about what I've learned!"

        # Default response
        return random.choice(self.knowledge["clarifications"])

    def extract_concept(self, message):
        message = message.lower()
        if "what is" in message:
            return message.split("what is")[1].strip()
        elif "define" in message:
            return message.split("define")[1].strip()
        return None

    def extract_definition(self, message):
        message = message.lower()
        
        # Get the last question asked concept
        last_concept = None
        for msg in reversed(self.knowledge["last_conversation"][:-1]):  # Exclude the current message
            if "what is" in msg["message"].lower():
                last_concept = self.extract_concept(msg["message"])
                break
            elif "define" in msg["message"].lower():
                last_concept = self.extract_concept(msg["message"])
                break
        
        # Check if message starts with it/its/it's/it is
        if message.startswith("it") or message.startswith("its") or message.startswith("it's") or message.startswith("it is"):
            # If this is a direct answer to a previous question
            if last_concept:
                return last_concept, message
        
        # Original parsing logic
        if "it's" in message:
            parts = message.split("it's")
        elif "it is" in message:
            parts = message.split("it is")
        elif "its" in message:  # Added to handle missing apostrophe
            parts = message.split("its")
        else:
            return None, None

        if len(parts) > 1:
            concept = parts[0].strip()
            definition = parts[1].strip()
            # If concept is empty but we have a last_concept from previous question
            if not concept and last_concept:
                concept = last_concept
            return concept, definition
        return None, None

if __name__ == "__main__":
    root = tk.Tk()
    app = Chatbot(root)
    root.mainloop()
