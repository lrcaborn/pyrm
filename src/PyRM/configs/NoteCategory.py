from enum import Enum

class NoteCategory(Enum):
  CRASH = "Cymbal Crashes"
  HAT = "Hi-Hat"
  KICK = "Kick"
  RIDE = "Ride cymbal"
  SNARE = "Snare"
  TOM = "Toms"
  FX = "FX"
  
  # piano sections
  LOW = "Low"
  MIDDLE = "Middle"
  HIGH = "High"
  
  # keys
  AHARMONICMINOR = "AHARMONICMINOR"
  JAPANESE = "JAPANESE"
  
  def __str__(self):
    return self.name
