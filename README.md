# X-Ray pneumonia detection

## Used libraries
#### Libraries

- falcon
- TensorFlow
- Keras
- NumPy
- JQuery

## Preparation for launch
### Install Python libraries

```
pip install falcon
pip install keras
pip install tensorflow
pip install numpy
```
### Dataset
I take x-ray images from this site:
https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia

And I added some random pictures from the phone’s cache to make dataset for sorting X-ray images from another “garbage”.

## Launch
The server starts in the server.py file with
```
python3 server.py
```
After message
```
Serving on 127.0.0.1:8000
```
The server is running at http://127.0.0.1:8000/
