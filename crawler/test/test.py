import sys
import pyttsx3
import PyPDF2



pdfFileObj = open('test.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
a = pdfReader.numPages
print(a)

# marker for while loop
x = 1

# user answer collector
c = 1


# Reads the PDF

def read(page):
    """
    read pdf and print content of specified page
    :param page: str or int, page to read
    :return: None
    """
    page_content = pdfReader.getPage(int(page))
    b = page_content.extractText()
    print(b)
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)
    engine.say(b)
    engine.say("Page number " + str(page) + " is completed")
    engine.runAndWait()
    engine.stop()


# The main code
while (x):
    page = input("Enter the page number to read :")

    read(page)
    c = int(input("Do you want to continue? (1)Yes (2)No"))
    if c == 2:
        x = 0
        print("Thank you")

