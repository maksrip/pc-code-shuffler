import subprocess
import pkg_resources

from tkinter import *
from tkinter.ttk import Checkbutton, Progressbar
from tkinter import scrolledtext

from tkinter import * 
from tkinter import ttk

from UI_constants import *
from UI_helpers import *


EXPANDED_WINDOW_SIZE = (1350, 760)
COLLAPSED_WINDOW_SIZE = (450, 450)

window = Tk()
# window.state("zoomed")
window.title("Program PC")
window.minsize(EXPANDED_WINDOW_SIZE[0], EXPANDED_WINDOW_SIZE[1])
window.maxsize(EXPANDED_WINDOW_SIZE[0], EXPANDED_WINDOW_SIZE[1])

textFrame = None
textWidget = None
timeWidget = None 
completedFilesWidget = None

controlsFrame = None
commonOptionsFrame = None
fileOptionsFrame = None
folderOptionsFrame = None

isShowingTextChangesVar = None
isShowingTextChangesWidget = None

workModeVar = None
strategyWidget = None
strategyVar = None
globalOptionsWidget = None
globalOptionsVar = None
localOptionsWidget = None
localOptionsVar = None

numberOfShufflesWidget = None
numberOfShufflesWidgetInput = None
windowWidget = None
windowWidgetInput = None
stepWidget = None
stepWidgetInput = None
def makeTextView():
    global textFrame
    textFrame = Frame(window, highlightbackground="lightgrey", highlightthickness=2)
    textFrame.pack(side=LEFT, fill=Y, padx=10, pady=10)

    global textWidget
    textWidget = scrolledtext.ScrolledText(textFrame, width=130)
    textWidget.pack(side=LEFT, fill=Y, expand=True)

def makeButtonStart(frame):
    btnStart = Button(
        frame, 
        text=START)
    
    btnStart.config(command=lambda:start(
        btnStart,
        textWidget,
        isShowingTextChangesVar,
        timeWidget,
        completedFilesWidget, 
        workModeVar, 
        strategyVar, 
        globalOptionsVar, 
        localOptionsVar, 
        numberOfShufflesWidgetInput, 
        windowWidgetInput, 
        stepWidgetInput,
        )
    )
    btnStart.pack(side=TOP, fill=X, pady=4)

def makeFileOptionsView(frame):
    global fileOptionsFrame
    fileOptionsFrame = ttk.Frame(frame)
    fileOptionsFrame.pack(side=TOP, fill=X, pady=4)

    btnDel = Button(fileOptionsFrame, text=DELETE, command=lambda: textWidget.delete("0.0", END))
    btnDel.pack(side=LEFT)

    btnOpen = Button(fileOptionsFrame, text=OPEN_FILE, command=open_file(textWidget, isShowingTextChangesVar))
    btnOpen.pack(side=LEFT)
    
    btnSave = Button(fileOptionsFrame, text=SAVE_AS, command=save_file)
    btnSave.pack(side=LEFT)

    # btnPreproc = Button(fileOptionsFrame, text=PREPROCESS, command=preproc(textWidget, isShowingTextChangesVar))
    # btnPreproc.pack(side=LEFT)

def makeFolderOptionsView(frame):
    global folderOptionsFrame
    folderOptionsFrame = ttk.Frame(frame)
    folderOptionsFrame.pack(side=TOP, fill=X, pady=4)

    btnOpenFolder = Button(folderOptionsFrame, text=OPEN_FOLDER, command=open_folder)
    btnOpenFolder.pack(side=LEFT)

def makeOptionWidget(frame, description, options, callback=None) -> (Frame, StringVar):
    frame = ttk.Frame(frame)
    frame.pack(side=TOP, fill=X, pady=4)

    label = Label(frame, text=description)
    label.pack(side=LEFT)

    variable = StringVar()
    variable.set(options[0]) # default value

    widget = OptionMenu(frame, variable, *options, command=callback)
    widget.place(x=150, y=0)

    return (frame, variable)

def makeTextInputWidget(frame, description):
    frame = ttk.Frame(frame)
    frame.pack(side=TOP, fill=X, pady=4)

    label = Label(frame, text=description)
    label.pack(side=LEFT)

    input = Entry(frame, width=10)
    input.place(x=150,y=0)

    return frame, input

def makeCheckWidget(frame, text, defaultValue=False, callback=None) -> (BooleanVar, Checkbutton):
    frame = ttk.Frame(frame)
    frame.pack(side=TOP, fill=X, pady=4)
    
    var = BooleanVar()
    var.set(defaultValue)

    widget = Checkbutton(frame, text=text, var=var, command=callback)
    widget.pack(side=LEFT)
    
    return (var, widget)

