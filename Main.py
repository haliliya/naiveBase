from Feature import Feature
from Classifier import Classifier
import pandas as pd

# TODO check if file exists and format is valid
def read_structure_file(path):
    file = open(path + "\\Structure.txt", "r")
    for line in file:
        description = (line.replace("@ATTRIBUTE ", "").replace("\n", "")).split(" ", 1)
        create_feature(description)

def create_feature(feature_description):
    feature_name = feature_description[0]
    if "{" in feature_description[1] and "}" in feature_description[1]:
        feature_type = "CATEGORIAL"
    else:
        feature_type = "NUMERIC"
    feature_possible_values = (feature_description[1].replace("{", "").replace("}", "")).split(",")
    feature = Feature(feature_name, feature_type, feature_possible_values)
    features_list.append(feature)

# TODO check if file exists and format is valid
def read_csv(path):
    df = pd.read_csv(path)
    return df






features_list = []
read_structure_file("C:\\Users\\yardenhalili\\PycharmProjects\\naiveBayes")
train_set = read_csv("C:\\Users\\yardenhalili\\PycharmProjects\\naiveBayes\\train.csv")
# TODO send num of bins as parameter, check if valid
num_of_bins = 2
classifier = Classifier(features_list, train_set)
classifier.pre_process_data(num_of_bins)
test_set = read_csv("C:\\Users\\yardenhalili\\PycharmProjects\\naiveBayes\\test.csv")
classifier.classify(test_set)

