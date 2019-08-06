from Feature import Feature
from Classifier import Classifier
import pandas as pd
from Tkinter import *
import tkFileDialog
import tkMessageBox
import os

# The following function reads structure.txt file in the specified path
def read_structure_file(path):
    file = open(path.get() + "\\Structure.txt", "r")
    for line in file:
        description = (line.replace("@ATTRIBUTE ", "").replace("\n", "")).split(" ", 1)
        create_feature(description)

# The following function creates a new feature based on feature_description
def create_feature(feature_description):
    feature_name = feature_description[0]
    if "{" in feature_description[1] and "}" in feature_description[1]:
        feature_type = "CATEGORICAL"
    else:
        feature_type = "NUMERIC"
    feature_possible_values = (feature_description[1].replace("{", "").replace("}", "")).split(",")
    feature = Feature(feature_name, feature_type, feature_possible_values)
    # append feature to features_list
    features_list.append(feature)

# The following function reads a csv file in the specified path
def read_csv(path):
    try:
        df = pd.read_csv(path)
    except:
        df = pd.DataFrame()
    return df

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    folderName = tkFileDialog.askdirectory()
    folder_path.set(folderName)
    validateFolderPath()

def validateBeforeBuild(*args):
    validFolder = validateFolderPath()
    validBins = validateBins()
    if (validFolder & validBins):
        build_button.config(state="normal")
    else:
        build_button.config(state="disabled")

def validateBins():
    # check validation of bins
    isValid =True
    if (not discretization_bins_entry.get()):
        tkMessageBox.showerror("Naive Bayes Classifier", "Please enter number of bins")
        isValid = False
    try:
        if (int(discretization_bins_entry.get()) <= 0):
            tkMessageBox.showerror("Naive Bayes Classifier", "Please enter number of bins greater than 0")
            isValid = False
    except:
        tkMessageBox.showerror("Naive Bayes Classifier", "Please enter an integer number")
        isValid = False

    return isValid

def validateFolderPath():
    # check validation of chosen folder path
    isValid = True
    if (not os.path.isdir(folder_path.get())):
        tkMessageBox.showerror("Naive Bayes Classifier", "You should choose a folder path")
        isValid = False

    # validate files in folder path
    global trainFile, testFile
    structureFile = folder_path.get() + "\\Structure.txt"
    trainFile = folder_path.get() + "\\train.csv"
    testFile = folder_path.get() + "\\test.csv"

    # Structure.txt file
    if (not os.path.exists(structureFile)):
        tkMessageBox.showerror("Naive Bayes Classifier", "'Structure.txt' file does not exist in the chosen folder")
        isValid = False
    else:
        if (os.stat(structureFile).st_size == 0):
            tkMessageBox.showerror("Naive Bayes Classifier", "'Structure.txt' file is empty")
            isValid = False

    # train.csv file
    if (not os.path.exists(trainFile)):
        tkMessageBox.showerror("Naive Bayes Classifier", "'train.csv' file does not exist in the chosen folder")
        isValid = False

    # test.csv file
    if (not os.path.exists(testFile)):
        tkMessageBox.showerror("Naive Bayes Classifier", "'test.csv' file does not exist in the chosen folder")
        isValid = False

    return isValid

def build():
    read_structure_file(folder_path)
    global train_set
    train_set = read_csv(trainFile)
    if (train_set.empty):
        tkMessageBox.showerror("Naive Bayes Classifier", "'train.csv' file is empty")
        return

    global classifier
    classifier = Classifier(features_list, train_set)
    numOfBins = (int)(discretization_bins_entry.get())
    classifier.pre_process_data(numOfBins)
    tkMessageBox.showinfo("Naive Bayes Classifier", "Building classifier using train-set is done!")

def classify():
    global test_set
    test_set = read_csv(testFile)
    if (test_set.empty):
        tkMessageBox.showerror("Naive Bayes Classifier", "'test.csv' file is empty")
        return

    classifier.classify(test_set, folder_path.get() + "/output.txt")
    tkMessageBox.showinfo("Naive Bayes Classifier","Classifying test-set is done! You can find the results in the folder you chose")
    root.destroy()

features_list = []
'''
read_structure_file("C:\\Users\\yardenhalili\\PycharmProjects\\naiveBayes")
train_set = read_csv("C:\\Users\\yardenhalili\\PycharmProjects\\naiveBayes\\train.csv")
# TODO send num of bins as parameter, check if valid
num_of_bins = 3
classifier = Classifier(features_list, train_set)
classifier.pre_process_data(num_of_bins)
test_set = read_csv("C:\\Users\\yardenhalili\\PycharmProjects\\naiveBayes\\test.csv")
classifier.classify(test_set, "C:\\Users\\yardenhalili\\PycharmProjects\\naiveBayes\\output.txt")
'''

root = Tk()
root.title("Naive Bayes Classifier")
'''
directory_path_label = Label(root, text="Directory Path")
directory_path_label.grid(row=0, column=0, sticky=W)
'''

build_button = Button(text="Build", command=build, state="disabled")
build_button.grid(row=5, column=1, padx=5, pady=5)

folder_path = StringVar()
bins = StringVar()

directory_path_label = Label(root, text="Directory Path:")
discretization_bins_label = Label(root, text="Discretization Bins:")

directory_path_entry = Entry(root, textvariable=folder_path)
discretization_bins_entry = Entry(root, textvariable=bins)
bins.trace("w",validateBeforeBuild)

directory_path_entry.grid(row=0, column=1, sticky=W, padx=5, pady=5)
discretization_bins_entry.grid(row=1, column=1, sticky=W, padx=5, pady=5)

directory_path_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
discretization_bins_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)

browse_button = Button(text="Browse", command=browse_button)
browse_button.grid(row=0, column=8, padx=5, pady=5)

classify_button = Button(text="Classify", command=classify)
classify_button.grid(row=10,column=1, padx=5, pady=5)

root.geometry("350x150")
root.resizable(width=True, height=True)
root.mainloop()