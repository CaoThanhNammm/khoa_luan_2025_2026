import google.generativeai as genai
genai.configure(api_key='AIzaSyAndwhiQHj1Tdo82CT0idA1RpkkoSG87Dw')
model = genai.GenerativeModel('gemini-1.5-flash')
print(model.generate_content("Hello").text)