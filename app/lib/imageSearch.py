import numpy as np 
import os
from keras.preprocessing import image 
from keras import utils 
import pickle 
# from tensorflow.keras.preprocessing import image 
from keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
from sklearn.neighbors import NearestNeighbors
import urllib.parse

 
class imageSearch(object):
    def __init__(self,filenames,features):   
        if filenames == "" or features == "":
            raise ValueError("The parameter for filenames || features cannot be empty.") 
        img_size = 224
        self.filenames =  filenames
        self.features  =  features
        self.img_size  =  img_size 
        # ถ้า Runใน Docker เปลี่ยนเป็น "model/" +
        # ถ้า Runใน FastAPI เปลี่ยนเป็น "app/model/" +
        prefix = "app/model/"
        self.model          = load_model(prefix + 'ResNet50.h5')
        self.filenames_load = pickle.load(open(prefix + filenames + ".pickle", 'rb'))
        self.feature_loadd  = pickle.load(open(prefix + features + ".pickle", 'rb')) 
        self.neighbors = NearestNeighbors(n_neighbors=4,
                                    algorithm='ball_tree',
                                    metric='euclidean')

    def urlToImg(self,filename="file01" , mainUrl= None):  
        img_width, img_height = self.img_size, self.img_size 
        imageUrl = utils.get_file(str(filename),origin=mainUrl)  
        mainImg  = image.load_img(imageUrl, target_size=(img_width, img_height))     
        img_array           = image.img_to_array(mainImg)
        expanded_img_array  = np.expand_dims(img_array, axis=0)
        preprocessed_img    = preprocess_input(expanded_img_array) 
        os.remove(imageUrl) # Remove the cached file 
        return preprocessed_img

    def find_similar_images(self,indices):
        plotnumber = 1    
        data = []
        for index in indices:
            if plotnumber<=len(indices) :
                public_url = self.filenames_load[index]
                url = urllib.parse.unquote(public_url)  
                text_split = url.split('/') 
                rs = {'name': text_split[2], 'category': text_split[1], 'folder': text_split[0]}, 
                data.append(rs[0])
        return data

    def main(self,mainUrl):
        # mainUrl                = "https://storage.googleapis.com/chatbot-ecommerce/umber_shop/snap1.png" 
        preprocessed_img       = self.urlToImg('img1',mainUrl)  
        model                  = self.model
        neighbors              = self.neighbors.fit(self.feature_loadd)  
        test_img_features      = model.predict(preprocessed_img, batch_size=1)  
        distances,indices      = neighbors.kneighbors(test_img_features)  
        result                 = self.find_similar_images(indices[0])
        return result 
