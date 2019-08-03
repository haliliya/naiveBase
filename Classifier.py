import pandas as pd

# The following class represents naive bayes classifier
class Classifier:

    # Classifier Constructor
    def __init__(self, model_structure, train_set):
        # a list of features (feature is defined by: name, type and possible values)
        self.model_structure = model_structure
        # train-set data frame representation
        self.train_set = train_set
        self.missing_values = dict()
        self.discretiztion_params = dict()

    # The following function preforms pre-processing of the data
    def pre_process_data(self, num_of_bins):
        # iterate model features
        for feature in self.model_structure[:-1]:
            # fill missing values
            self.missing_values[feature.name] = self.fill_missing_values(feature)
            if feature.type == "NUMERIC":
                # perform discretization on NUMERIC variables
                self.discretiztion_params[feature.name] = self.perform_discretization(feature, num_of_bins)

    # The following function fills missing data: CATEGORICAL variables - by mode, NUMERIC variables - by mean
    def fill_missing_values(self, feature):
        if feature.type == "CATEGORICAL":
            # fill missing values by mode
            self.train_set[feature.name].fillna((self.train_set[feature.name]).mode()[0], inplace=True)
            return self.train_set[feature.name].mode()[0]
        elif feature.type == "NUMERIC":
            # fill missing data by mean
            self.train_set[feature.name].fillna(self.train_set[feature.name].mean(), inplace=True)
            return self.train_set[feature.name].mean()

    # The following function performs discretization by equal-width partitioning
    def perform_discretization(self, feature, num_of_bins):
        min_val = self.train_set[feature.name].min()
        max_val = self.train_set[feature.name].max()
        interval_width =  (max_val - min_val) / num_of_bins
        cut_points = []
        for i in range(1,num_of_bins):
            cut_points.append(min_val + i * interval_width)
        labels = range(len(cut_points) + 1)
        break_points = [min_val] + cut_points + [max_val]
        # discretization of feature possible values
        index = self.model_structure.index(feature)
        self.model_structure[index].possible_values = labels
        self.train_set[feature.name] = pd.cut(self.train_set[feature.name], bins = break_points, labels = labels, include_lowest=True)
        return [break_points] + [labels]

    # The following function classifies test set records and writes output to path
    def classify(self, test_set, path):
        # pre-process data in test-set : fill missing values and perform discretization (similarly to train-set)
        for feature in self.model_structure[:-1]:
            test_set[feature.name].fillna((self.missing_values[feature.name]), inplace=True)
            if feature.type == "NUMERIC":
                test_set[feature.name] = pd.cut(test_set[feature.name], bins=self.discretiztion_params[feature.name][0], labels=self.discretiztion_params[feature.name][1], include_lowest=True)
        # create file in path
        file = open(path, "w")
        #iterate test-set
        for i in range(len(test_set)):
            record = test_set.iloc[i]
            # classify record
            record_class = self.classify_record(record)
            # write output to file
            file.write((str)(i+1) + " " + record_class)
            if i < len(test_set) - 1:
              file.write("\n")
        file.close()

    # The following function classifies a given record
    def classify_record(self, record):
        index = len(self.model_structure) - 1
        classes = self.model_structure[index].possible_values
        features_list = self.model_structure
        probabilities_dict = dict()
        # iterate optional classes
        for optional_class in classes:
            i = 0
            probability = 1
            # probability of an arbitrary record to belong to class
            prob_class = float(pd.value_counts(self.train_set['class'])[optional_class]) / float(len(self.train_set))
            # iterate record features
            for column in record[:-1]:
                feature = features_list[i]
                feature_value = column
                # calculate conditional probability
                probability *= self.calculate_probability(feature, feature_value, optional_class)
                i += 1
            probabilities_dict[optional_class] = probability * prob_class
        # return class with highest probability
        return max(probabilities_dict, key=probabilities_dict.get)

    # The following function calculates probability using m-estimate (m=2)
    def calculate_probability(self, feature, feature_value, optional_class):
        m = 2
        # number of records in train-set that belong to the optional_class
        records_in_class_num = pd.value_counts(self.train_set['class'])[optional_class]
        index = self.model_structure.index(feature)
        # number of possible feature values
        num_of_possible_values = (float)(len(self.model_structure[index].possible_values))
        value_probability = 1.0/num_of_possible_values
        # number of records in train-set that belong to the optional_class in which feature value equals feature_value
        value_in_class_num = len((self.train_set.loc[(self.train_set[feature.name] == feature_value) & (self.train_set['class'] == optional_class)]))
        # calculate probability using m_estimate formula
        m_estimate = (value_in_class_num + m * value_probability)/(records_in_class_num + m)
        return m_estimate
