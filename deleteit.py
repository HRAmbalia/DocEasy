import requests
import json

instructions = {
  'parts': [
    {
      'file': 'document'
    }
  ],
  'actions': [
    {
      'type': 'watermark',
      'image': 'logo',
      'width': '25%'
    }
  ]
}

response = requests.request(
  'POST',
  'https://api.pspdfkit.com/build',
  headers = {
    'Authorization': 'Bearer pdf_live_dM9fhAsWkOXv2ctQsusElVRhESAu41mTwtU5WrtA1sF'
  },
  files = {
    'document': open('document.pdf', 'rb'),
    'logo': open('logo.png', 'rb')
  },
  data = {
    'instructions': json.dumps(instructions)
  },
  stream = True
)

if response.ok:
  with open('result.pdf', 'wb') as fd:
    for chunk in response.iter_content(chunk_size=8096):
      fd.write(chunk)
else:
  print(response.text)
  exit()

