from textblob import TextBlob
class SentimentAnalyzer:
    def analyze(self, text):
        blob = TextBlob(text)
        return blob.sentiment.polarity