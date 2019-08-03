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
    ''' TODO complete function'''


  def classify(self, test_set):
      ''' TODO complete function'''
