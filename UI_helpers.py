from tkinter.filedialog import asksaveasfile, askopenfile, askdirectory, askopenfilename
from tkinter import *
import os
import time
from logicNLP import *
from UI_constants import *
from pathlib import Path
import threading


FILENAME = ""


def open_folder():
	global file_names_dict

	directory = askdirectory(title = "Оберіть папку з файлами, які необхідно рандомізувати")

	file_names_dict = {}

	for root, dirs, file in os.walk(directory):
		if root in file_names_dict:
			file_names_dict[root].append(file)
		else:	
			file_names_dict[root] = file


def save_file():
    files = [('All Files', '*.*'),
             ('Python Files', '*.py'),
             ('Text Document', '*.txt')]
    try:
        file = asksaveasfile(filetypes=files, initialfile=FILENAME, defaultextension=".txt")
        # title = "Save the file", defaultextension = ".txt"
        file = open(file.name, 'w', encoding='utf8')
        file.write(text)
        file.close()
    except AttributeError:
        print('Error saving file. Try again!')
        
def preproc(textWidget, isShowingTextChangesVar):
    def preprocWrapped():
        files_ = [('All Files', '*.*'), 
            ('Python Files', '*.py'),
            ('Text Document', '*.txt')]
        file = askopenfile(mode='r', filetypes=files_, defaultextension=files_)
        text = file.read()

        text = text.translate ({ord(c): " " for c in "--@#$%^&*()[]»{};:,/<>\|`~-=_+"}).replace('"',' ')
        text = text.replace("!"," ").replace("'","").replace("?"," ").lower()
        text = ' '.join(text.split())[3:]

        if isShowingTextChangesVar.get():
            textWidget.insert("0.0", text[0:20000])

        file.close()

        file = asksaveasfile(filetypes=files_, defaultextension = files_)
        try:
            file = open(file.name, 'w')
            file.write(text)
            file.close()
        except AttributeError as e:
            print(e)
    
    return preprocWrapped

def open_file(textWidget, isShowingTextChangesVar):
    def openFileWrapped():
        global text
        files = [('All Files', '*.*'), 
            ('Python Files', '*.py'),
            ('Text Document', '*.txt')]
        file = askopenfilename(filetypes=files, defaultextension=files)
        global FILENAME
        FILENAME = Path(file).stem
        with open(file, 'r', encoding='utf8') as f:
            try:
                text = f.read()
                f.close()
                if isShowingTextChangesVar.get():
                    textWidget.insert("0.0", text[0:20000])
            except UnicodeDecodeError as e:
                print('Please, check text format in file.')



    return openFileWrapped

def handleConfiguration(text, strategy, option, K, WIN, KROK):
    global FILENAME
    print(f"PROCESSING {FILENAME}")
    if strategy == GLOBAL:
        
        if option == WORDS:
            FILENAME += f'_SW{K}G'
            return mixing_words_global(text, K)
    else: # LOCAL
        
        if option == WORD_1:
            FILENAME += f'_SW{K}L1w={WIN}s={KROK}'
            return lok1_mix_words_in_sentences(text, K, WIN, KROK)
        elif option == WORD_2:
            FILENAME += f'_SW{K}L2w={WIN}s={KROK}'
            return lok2_mix_words_within_sentences(text, K, WIN, KROK,)
        
def update_status_label(widget, text, root):
    root.after(0, lambda: widget.configure(text=text))

def processFile(textWidget, isShowingTextChanges,  timeWidget, completedFilesWidget, strategy, option, K, WIN, KROK):
    update_status_label(completedFilesWidget, "", textWidget)
    start_time = time.time()

    global text
    processedText = handleConfiguration(text, strategy, option, K, WIN, KROK)
    if processedText != "":
        text = processedText
    
    if isShowingTextChanges:
        textWidget.delete("0.0", END)
        textWidget.insert("0.0", processedText[0:20000])

    finish_time = time.time()
    update_status_label(timeWidget,f'Time: {(finish_time-start_time):.3f}',textWidget)
    if processedText == "" :
        update_status_label(completedFilesWidget, "It is not possible to divide the text into sentences", textWidget)
    else:
        print('Work is done.')

