import pandas as pd

class Classifier:
  def __init__(self, model_structure, train_set):
    self.model_structure = model_structure
    self.train_set = train_set

  def pre_process_data(self, num_of_bins):
      self.missing_values = dict()
      self.discretiztion_params = dict()
      for feature in self.model_structure[:-1]:
          self.missing_values[feature.name] = self.fill_missing_values(feature)
          if feature.type == "NUMERIC":
            self.discretiztion_params[feature.name] = self.perform_discretization(feature, num_of_bins)


  def fill_missing_values(self, feature):
      if feature.type == "CATEGORIAL":
          self.train_set[feature.name].fillna((self.train_set[feature.name]).mode()[0], inplace=True)
          return self.train_set[feature.name].mode()[0]
      elif feature.type == "NUMERIC":
          self.train_set[feature.name].fillna(self.train_set[feature.name].mean(), inplace=True)
          return self.train_set[feature.name].mean()


  def perform_discretization(self, feature, num_of_bins):
     min_val = self.train_set[feature.name].min()
     max_val = self.train_set[feature.name].max()
     interval_width =  (max_val - min_val) / num_of_bins
     cut_points = []
     for i in range(1,num_of_bins):
         cut_points.append(min_val + i * interval_width)
     labels = range(len(cut_points) + 1)
     break_points = [min_val] + cut_points + [max_val]
     '''
     print(feature.name)
     print(min_val)
     print(max_val)
     print(interval_width)
     print(cut_points)
     print(break_points)
     print(labels)
     '''

     # discretization of feature possible values TODO check if neccessary
     index = self.model_structure.index(feature)
     self.model_structure[index].possible_values = labels
     self.train_set[feature.name] = pd.cut(self.train_set[feature.name], bins = break_points, labels = labels, include_lowest=True)
     return [break_points] + [labels]


  def classify(self, test_set, path):
      for feature in self.model_structure[:-1]:
          test_set[feature.name].fillna((self.missing_values[feature.name]), inplace=True)
          if feature.type == "NUMERIC":
            test_set[feature.name] = pd.cut(test_set[feature.name], bins=self.discretiztion_params[feature.name][0], labels=self.discretiztion_params[feature.name][1], include_lowest=True)
      file = open(path, "w")
      for i in range(len(test_set)):
          record = test_set.iloc[i]
          record_class = self.classify_record(record)
          file.write((str)(i+1) + " " + record_class)
          if i < len(test_set) - 1:
              file.write("\n")
      file.close()


  def classify_record(self, record):
      index = len(self.model_structure) - 1
      classes = self.model_structure[index].possible_values
      features_list = self.model_structure
      probabilities_dict = dict()
      for optional_class in classes:
          i = 0
          probability = 1
          prob_class = (float)(pd.value_counts(self.train_set['class'])[optional_class])/(float)(len(self.train_set))
          for column in record[:-1]:
              feature = features_list[i]
              feature_value = column
              probability *= self.calculate_probability(feature, feature_value, optional_class)
              i += 1
          probabilities_dict[optional_class] = probability * prob_class
      return max(probabilities_dict, key=probabilities_dict.get)

  def calculate_probability(self, feature, feature_value, optional_class):
      m = 2
      n = pd.value_counts(self.train_set['class'])[optional_class]
      index = self.model_structure.index(feature)
      M = (float)(len(self.model_structure[index].possible_values))
      p = 1.0/M
      n_class =  len((self.train_set.loc[(self.train_set[feature.name] == feature_value) & (self.train_set['class'] == optional_class)]))
      m_estimate = (n_class + m * p)/(n + m)
      '''
      print (optional_class)
      print (feature.name)
      print (feature_value)
      print (n)
      print (M)
      print (p)
      print (n_class)
      print (m_estimate)
      print ("\n")
      '''

      return m_estimate
