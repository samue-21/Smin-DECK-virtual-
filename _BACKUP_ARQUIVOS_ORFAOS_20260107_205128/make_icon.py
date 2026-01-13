from PIL import Image

img = Image.open("assets/logo 3.ico")

sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]

img.save("assets/app.ico", format="ICO", sizes=sizes)

print("Ícone criado com sucesso!")