def processFolder(textWidget, isShowingTextChanges, timeWidget, completedFilesWidget, strategy, option, K, WIN, KROK):
    update_status_label(completedFilesWidget, "", textWidget)

    if isShowingTextChanges:
        textWidget.delete("0.0", END)

    fileCounter = 0
    successCounter = 0
    numAllFiles = 0
    directory_for_save = askdirectory(title = "Оберіть папку для збереження результатів")
    for root,_,_ in os.walk(directory_for_save):
        save_folder = root
        break
    
    global FILENAME
    start_time = time.time()



    for i, j in file_names_dict.items():
        numAllFiles = len(j)
        if fileCounter == 0:
            update_status_label(completedFilesWidget, f'Processed: {fileCounter}/{numAllFiles} ', textWidget)

        for x in j:
            randomizedText = ""
            with open(f"{i}/{x}", 'r', encoding='utf8') as f:
                text = ""
                try:
                    text = f.read()
                except Exception as e:
                    print("Skipping file", x)
                    continue
                
                if len(text) == 0:
                    print("Skipping file", x)
                    continue
                
                FILENAME = x[0:-4]
                f.close()

                randomizedText = handleConfiguration(text, strategy, option, K, WIN, KROK)             

                if randomizedText != "":
                    if isShowingTextChanges:
                        textWidget.insert(str(float(fileCounter)), f'{x} done!\n' )
                        
                    print(f'{fileCounter} Finished shuffling for {FILENAME}\n')
                    successCounter += 1
                    with open(f'{save_folder}/{FILENAME}.txt', 'w', encoding='utf8') as f:
                        f.write(randomizedText)
                else:
                    print("Failed to randomize the text. It is not possible to divide the text into sentences\n")
                
                fileCounter +=1
                update_status_label(completedFilesWidget, f'Processed: {fileCounter}/{numAllFiles} ', textWidget)


    update_status_label(completedFilesWidget, f'Successfully processed: {successCounter}/{numAllFiles} ', textWidget)
    finish_time = time.time()
    update_status_label(timeWidget, f'Time: {(finish_time - start_time):.3f}', textWidget)
    print('Work is done.')

def start(btnStart, textWidget, isShowingTextChangesVar, timeWidget, completedFilesWidget, workModeVar, strategyVar, globalOptionsVar, localOptionsVar, numberOfShufflesWidget, windowWidget, stepWidget):
    def startWrapped():
        try:
            try:
                K = int(numberOfShufflesWidget.get())
            except Exception:
                print("Invalid number of shuffles")
                return

            WIN = 0
            KROK = 0

            workMode = workModeVar.get()
            strategy = strategyVar.get()
            if strategy == GLOBAL:
                option = globalOptionsVar.get()
            else:
                option = localOptionsVar.get()
                try:
                    WIN = int(windowWidget.get())
                except Exception:
                    print("Invalid Window for Local strategy")
                    return

                try:
                    KROK = int(stepWidget.get())
                except Exception as e:
                    print("Invalid Step for Local strategy")
                    return
            
            
            isShowingTextChanges = isShowingTextChangesVar.get()
           

            if workMode == FILE:
                processFile(textWidget, isShowingTextChanges, timeWidget, completedFilesWidget, strategy, option, K, WIN, KROK)
            else:
                processFolder(textWidget, isShowingTextChanges, timeWidget, completedFilesWidget, strategy, option, K, WIN, KROK)

            btnStart.config(state='normal')



        except Exception as e:
            print(e)
            btnStart.config(state='normal')
    
    btnStart.config(state='disabled')
    threading.Thread(target=startWrapped, daemon=True).start()
