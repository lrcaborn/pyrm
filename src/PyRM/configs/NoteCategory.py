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
    ACOUSTIC = "Acoustic"
    ALGERIAN = "Algerian"
    ALGERIAN_2 = "Algerian2"
    AEOLIAN_DOMINANT = "Aeolian Dominant"
    AUGMENTED = "Augmented"
    BALINESE = "Balinese"
    BYZANTINE = "Byzantine"
    CHINESE = "Chinese"
    CHROMATIC = "Chromatic"
    DIMINISHED = "Diminished"
    DOMINANT_DIMINISHED = "Dominant Diminished"
    EGYPTIAN = "Egyptian"
    EIGHT_TONE_SPANISH = "Eight Tone Spanish"
    HAWAIIAN = "Hawaiian"
    HARMONIC_MINOR = "Harmonic Minor"
    HIRAJŌSHI = "Hirajōshi"
    HUNGARIAN = "Hungarian"
    HUNGARIAN_MAJOR = "Hungarian major"
    IBERIAN = "Iberian"
    IWATO = "Iwato"
    JAPANESE = "Japanese"
    NEOPOLITAN_MAJOR = "Neopolitan Major"
    NEOPOLITAN_MINOR = "Neopolitan Minor"
    ORIENTAL = "Oriental"
    PHRYGIAN_DOMINANT = "Phrygian Dominant"
    PROMETHEUS = "Prometheus"
    ROMANIAN_MINOR = "Romanian Minor"
    SUPER_LOCRIAN = "Super Locrian"
    WHOLE_TONE = "Whole Tone"
    YO = "Yo"

    def __str__(self):
        return self.name
