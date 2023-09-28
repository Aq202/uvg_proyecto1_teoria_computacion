def generate_txt(name, text):
  with open(f'{name}', 'w', encoding='UTF-8') as f:
    f.write(text)
    print(text)