import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def perform_point_transformations(image_paths, c=1):
    for image_path in image_paths:
        # Wczytywanie obrazu i konwersja na skalę szarości
        img = Image.open(image_path).convert('L')
        img_array = np.array(img, dtype=np.float32)
        
        # Mnożenie przez stałą
        img_array_multiplied = img_array * c
        img_array_multiplied[img_array_multiplied > 255] = 255  # ogranicz wartości do zakresu [0, 255]
        img_multiplied = Image.fromarray(img_array_multiplied.astype(np.uint8))
        plt.imshow(img_multiplied, cmap='gray')
        plt.title(f'Mnożenie przez stałą - {image_path}')
        plt.show()

        # Transformacja logarytmiczna
        img_array_log = c * np.log1p(img_array)  # np.log1p(x) oblicza log(1+x)
        img_array_log = (img_array_log / img_array_log.max()) * 255  # normalizacja do zakresu [0, 255]
        img_log = Image.fromarray(img_array_log.astype(np.uint8))
        plt.imshow(img_log, cmap='gray')
        plt.title(f'Transformacja logarytmiczna - {image_path}')
        plt.show()

# Lista obrazów do przetworzenia
image_paths = [
    'data/chest-xray.png',  
    'data/pollen-dark.png',  
    'data/spectrum.png'      
]

# Stała c dla przekształceń punktowych
c = 10.0

# Wykonanie przekształceń punktowych
perform_point_transformations(image_paths, c)
