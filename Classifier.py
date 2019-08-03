import pandas as pd

class Classifier:
  def __init__(self, model_structure, train_set):
    self.model_structure = model_structure
    self.train_set = train_set

  def pre_process_data(self, num_of_bins):
      for feature in self.model_structure[:-1]:
          self.fill_missing_values(feature)
          if feature.type == "NUMERIC":
            self.perform_discretization(feature, num_of_bins)

  def fill_missing_values(self, feature):
      if feature.type == "CATEGORIAL":
          self.train_set[feature.name].fillna((self.train_set[feature.name]).mode()[0], inplace=True)
      elif feature.type == "NUMERIC":
          self.train_set[feature.name].fillna(self.train_set[feature.name].mean(), inplace=True)


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





  def classify(self, test_set):
      ''' TODO complete function'''
