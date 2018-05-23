from googletrans import Translator

translator = Translator()
text = translator.translate("안녕하세요")
print(text.text)
