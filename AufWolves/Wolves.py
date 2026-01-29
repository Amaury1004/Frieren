import os 
import random

class Wolf: 
    def random_AufWolves(self):
        auf_Folders = "AufWolves/ImageSet"
        files = os.listdir(auf_Folders)
        image = [file for file in files if file.endswith('.png')]
        return os.path.join(auf_Folders, random.choice(image))
    