from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def load_and_display_image(image_path):
    # Wczytywanie i wyświetlanie obrazu
    img = Image.open('data/aerial_view.png')
    plt.imshow(img, cmap='gray')
    plt.title('Wczytany obraz')
    plt.axis('off')
    plt.show()

def plot_intensity_along_line(image_path, axis, coordinate):
    # Wykres zmian poziomu szarości wzdłuż linii
    img = Image.open('data/aerial_view.png').convert('L')
    pixels = np.array(img)
    
    if axis == 'horizontal':
        intensity = pixels[coordinate, :]
        label = 'Poziomo'
    elif axis == 'vertical':
        intensity = pixels[:, coordinate]
        label = 'Pionowo'
    
    plt.plot(intensity)
    plt.title(f'Zmiana poziomu szarości wzdłuż linii {label}')
    plt.xlabel('Pozycja na linii')
    plt.ylabel('Poziom szarości')
    plt.show()

def save_subimage(image_path, left, top, right, bottom, new_image_path):
    # Wycinanie i zapisywanie podobrazu
    img = Image.open('data/aerial_view.png')
    subimg = img.crop((left, top, right, bottom))
    subimg.save('data/aerial_new.png')
    print(f'Podobraz zapisany jako: {'data/aerial_new.png'}')

# Przykład użycia:
image_path = 'data/aerial_view.png'  # Zmień na właściwą ścieżkę do obrazu
load_and_display_image(image_path)
plot_intensity_along_line(image_path, 'horizontal', 100)  # Przykład dla linii poziomej
plot_intensity_along_line(image_path, 'vertical', 50)    # Przykład dla linii pionowej
save_subimage(image_path, 50, 50, 200, 200, 'nowy_obraz.jpg')  # Zmień współrzędne i nazwę nowego obrazu
