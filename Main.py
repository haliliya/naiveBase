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
num_of_bins = 3
classifier = Classifier(features_list, train_set)
classifier.pre_process_data(num_of_bins)
test_set = read_csv("C:\\Users\\yardenhalili\\PycharmProjects\\naiveBayes\\test.csv")
'''
for feature in features_list[:-1]:
    if feature.type == "NUMERIC":
        min_val = train_set[feature.name].min()
        max_val = train_set[feature.name].max()
        interval_width = (max_val - min_val) / num_of_bins
        cut_points = []
        for i in range(1, num_of_bins):
            cut_points.append(min_val + i * interval_width)
        labels = range(len(cut_points) + 1)
        break_points = [min_val] + cut_points + [max_val]
        test_set = pd.cut(train_set[feature.name], bins = break_points, labels = labels, include_lowest=True)
'''

classifier.classify(test_set, "C:\\Users\\yardenhalili\\PycharmProjects\\naiveBayes\\output.txt")
