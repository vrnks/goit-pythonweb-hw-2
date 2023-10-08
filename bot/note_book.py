import json
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from abc import ABC, abstractmethod


class Note:  # Клас Note представляє окрему нотатку з такими атрибутами:
    # title: Рядок, що представляє заголовок нотатки.
    # content: Рядок, що містить вміст нотатки.
    # tags: Список рядків, які представляють теги, пов'язані з нотаткою.

    def __init__(self, title, content, tags=[]):
        self.title = title
        self.content = content
        self.tags = tags if tags is not None else []

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}\nTags: {', '.join(self.tags)}"


class InvalidFormatError(
    Exception
):  # Клас InvalidFormatError є власним виключенням, яке використовується для обробки помилок невірного формату
    # введення.
    pass


class MyBaseClass(ABC):
    @abstractmethod
    def list_notes(self):  # Перелічує всі нотатки у блокноті.
        pass


class Notebook(
    MyBaseClass
):  # Клас Notebook представляє собою колекцію нотаток і надає методи для їх управління. Він має наступні атрибути:
    # notes: Список об'єктів Note.
    # filename: Назва файлу, який використовується для зберігання нотаток у форматі JSON.

    def __init__(self, filename="notes.json"):
        self.notes = []
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                json.dump([], file)
        else:
            self.load_notes()

    def add_note(
        self, note
    ):  # Додає нову нотатку до блокнота. Перевіряє наявність нотаток з однаковими заголовками і валідує довжину тегів.
        if any(len(tag) > 15 for tag in note.tags):
            raise InvalidFormatError("Invalid format. Tags <= 15")

        # Перевірка на однакові назви
        title = note.title.casefold()
        for existing_note in self.notes:
            if existing_note.title.casefold() == title:
                print("Note with the same title already exists.")
                return

        self.notes.append(note)
        print("Note added!")

    def search_notes(
        self, keyword
    ):  # Шукає нотатки, які містять вказане ключове слово в їхніх заголовках, вмісті або тегах.
        """Пошук нотаток за ключовим словом."""
        keyword = keyword.lower()
        matching_notes = []
        for note in self.notes:
            if (
                keyword in note.title.lower()
                or keyword in note.content.lower()
                or keyword in note.tags
            ):
                matching_notes.append(note)
        return matching_notes

    def find_note(self, title):  # Знаходить нотатку за її заголовком.
        title = title.casefold()
        for note in self.notes:
            if note.title.casefold() == title:
                return note
        return None

    def edit_note(self, title):  # Редагує вміст існуючої нотатки.
        note = self.find_note(title)
        if note is None:
            print("Note not found!")
            return False

        print(f"Editing note: {note.title}")
        print(f"Current content: {note.content}")

        try:
            new_content = input("Enter the new content: ")
            if len(new_content) < 10:
                raise InvalidFormatError(
                    "Invalid format. Content length should be >= 10."
                )
        except InvalidFormatError as error:
            print(error)
        else:
            note.content = new_content
            return True

    def delete_note(self, title):  #  Видаляє нотатку за заголовком.
        title = title.casefold()
        for note in self.notes.copy():
            if note.title.casefold() == title.casefold():
                self.notes.remove(note)
                return True
        return False

    def sort_notes_by_tags(
        self, tag
    ):  # Сортує нотатки за тегами,розміщуючи нотатки з вказаними тегами спереду.
        tag = tag.casefold()
        filtered_notes = [
            note for note in self.notes if tag in [t.casefold() for t in note.tags]
        ]
        sorted_notes = sorted(filtered_notes, key=lambda x: x.title.lower())
        return sorted_notes

    def list_notes(self):  # Перелічує всі нотатки у блокноті.
        if not self.notes:
            print("No notes available.")
        else:
            for i, note in enumerate(self.notes, start=1):
                print(f"{i}. Title: {note.title}")
                print(f"   Content: {note.content}")
                print(f"   Tags: {', '.join(note.tags)}")

    def save_notes(self):  # Зберігає нотатки у JSON-файлі.
        data = [
            {"title": note.title, "content": note.content, "tags": note.tags}
            for note in self.notes
        ]
        with open(self.filename, "w") as file:
            json.dump(data, file)

    def load_notes(self):  # Завантажує нотатки з JSON-файлу.
        with open(self.filename, "r") as file:
            data = json.load(file)
            self.notes = [
                Note(note["title"], note["content"], note["tags"]) for note in data
            ]


# Команди, які підтримує бот.
commands = [
    "add",
    "edit",
    "delete",
    "tag",
    "sort",
    "list",
    "search",
    "load",
    "save",
    "exit",
]

