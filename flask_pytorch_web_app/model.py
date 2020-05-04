import io
from os import getcwd
import json
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image


def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def predict(image_file, class_file):
    class_file = getcwd() + '/flask_pytorch_web_app/' + class_file
    # Make sure to pass `pretrained` as `True` to use the pretrained weights:
    model = models.densenet121(pretrained=True)
    # Since we are using our model only for inference, switch to `eval` mode:
    model.eval()

    imagenet_class_index = json.load(open(class_file))
    with open(image_file, 'rb') as f:
        image_bytes = f.read()
        tensor = transform_image(image_bytes=image_bytes)
        outputs = model.forward(tensor)
        _, y_hat = outputs.max(1)
        predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]

#testing
def test():
    img = '/tmp/dog.jpg'
    cf = '/tmp/imagenet_class_index.json'

    p = predict(img, cf)
    print(f'Given image is: {p[1]}')
