
# The following class represents a feature
class Feature:
  def __init__(self, name, type, possible_values):
    self.name = name
    # NUMERIC or CATEGORICAL variable
    self.type = type
    self.possible_values = possible_values