# Створення автозавершення для команд.
command_completer = WordCompleter(commands, ignore_case=True)


def get_command_from_user():
    return prompt("Enter a command: ", completer=command_completer)


def main():
    filename = "notes.json"
    notebook = Notebook(filename)
    notebook.load_notes()

    while True:
        print("\nNotebook Menu:")  # Підтримувані команди.
        print("add = Add Note(Додати нот)")
        print("edit = Edit Note(Редагувати вміст)")
        print("delete = Delete Note(Видалити)")
        print("tag = Add Tag(Додати тег)")
        print("sort = Sort Notes(Сортування)")
        print("list = List Notes(Вивести список)")
        print("search = Search Notes(Пошук)")
        print("load = Load Notes(Завантаження)")
        print("save = Save Notes(Зберігання)")
        print("exit = Exit (and save)")
        print("=" * 10)

        user_input = get_command_from_user()

        if user_input.casefold() == "add":
            # Додати нотатку.
            try:
                title = input("Enter Title: ")
                if len(title) < 5:
                    raise InvalidFormatError(
                        "Invalid format. Title length should be >= 5."
                    )
            except InvalidFormatError as error:
                print(error)
            else:
                try:
                    content = input("Enter content: ")
                    if len(content) < 10:
                        raise InvalidFormatError(
                            "Invalid format. Content length should be >= 10."
                        )
                except InvalidFormatError as error:
                    print(error)
                else:
                    tags = input("Enter Tags (comma-separated or space-separated): ")
                    tags = [tag.strip() for tag in tags.replace(",", " ").split()]
                    note = Note(title, content, tags)
                    notebook.add_note(note)

        elif user_input.casefold() == "edit":
            # Редагувати нотатку.
            title = input("Enter the title of the note to edit: ")

            if notebook.edit_note(title):
                print("Note edited!")

        elif user_input.casefold() == "delete":
            # Видалити нотатку.
            title = input("Enter the title of the note to delete: ").strip()
            if notebook.delete_note(title.casefold()):
                print("Note deleted!")
            else:
                print("Note not found!")

        elif user_input.casefold() == "tag":
            # Додати тег до нотатки.
            title = input("Enter the title of the note to add a tag: ")
            note = notebook.find_note(title)

            if note is None:
                print("Note not found!")

            else:
                new_tags_input = input(
                    "Enter the new tags (comma-separated or space-separated): "
                )
                new_tags = [
                    tag.strip() for tag in new_tags_input.replace(",", " ").split()
                ]

                if not new_tags:
                    print("Invalid format. Tags can't be empty.")

                elif all(len(tag) < 20 for tag in new_tags):
                    if any(tag.casefold() in note.tags for tag in new_tags):
                        print("Some tags already exist for this note.")
                    else:
                        note.tags.extend(new_tags)
                        print("Tags added!")

                else:
                    print("Invalid format. Tags <= 20.")

        elif user_input.casefold() == "sort":
            # Cортування нотаток.
            keyword = input("Enter a keyword to sort notes by: ")

            notes_with_priority = []

            for note in notebook.notes:
                priority = 0

                if any(keyword in tag.lower() for tag in note.tags):
                    priority += 3

                if keyword in note.title.lower():
                    priority += 2

                if keyword in note.content.lower():
                    priority += 1

                notes_with_priority.append((note, priority))
            sorted_notes = sorted(notes_with_priority, key=lambda x: x[1], reverse=True)

            for note, _ in sorted_notes:
                print(note)

        elif user_input.casefold() == "list":
            # Вивести список нотаток.
            notebook.list_notes()

        elif user_input.casefold() == "search":
            # Пошук нотаток за ключовим словом.
            keyword = input("Enter the keyword to search notes by: ")
            matching_notes = notebook.search_notes(keyword)
            if matching_notes:
                print("Found notes:")
                for note in matching_notes:
                    print(note)
            else:
                print("No notes found.")

        elif user_input.casefold() == "reset":
            # Завантажити нотатки з файлу
            # new_filename = input("Enter the filename for loading notes (e.g., notes.json): ")
            new_filename = "notes.json"
            notebook = Notebook(new_filename)
            notebook.load_notes()
            print("Notes loaded from the file as it was before the start.")

        elif user_input.casefold() == "save":
            # Зберегти нотатки у файл.
            notebook.save_notes()
            print("Notes saved to the file.")

        elif user_input.casefold() == "exit":
            # Вийти з програми.

            notebook.save_notes()
            print("Notes saved to the file.")
            print("Bye...")
            break

        else:
            print("I do not understand the command!")


if __name__ == "__main__":
    main()
