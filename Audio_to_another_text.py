from ibm_watson import SpeechToTextV1 
import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pandas import json_normalize
from ibm_watson import LanguageTranslatorV3


#audio to text API URL
url_s2t = "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/4765ed89-ef57-421f-83d9-a7599cd2fe54"

#audio to text API key
iam_apikey_s2t = "enter you API key here"

#this will aurthenticate audio to text API key
authenticator = IAMAuthenticator(iam_apikey_s2t)
s2t = SpeechToTextV1(authenticator=authenticator)
s2t.set_service_url(url_s2t)
print(s2t)

#audio file that needs to convert
filename='enter your WAV file here'

with open(filename, mode="rb")  as wav:
    response = s2t.recognize(audio=wav, content_type='audio/mp3')

#result is dictionary which contain text
print(response.result)

#convert into human readable formate (tabluer formate)
normalize_text= json_normalize(response.result['results'],"alternatives")
print(normalize_text)

#this will print data in JSON or dictionary formate
#print(response)

#it will print only first line 
recognized_text=response.result['results'][0]["alternatives"][0]["transcript"]
print(recognized_text)


#convert english text to another language 
#one language text to another language text API URL
url_lt= "https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/1f2156be-9009-42f6-ac9d-44955e25e4f5"

#one language text to another language text API key
apikey_lt= "enter your key here"

#this API require current version of language translator
version_lt='2021-12-24'


#this will aurthenticate one language text to another language text API key
authenticator = IAMAuthenticator(apikey_lt)
language_translator = LanguageTranslatorV3(version=version_lt,authenticator=authenticator)
language_translator.set_service_url(url_lt)
print(language_translator)


#this will print list of differnt language availavle to in translator
print(json_normalize(language_translator.list_identifiable_languages().get_result(), "languages"))

#this will translate into spanish (language we had selected)
translation_response = language_translator.translate(\
    text=recognized_text, model_id='en-es')
print(translation_response)
print(type(translation_response))


#convert into dictionary type
translation=translation_response.get_result()
print(translation)
print(type(translation))

#it will print only spanish translation string, first string only
spanish_translation =translation['translations'][0]['translation']
print(spanish_translation)

#get back in english again as dictionary
translation_new = language_translator.translate(text=spanish_translation ,model_id='es-en').get_result()
print(translation_new)
print(type(translation_new))

#get back in english again as string
translation_eng=translation_new['translations'][0]['translation']
print(translation_eng)
print(type(translation_eng))


#convert into french into string type
French_translation=language_translator.translate(
    text=translation_eng , model_id='en-fr').get_result()

print(French_translation['translations'][0]['translation'])
print(type(French_translation['translations'][0]['translation']))