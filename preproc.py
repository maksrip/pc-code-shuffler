
# Попередня обробка текстового файлу
#t = open('text_LOTR.txt', 'r')
t = open('text_The jungle book_Kipling.txt')
readTextFromFile = t.read()

#Видалення символів
removeSpecialChars = readTextFromFile.translate ({ord(c): " " for c in "--@#$%^&*()[]»{};:,/<>\|`~-=_+"}).replace('"',' ')
removeSpecialChars = removeSpecialChars.replace("!"," ").replace("'","").replace("?"," ").lower()
res = ' '.join(removeSpecialChars.split())[3:]

#Відкриття файлу для запису

fileforsave = open('savedtext.txt','w')
fileforsave.write(res)

#Закриваємо файли
t.close()
fileforsave.close()
