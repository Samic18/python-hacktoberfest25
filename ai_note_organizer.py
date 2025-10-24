import json
import os
from collections import defaultdict
from textblob import TextBlob
from datetime import datetime

NOTES_FILE = "notes.json"

class Note:
    def __init__(self, title, content, tags=None, created_at=None):
        self.title = title
        self.content = content
        self.tags = tags or []
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at
        }

class NoteApp:
    def __init__(self):
        self.notes = []
        self.load_notes()

    def load_notes(self):
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r") as f:
                data = json.load(f)
                for item in data:
                    self.notes.append(Note(**item))

    def save_notes(self):
        with open(NOTES_FILE, "w") as f:
            json.dump([n.to_dict() for n in self.notes], f, indent=2)

    def auto_tag(self, content):
        # Simple NLP: pick nouns/adjectives as tags
        blob = TextBlob(content)
        tags = list({word.lower() for word, pos in blob.tags if pos in ["NN", "NNS", "JJ"]})
        return tags

    def add_note(self):
        title = input("Enter note title: ").strip()
        content = input("Enter note content: ").strip()
        tags = self.auto_tag(content)
        note = Note(title, content, tags)
        self.notes.append(note)
        self.save_notes()
        print(f"✅ Note added with tags: {tags}")

    def list_notes(self):
        if not self.notes:
            print("No notes available!")
            return
        print("\n=== Notes ===")
        for i, n in enumerate(sorted(self.notes, key=lambda x: x.created_at), 1):
            print(f"{i}. {n.title} ({n.created_at}) - Tags: {n.tags}")

    def search_notes(self):
        query = input("Enter keyword to search: ").strip().lower()
        results = [n for n in self.notes if query in n.title.lower() or query in n.content.lower() or query in n.tags]
        if not results:
            print("No matching notes found.")
            return
        print(f"\nFound {len(results)} notes:")
        for n in results:
            print(f"- {n.title} ({n.created_at}) - Tags: {n.tags}")

    def run(self):
        while True:
            print("\n=== AI Note Organizer ===")
            print("1. Add Note")
            print("2. List Notes")
            print("3. Search Notes")
            print("4. Exit")
            choice = input("Choose an option: ").strip()
            if choice == "1":
                self.add_note()
            elif choice == "2":
                self.list_notes()
            elif choice == "3":
                self.search_notes()
            elif choice == "4":
                print("Goodbye! 👋")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    app = NoteApp()
    app.run()
