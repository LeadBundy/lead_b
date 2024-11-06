from transformers import AutoTokenizer, AutoModel
import torch
from torchvision import models, transforms
from PIL import Image

# Загрузка модели для анализа текста (BERT)
text_model_name = 'distilbert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(text_model_name)
text_model = AutoModel.from_pretrained(text_model_name)

# Пример функции для обработки текста
def get_text_features(text):
    inputs = tokenizer(text, return_tensors='pt')
    outputs = text_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)  # Векторизация текста

# Загрузка модели для анализа изображений (ResNet)
image_model = models.resnet50(pretrained=True)
image_model.eval()

# Функция обработки изображений
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def get_image_features(image_path):
    image = Image.open(image_path)
    image_tensor = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        features = image_model(image_tensor)
    return features  # Вектор изображения
