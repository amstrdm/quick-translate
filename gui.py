from pathlib import Path
from tkinter import Tk, Canvas, Text, PhotoImage, Toplevel

from deep_translator import GoogleTranslator
from PyMultiDictionary import MultiDictionary

import keyboard


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\coding\Python\quick-translate\quick\build\build\assets\frame0")

#basic tkinter setup
window = Tk()

window.geometry("519x457")
window.configure(bg = "#2E2E2E")
window.title("Translate")

#start minimized
window.withdraw()


translator = GoogleTranslator(source="de", target="en") #set up the translator class in advance for efficiency
dictionary=MultiDictionary()

definition_window = None
synonyms_window = None

def toggle_window():
    if window.state() == 'normal':
        window.withdraw()
    else:
        window.deiconify()
        entry_1.focus_set()
        


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Flag to track whether the entry should be cleared
should_clear = False

definition = ""
synonyms = ""
translated_text = ""


def definition_detail(event=None):
    global definition_window
    global definition
    global translated_text
    #check if definition window is open to open it when control-d gets pressed
    if definition_window is None or not definition_window.winfo_exists():
        # Create a new top-level window (a new, separate window)
        definition_window = Toplevel() 
        definition_window.geometry("695x517")
        definition_window.configure(bg="#2E2E2E")
        definition_window.title(f"Definition of: {translated_text}")
        
        # Create a Text widget within the new window
        T = Text(
            definition_window,  # Make sure the Text widget is a child of the new window
            bd=0,
            bg="#53555a",
            fg="#ffffff",
            highlightthickness=0,
            font=("Roboto", 15),
            padx=20,
            pady=20,
            wrap="word"
        )

        # the first item of the definition list tells us what kind of word it is and is therefore 
        # a list itself so we have to format that with just a comma and then join it with the actual definitions afterwards
        word_type = ", ".join(definition[0])
        #format the other definitions 
        other_definitions = "\n".join(definition[1:])
        # Combine the formatted first definition with the rest of the definitions
        definition_text = f"{word_type}\n{other_definitions}"
        T.insert(1.0, definition_text)  # Insert the definition into the Text widget

        T.config(state="disabled") #make it read-only
        T.pack(expand=True, fill='both')  # Pack the Text widget to fill the new window

        #to close the window even when the definition window itself is in focus we have to specifiy the hotkeys
        #again for the Toplevel window (we're also adding Escape as an additional closing hotkey here)
        definition_window.bind("<Control-d>", lambda event: definition_window.destroy())
        definition_window.bind("<Escape>", lambda event: definition_window.destroy())
    #if it is open we want to close it on press of control-d
    else:
        definition_window.destroy()
        definition_window = None

def synonyms_detail(event=None):
    global synonyms_window
    global synonyms
    global translated_text
    #check if synonyms window is open to open it when control-s gets pressed
    if synonyms_window is None or not synonyms_window.winfo_exists():
        # Create a new top-level window (a new, separate window)
        synonyms_window = Toplevel() 
        synonyms_window.geometry("695x517")
        synonyms_window.configure(bg="#2E2E2E")
        synonyms_window.title(f"Synonyms of: {translated_text}")
        
        # Create a Text widget within the new window
        T = Text(
            synonyms_window,  # Make sure the Text widget is a child of the new window
            bd=0,
            bg="#53555a",
            fg="#ffffff",
            highlightthickness=0,
            font=("Roboto", 15),
            padx=20,
            pady=20,
            wrap="word"
        )
        T.insert(1.0, ", ".join(synonyms))  # Insert the definition into the Text widget
        T.config(state="disabled") #make it read-only
        T.pack(expand=True, fill='both')  # Pack the Text widget to fill the new window

        #to close the window even when the definition window itself is in focus we have to specifiy the hotkeys
        #again for the Toplevel window (we're also adding Escape as an additional closing hotkey here)
        synonyms_window.bind("<Control-s>", lambda event: synonyms_window.destroy())
        synonyms_window.bind("<Escape>", lambda event: synonyms_window.destroy())
    #if it is open we want to close it on press of control-s
    else:
        synonyms_window.destroy()
        synonyms_window = None

    



