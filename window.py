from tkinter import *

from buttons import RoundedButton
from PIL import ImageTk, Image

# from tensorflow.keras.models import model_from_json
from tensorflow.keras.models import load_model
import numpy as np
import re 
import nltk
from nltk.corpus import stopwords

from nltk.stem import PorterStemmer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import one_hot

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')

# model loading
vocabSize = 11000
max_len = 300


# with open(r"D:\AISciD(S6)\Deep_Learning\Project\interface\model_saved.json", 'r') as json_file:
#     loaded_model_json = json_file.read()
    
# loaded_model = model_from_json(loaded_model_json)
# loaded_model.load_weights(r"D:\AISciD(S6)\Deep_Learning\Project\interface\model_saved.h5")

model_hamza = load_model(r'D:\AISciD(S6)\Deep_Learning\Project\interface\model_hamza.h5')

# sentence cleaning
def sentence_cleaning(sentence):
    """Pre-processing sentence for prediction"""
    global stopwords
    stemmer = PorterStemmer()
    corpus = []
    text = re.sub("[^a-zA-Z]", " ", sentence)
    text = text.lower()
    text = text.split()
    text = [stemmer.stem(word) for word in text if word not in stopwords]
    text = " ".join(text)
    corpus.append(text)
    one_hot_word = [one_hot(input_text=word, n=11000) for word in corpus]
    pad = pad_sequences(sequences=one_hot_word,maxlen=300,padding='pre')
    return pad

# dictionary of the emotions
emotions_dict = {0:'Anger', 1:'Fear', 2:'Joy', 3:'Love', 4:'Sadness', 5:'Surprise'}

window = Tk()
window.title("Emotion detetctor")
window.geometry('600x500')
window.resizable(1,1)


label = Label(window, text="Welcome to emotion detector", font=("Arial Bold", 16))
label.pack(side=TOP, pady=30)



img = ImageTk.PhotoImage(Image.open(r"D:\AISciD(S6)\Deep_Learning\Project\interface\button.png"))
feel = None
textfield = Text(window, width=40, font=('Arial', 12), bd=2, relief='groove', height=2)
textfield.pack(side=TOP, pady=10)
lb = Label(window, image=None, height=240)
lb_text = Label(window, text=None, font=("Arial Bold", 16))


def on_submit():
    text = textfield.get("1.0", "end-1c")
    text = sentence_cleaning(text)
    result = model_hamza.predict(text)
    emotion_result = int(np.argmax(result))
    proba =  np.max(result) * 100
    
    global lb
    global lb_text
    lb_text.destroy()
    feeling = ''
    if emotion_result == 0:
        feeling = 'angry'
        lb.destroy()
    elif emotion_result == 1:
        feeling = 'feared'
        lb.destroy()
    elif emotion_result == 2:
        feeling = 'happy'
        lb.destroy()
    elif emotion_result == 3:
        feeling = 'lover'
        lb.destroy()
    elif emotion_result == 4:
        feeling = 'sad'
        lb.destroy()
    elif emotion_result == 5:
        feeling = 'surprised'
        lb.destroy()

    gif_path = (f"D:\AISciD(S6)\Deep_Learning\Project\interface\{feeling}.gif")
    print(f"file path = {gif_path}")
    
    image = Image.open(gif_path)
    # Resize the image
    image = image.resize((150, 150))
    # Create a PhotoImage object from the image
    photo = ImageTk.PhotoImage(image,  format="gif -index 2")
    lb = Label(window, image=photo, height=240)
    lb.image = photo
    lb.pack()
    lb_text = Label(window, text=f'You are : {proba:.2f}% {feeling}', font=("Arial Bold", 16))
    lb_text.pack(pady=10)
    textfield.delete("1.0", "end-1c")


button = Button(window, command = on_submit, image = img, border=0)
button.pack()





window.mainloop()

