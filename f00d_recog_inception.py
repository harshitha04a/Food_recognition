import streamlit as ss


import numpy as np #standard
import plotly.express as px  #plots and graphing lib
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image

import tensorflow
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import SGD,Adam
from tensorflow.keras.layers import Dense,Input,Flatten
from tensorflow.keras.applications.inception_v3 import InceptionV3,preprocess_input,decode_predictions
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

        
ss.markdown(
     """
     <style>
     .ssApp {
         background: url("f1.jpg");
         background-size: cover;
     }
     </style>
     """,
     unsafe_allow_html=True
 )


def dic_maker(arr):
  """ dis takes in arr [[prob(1),prob(2),prob(3)......prob(n)]]
   and outputs [(1,prob(1)),(2,prob(2))]
   (basically some formatting to make life easier)"""
  dict_ = {}
  for ind in range(len(arr[0])):
    dict_[ind] = arr[0][ind]
  return sorted(dict_.items(), key=lambda x: x[1],reverse=True)[:3]


def dic_maker_tuple(tuple_arr):
  """ takes in [(x,y),(a,b)]
      outputs {x:y,a:b} (basically some formatting to make life easier)
  """
  dict_ = {}
  for tuple_ in tuple_arr:
    dict_[target_dict[tuple_[0]]] = tuple_[1]
  return dict_


def inception_no_gen(image):
  """ 
  prediction happens in this function
  super important, takes in image_path (/content/test_1/test/111.jpg)
  outputs: {1:prob(1),2:prob(2)}
  """
  #image_1 = tensorflow.keras.preprocessing.image.load_img(image_path)


  input_arr = tensorflow.keras.preprocessing.image.img_to_array(image)
  input_arr = preprocess_input(input_arr)
  input_arr = tensorflow.image.resize(input_arr,size = (256,256))
  input_arr = np.array([input_arr])  # Convert single image to a batch.
  predictions = model_saved.predict(input_arr)
  return dic_maker_tuple(dic_maker(predictions))


def plot_pred_final(test_imgs):
  """
  dis takes in {1:prob(1),2:prob(2)}
  and plots a SUPER NORMIE PLOT to make it easier for SRM FACULTY(or they might flip out like the bunch of idiots they are)
  """
  #test_imgs = glob(image_path_custom + '/*/*.jpeg')
  fig = make_subplots(rows = 2, cols = 2)
  pred_list = inception_no_gen(test_imgs)
  fig.append_trace(go.Image(z = np.array(test_imgs)),1,1)
  fig.append_trace(go.Bar(y = list(pred_list.keys()), x = list(pred_list.values()),orientation = 'h'),1,2)
  fig.update_layout(width = 1750, height = 800,title_text = "Custom Predictions",showlegend = False)
  return fig

#------streamlit starts here----------------

model_saved = tensorflow.keras.models.load_model("inception_food_rec_50epochs.h5")
target_dict = {0:"Bread",1:"Dairy_product",2:"Dessert",3:"Egg",4:"Fried_food",
                 5:"Meat",6:"Noodles/Pasta",7:"Rice",8:"Seafood",9:"Soup",10:"veggies/Fruit"}

#ss.set_page_config(page_title = "Am I eating well??🤔", layout = "wide")
htm_temp="""
    <h1 style ="text-align:center;"color:#048c7f;">Am I eating well??🤔</h1>
    </div>
    """
ss.markdown(htm_temp,unsafe_allow_html=True)
htm_temp1="""
    <h3 style ="color:#AFB83B;">Every one likes food🥞! \nYou are what you eat,so don't be fast ,cheap, easy, or fake.🤔</h3>
    </div>
    """
ss.markdown(htm_temp1,unsafe_allow_html=True)
htm_temp2="""
    <h3 style ="color:#AFB83B;">If you keep good food in your fridge ,you will eat good food.</h3>
    </div>
    """
ss.markdown(htm_temp2,unsafe_allow_html=True)
htm_temp3="""
    <h3 style="color:#AFB83B;">So lets drive into what you eat...🧐🧐</h3>
    </div>
    """
ss.markdown(htm_temp3,unsafe_allow_html=True)


#ss.markdown('Dataset is obtained from [kaggle](https://www.kaggle.com/trolukovich/food11-image-dataset)')


ss.markdown('### Food Recognition step 😄- Upload Image')
image_path = ss.file_uploader("drop the image file here: ", type = ["jpg"])

if image_path:
  image = Image.open(image_path)
  preds = plot_pred_final(image)
  ss.plotly_chart(preds)
  