def makeCommonOptionsView(frame):
    global commonOptionsFrame
    commonOptionsFrame = ttk.Frame(frame)
    commonOptionsFrame.pack(side=TOP, fill=X, pady=4)

    global isShowingTextChangesVar
    global isShowingTextChangesWidget
    isShowingTextChangesVar, isShowingTextChangesWidget = makeCheckWidget(commonOptionsFrame, text=SHOW_TEXT_CHANGES, defaultValue=False, callback=isShowingTextChangesCallback)
    configureShowingTextChanges(False)

    global workModeWidget
    global workModeVar
    workModeWidget, workModeVar = makeOptionWidget(commonOptionsFrame, description=WORK_MODE, options=WORK_MODE_OPTIONS, callback=workModeCallback)


    # Strategy configuration
    global strategyWidget
    global strategyVar
    global globalOptionsWidget
    global globalOptionsVar
    global localOptionsWidget
    global localOptionsVar
    
    strategyWidget, strategyVar = makeOptionWidget(commonOptionsFrame, description=STRATEGY, options=STRATEGY_OPTIONS, callback=strategyWidgetCallback)

    globalOptionsWidget, globalOptionsVar = makeOptionWidget(commonOptionsFrame, description=RANDOMISATION_TYPE, options=GLOBAL_OPTIONS)

    localOptionsWidget, localOptionsVar = makeOptionWidget(commonOptionsFrame, description=RANDOMISATION_TYPE, options=LOCAL_OPTIONS)
    localOptionsWidget.pack_forget()

    # Shuffling configuration
    global numberOfShufflesWidget, numberOfShufflesWidgetInput
    global windowWidget, windowWidgetInput
    global stepWidget, stepWidgetInput
    numberOfShufflesWidget, numberOfShufflesWidgetInput = makeTextInputWidget(commonOptionsFrame, description=NUMBER_OF_SHUFFLES)
    windowWidget, windowWidgetInput = makeTextInputWidget(commonOptionsFrame, description=WINDOW)
    stepWidget, stepWidgetInput = makeTextInputWidget(commonOptionsFrame, description=STEP)
    
    windowWidget.pack_forget()
    stepWidget.pack_forget()

def isShowingTextChangesCallback():
    configureShowingTextChanges(isShowingTextChangesVar.get())


def configureShowingTextChanges(isShowingTextChanges):
    if isShowingTextChanges:
        # Have no idea how to pack to the very left, so removing controls frame and packing it back
        # TODO: Find out how to pack text frame to the very left
        controlsFrame.pack_forget()
        textFrame.pack(side=LEFT, fill=Y, padx=10, pady=10)
        controlsFrame.pack(side=LEFT, fill=BOTH, padx=10, pady=10, expand=True)

        # if text is shown, make window big
        window.minsize(EXPANDED_WINDOW_SIZE[0], EXPANDED_WINDOW_SIZE[1])
        window.maxsize(EXPANDED_WINDOW_SIZE[0], EXPANDED_WINDOW_SIZE[1])
    else:
        textFrame.pack_forget()
        
        # if no text is shown, make window smaller
        window.minsize(COLLAPSED_WINDOW_SIZE[0], COLLAPSED_WINDOW_SIZE[1])
        window.maxsize(COLLAPSED_WINDOW_SIZE[0], COLLAPSED_WINDOW_SIZE[1])

def workModeCallback(selection):
    if selection == FILE:
        folderOptionsFrame.pack_forget()
        fileOptionsFrame.pack(after=commonOptionsFrame, side=TOP, fill=X, pady=4)
    else:
        fileOptionsFrame.pack_forget()
        folderOptionsFrame.pack(after=commonOptionsFrame, side=TOP, fill=X, pady=4)


def strategyWidgetCallback(selection):
    if selection == GLOBAL:
        localOptionsWidget.pack_forget()
        globalOptionsWidget.pack(after=strategyWidget, side=TOP, fill=X, pady=4)

        windowWidget.pack_forget()
        stepWidget.pack_forget()
    else:
        globalOptionsWidget.pack_forget()
        localOptionsWidget.pack(after=strategyWidget, side=TOP, fill=X, pady=4)
        windowWidget.pack(after=numberOfShufflesWidget, side=TOP, fill=X, pady=4)
        stepWidget.pack(after=windowWidget, side=TOP, fill=X, pady=4)

def makeTimeWidget(frame):
    global timeWidget
    timeWidget = Label(frame, text="Time: 0:00")
    timeWidget.pack(side=TOP)

def makeCompletedFilesWidget(frame):
    global completedFilesWidget
    completedFilesWidget = Label(frame, text="")
    completedFilesWidget.pack(side=TOP)


def makeControlsView():
    global controlsFrame
    controlsFrame = Frame(window)
    controlsFrame.pack(side=LEFT, fill=BOTH, padx=10, pady=10, expand=True)

    makeCommonOptionsView(controlsFrame)
    makeFileOptionsView(controlsFrame)
    
    makeFolderOptionsView(controlsFrame)
    folderOptionsFrame.pack_forget()

    makeTimeWidget(controlsFrame)
    makeCompletedFilesWidget(controlsFrame)
    makeButtonStart(controlsFrame)

makeTextView()
makeControlsView()
