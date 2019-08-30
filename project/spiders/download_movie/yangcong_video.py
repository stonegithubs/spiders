import requests

html_data = requests.get('http://yangcong345.com/teacherIndex.html')
with open('yangcong.html','wb') as f:
    f.write(html_data.content.decode())