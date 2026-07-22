"""
NEURA-1 Model Loader

Connects NEURA-1 with external AI inference providers.
"""

import os

from core.config import Config
from core.inference_api import InferenceAPI

class ModelLoader:
"""
Loads and manages the AI model connection.
"""

def __init__(self, model_name=None):  

    self.config = Config()  

    self.model_name = (  
        model_name  
        or self.config.model_name  
    )  

    self.model = None  

    self.inference = InferenceAPI()  


def load(self):  
    """  
    Initialize external inference connection.  
    """  

    print(  
        f"Connecting model: {self.model_name}"  
    )  

    self.model = self.inference  

    return self.model  


def generate(self, prompt):  
    """  
    Generate AI response.  
    """  

    if self.model is None:  
        self.load()  

    return self.model.generate(prompt)  


def get_status(self):  
    """  
    Return model status.  
    """  

    return {  
        "model": self.model_name,  
        "loaded": self.model is not None,  
        "provider": "Hugging Face Inference API"  
    }

if name == "main":

loader = ModelLoader()  

loader.load()  

print(  
    loader.get_status()  
) 