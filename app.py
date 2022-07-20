from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from keras.models import load_model
from PIL import Image #use PIL
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def init():
    if request.method == 'POST':
        file = request.files['file']
        print("File Received")
        filename = secure_filename(file.filename)
        print(filename)
        dict = ['NORMAL','PNEUMONIA']
        file.save("./static/"+filename) #Heroku no need static
        file = open("./static/"+filename,"r") #Heroku no need static
        model = load_model("Pneumonia")
        image = Image.open("./static/"+filename)#读取方式为RGB
        image = image.convert("RGB")                   # 图片转为RGB格式
        image = np.array(image)[:, :, ::-1]            # 将图片转为numpy格式，并将最后一维通道倒序
        image = Image.fromarray(np.uint8(image))       # 将numpy转换回PIL的Image对象 
        #转化为BGR格式
        image = np.asarray(image)
        image.resize((100,100,3),refcheck = False)
        image = np.asarray(image, dtype="float64") #need to transfer to np to reshape'
        image = image.reshape(1, image.shape[0], image.shape[1], image.shape[2]) #rgb to reshape to 1,100,100,3
        pred= dict[model.predict(image).argmax()]
        return(render_template("index.html", result=str(pred)))
    else:
        return(render_template("index.html", result="WAITING"))
if __name__ == "__main__":
    app.run()
