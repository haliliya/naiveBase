from Feature import Feature
from Classifier import Classifier
import pandas as pd
from Tkinter import *
import tkFileDialog

# TODO check if file exists and format is valid
# The following function reads structure.txt file in the specified path
def read_structure_file(path):
    file = open(path + "\\Structure.txt", "r")
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

# TODO check if file exists and format is valid
# The following function reads a csv file in the specified path
def read_csv(path):
    df = pd.read_csv(path)
    return df

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = tkFileDialog.askdirectory()
    folder_path.set(filename)

def build():
    print "build"
    '''TODO complete function'''

def classify():
    '''TODO complete function'''
    print "classify"

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
root.title("naive bayes classifier")
'''
directory_path_label = Label(root, text="Directory Path")
directory_path_label.grid(row=0, column=0, sticky=W)
'''
folder_path = StringVar()

directory_path_label = Label(root, text="Directory Path:")
discretization_bins_label = Label(root, text="Discretization Bins:")

directory_path_entry = Entry(root, textvariable=folder_path)
discretization_bins_entry = Entry(root)

directory_path_entry.grid(row=0, column=1, sticky=W)
discretization_bins_entry.grid(row=1, column=1, sticky=W)

directory_path_label.grid(row=0, column=0, sticky=W)
discretization_bins_label.grid(row=1, column=0, sticky=W)

browse_button = Button(text="Browse", command=browse_button)
browse_button.grid(row=0, column=3)

build_button = Button(text="Build", command=build)
build_button.grid(row=5, column=1)

classify_button = Button(text="Classify", command=classify)
classify_button.grid(row=10,column=1)

root.mainloop()