def translate(event=None):
    global should_clear
    global translator
    global dictionary
    global definition
    global translated_text
    global synonyms


    # Get all text from the first entry widget
    input_text = entry_1.get("1.0", "end-1c")

    #translate the fetched text
    translated_text = translator.translate(input_text)

    entry_2.delete("1.0", "end")  # Clear the second entry widget
    entry_2.insert("1.0", translated_text)  # Insert translated text into the second entry widget

    if len(translated_text.split()) == 1: #prevents checking sentences for definitions
        print(len(translated_text.split()))
         
        definition = dictionary.meaning(translator.target, translated_text)
        print(f"found dictionary meaning: {definition}")
        canvas.itemconfig(Definition, text=f"Definition: {definition[1]}")
       
    if len(translated_text.split()) == 1:
        synonyms = dictionary.synonym(translator.target, translated_text)
        canvas.itemconfig(Synonyms, text=f"Synonyms: {synonyms}")
        print(synonyms)
    should_clear = True

def clear_on_type(event=None):
    global should_clear
    if should_clear:
        entry_1.delete("1.0", "end")  # Clear the entry widget
        should_clear = False  # Reset the flag after clearing

# Toggle function to switch languages
def toggle_languages(event=None):
    global translator

    current_lang1 = canvas.itemcget(Language1, 'text')
    current_lang2 = canvas.itemcget(Language2, 'text')
    
    # Swap the languages and update the translator's source and target
    if current_lang1 == "German":
        canvas.itemconfig(Language1, text="English")
        canvas.itemconfig(Language2, text="German")
        translator.source = "en"
        translator.target = "de"
    elif current_lang2 == "German":
        canvas.itemconfig(Language1, text="German")
        canvas.itemconfig(Language2, text="English")
        translator.source = "de"
        translator.target = "en"
        





canvas = Canvas(
    window,
    bg = "#2E2E2E",
    height = 457,
    width = 519,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)


entry_1 = Text(
    bd=0,
    bg="#2E2E2E",
    fg="#ffffff",
    highlightthickness=0,
    font=("Roboto", 25),
)
entry_1.place(
    x=27.0,
    y=54.0,
    width=205.0,
    height=292.0
)
entry_1.bind("<Return>", translate) #bind pressing "enter" to translating
entry_1.bind("<Key>", clear_on_type)  # Bind any key press to clear the entry widget if required


entry_2 = Text(
    bd=0,
    bg="#53555a",
    fg="#ffffff",
    highlightthickness=0,
    font=("Roboto", 25)
)
entry_2.place(
    x=287.0,
    y=54.0,
    width=205.0,
    height=292.0
)

canvas.create_rectangle(
    76.0,
    10.0,
    183.0,
    44.0,
    fill="",
    outline="#ffffff")

Language1 = canvas.create_text(
    80.0,
    10.0,
    anchor="nw",
    text="German",
    fill="#FFFFFF",
    font=("Roboto", 20)
)

canvas.create_rectangle(
    336.0,
    10.0,
    443.0,
    44.0,
    fill="",
    outline="#ffffff")

Language2 = canvas.create_text(
    345.0,
    10.0,
    anchor="nw",
    text="English",
    fill="#FFFFFF",
    font=("Roboto", 20)
)

Definition = canvas.create_text(
    12.0,
    374.0,
    anchor="nw",
    text="Definition: ",
    fill="#FFFFFF",
    font=("RobotoRoman Bold", 15 * -1),
)

Synonyms = canvas.create_text(
    12.0,
    418.0,
    anchor="nw",
    text="Synonyms: ",
    fill="#FFFFFF",
    font=("RobotoRoman Bold", 15 * -1)
)

#UNIVERSAL HOTKEYS
window.bind("<Control-e>", toggle_languages) # binds control-e to swapping languages
window.bind("<Control-d>", definition_detail) # binds control-d to open/close the definition windows 
window.bind("<Control-s>", synonyms_detail) # binds control-s to open/close the synonyms window
window.bind("<Escape>", lambda event: window.withdraw()) #binds escpape to minimize the main window as an alternative to ctrl+shift+t
keyboard.add_hotkey('ctrl+shift+t', toggle_window) # binds ctrl+shift+t to open/minimize the window


entry_1.focus_set() #set entry1 textarea to focused on startup so the user doesn't have to select it manually

window.resizable(False, False)
window.mainloop()



