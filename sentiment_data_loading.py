from qrmine import Content
from qrmine import Network
from qrmine import Qrmine
from qrmine import ReadData
from qrmine import Sentiment
from qrmine import MLQRMine
import textacy


## Read the text file(s)
data = ReadData()
inp_file = [["./sentiment_data/marshall_planet.txt"],["./sentiment_data/marshall_planet2.txt"],["./sentiment_data/stepanova_airmo.txt"]]
data.read_file(inp_file[2])

q = Qrmine()
all_interviews = Content(data.content)
doc = textacy.make_spacy_doc(all_interviews.doc)
q.print_categories(doc, 50) # 10 categories

s = Sentiment()
s.sentiment_analyzer_scores(doc.text)
print(s.sentiment()) # neutral

q.content = data

q.print_dict(all_interviews, 5)
