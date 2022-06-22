# from PyPDF2 import PdfReader

# reader = PdfReader("testpdf.pdf")
# print(reader.documentInfo)

# number_of_pages = len(reader.pages)
# page = reader.pages[0]
# text = page.extract_text()
# print(reader.getNumPages())

# str=""
# for i in range(1,11):
# #    print(reader.getPage(i))
#    str+=reader.getPage(i).extractText()

# with open("text.txt",'w') as f:
#     f.write(str)  

# import PyPDF2
# pdf_file = open('testpdf.pdf', 'rb',encoding='utf-8')
# read_pdf = PyPDF2.PdfFileReader(pdf_file)
# number_of_pages = read_pdf.getNumPages()
# page = read_pdf.getPage(0)
# page_content = page.extractText()
# print(page_content.encode('utf-8'))   


from PyPDF2 import PdfReader

reader = PdfReader("testpdf.pdf")
page = reader.pages[0]
print(type(page))
print(page.extract_text())