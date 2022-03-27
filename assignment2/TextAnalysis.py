import random
import string
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import markovify


def process_file_HF(filename, skip_title=False):
    """Makes a histogram for HelloFresh that contains the words from a file.

    filename: string
    skip_header: boolean, whether to skip the post title

    returns: map from each word to the number of times it appears.
    """
    hist_HF = {}
    # needs encoding
    fp = open(filename, encoding='UTF8')

    if skip_title:
        skip_mealkit_header(fp)

    strippables = string.punctuation + string.whitespace

    for line in fp:
        if line.startswith('**END**'):
            break

        line = line.replace('-', ' ')

        for word in line.split():
            word = word.strip(strippables)
            word = word.lower()

            # Update the dictionary.
            hist_HF[word] = hist_HF.get(word, 0) + 1
    return hist_HF


def process_file_BA(filename, skip_title=False):
    """Makes a histogram for BlueApron that contains the words from a file.

    filename: string
    skip_header: boolean, whether to skip the post title

    returns: map from each word to the number of times it appears.
    """
    hist_BA = {}
    # needs encoding
    fp = open(filename, encoding='UTF8')

    if skip_title:
        skip_mealkit_header(fp)

    strippables = string.punctuation + string.whitespace

    for line in fp:
        if line.startswith('**END**'):
            break

        line = line.replace('-', ' ')

        for word in line.split():
            word = word.strip(strippables)
            word = word.lower()

            # Update the dictionary.
            hist_BA[word] = hist_BA.get(word, 0) + 1
    return hist_BA


def process_file_HC(filename, skip_title=False):
    """Makes a histogram for HomeChef that contains the words from a file.

    filename: string
    skip_header: boolean, whether to skip the post title

    returns: map from each word to the number of times it appears.
    """
    hist_HC = {}
    # needs encoding
    fp = open(filename, encoding='UTF8')

    if skip_title:
        skip_mealkit_header(fp)

    strippables = string.punctuation + string.whitespace

    for line in fp:
        if line.startswith('**END**'):
            break

        line = line.replace('-', ' ')

        for word in line.split():
            word = word.strip(strippables)
            word = word.lower()

            # Update the dictionary.
            hist_HC[word] = hist_HC.get(word, 0) + 1
    return hist_HC


def skip_mealkit_header(fp):
    """Reads from fp until it finds the line that ends the header.

    fp: open file object
    """
    for line in fp:
        if line.startswith('**START**'):
            break


def total_words_HF(hist_HF):
    """
    Returns the total of the frequencies in a histogram for HelloFresh.
    """
    return sum(hist_HF.values())


def total_words_BA(hist_BA):
    """
    Returns the total of the frequencies in a histogram for BlueApron.
    """
    return sum(hist_BA.values())


def total_words_HC(hist_HC):
    """
    Returns the total of the frequencies in a histogram for HomeChef.
    """
    return sum(hist_HC.values())


def different_words_HF(hist_HF):
    """
    Returns the number of different words in a histogram for HelloFresh.
    """
    return len(hist_HF.values())


def different_words_BA(hist_BA):
    """
    Returns the number of different words in a histogram for BlueApron.
    """
    return len(hist_BA.values())


def different_words_HC(hist_HC):
    """
    Returns the number of different words in a histogram for HomeChef.
    """
    return len(hist_HC.values())

# Characterizing by Word Frequencies.


def most_common_HF(hist_HF, excluding_stopwords=False):
    """Makes a list of word-freq pairs in descending order of frequency
    for HelloFresh.

    hist: map from word to frequency

    returns: list of (frequency, word) pairs
    """
    t_HF = []
    stopwords = process_file_HF('data/stopwords.txt')

    stopwords = list(stopwords.keys())
    for word, freq in hist_HF.items():
        if excluding_stopwords:
            if word in stopwords:
                continue
        else:
            t_HF.append((freq, word))
        t_HF.sort(reverse=True)
    return t_HF


def print_most_common_HF(hist_HF, num=10):
    """Prints the most commons words in a histgram and their frequencies.
    hist: histogram (map from word to frequency)
    num: number of words to print
    """
    t_HF = most_common_HF(hist_HF)
    print('The most common words on the HelloFresh subreddit are:')
    for freq, word in t_HF[:num]:
        print(word, '\t', freq)


def most_common_BA(hist_BA, excluding_stopwords=False):
    """Makes a list of word-freq pairs in descending order of frequency
    for BlueApron.

    hist: map from word to frequency

    returns: list of (frequency, word) pairs
    """
    t_BA = []
    stopwords = process_file_HF('data/stopwords.txt')

    stopwords = list(stopwords.keys())
    for word, freq in hist_BA.items():
        if excluding_stopwords:
            if word in stopwords:
                continue
        else:
            t_BA.append((freq, word))
        t_BA.sort(reverse=True)
    return t_BA


def print_most_common_BA(hist_BA, num=10):
    """Prints the most commons words in a histgram and their frequencies.
    hist: histogram (map from word to frequency)
    num: number of words to print
    """
    t_BA = most_common_BA(hist_BA)
    print('The most common words on the BlueApron subreddit are:')
    for freq, word in t_BA[:num]:
        print(word, '\t', freq)


def most_common_HC(hist_HC, excluding_stopwords=False):
    """Makes a list of word-freq pairs in descending order of frequency
    for HomeChef.

    hist: map from word to frequency

    returns: list of (frequency, word) pairs
    """
    t_HC = []
    stopwords = process_file_HC('data/stopwords.txt')

    stopwords = list(stopwords.keys())
    for word, freq in hist_HC.items():
        if excluding_stopwords:
            if word in stopwords:
                continue
        else:
            t_HC.append((freq, word))
        t_HC.sort(reverse=True)
    return t_HC


def print_most_common_HC(hist_HC, num=10):
    """Prints the most commons words in a histgram and their frequencies.
    hist: histogram (map from word to frequency)
    num: number of words to print
    """
    t_HC = most_common_HC(hist_HC)
    print('The most common words on the HomeChef subreddit are:')
    for freq, word in t_HC[:num]:
        print(word, '\t', freq)


def subtract(subs, wordfile):
    """Returns a dictionary with all keys that appear in each of the subreddits but not the word file.
    subs, wordfile: dictionaries
    """
    res = {}
    for key in subs:
        if key not in wordfile:
            res[key] = None
    return res


def random_word_HF(hist_HF, excluding_stopwords=True):
    """Chooses random words from the HelloFresh histogram.

    The probability of each word is proportional to its frequency.

    Excluding_stopwords = excludes stopwords.
    """
    stop = process_file_HF('data/stopwords.txt', False)

    stop = list(stop.keys())

    HF = []
    for word, freq in hist_HF.items():
        if excluding_stopwords:
            if word not in stop:
                HF.extend([word] * freq)
    return random.choice(HF)


def random_word_BA(hist_BA, excluding_stopwords=True):
    """Chooses random words from the BlueApron histogram.

    The probability of each word is proportional to its frequency.

    Excluding_stopwords = excludes stopwords.
    """
    stop = process_file_BA('data/stopwords.txt', False)

    stop = list(stop.keys())

    BA = []
    for word, freq in hist_BA.items():
        if excluding_stopwords:
            if word not in stop:
                BA.extend([word] * freq)
    return random.choice(BA)


def random_word_HC(hist_HC, excluding_stopwords=True):
    """Chooses random words from the HomeChef histogram.

    The probability of each word is proportional to its frequency.

    Excluding_stopwords = excludes stopwords.
    """
    stop = process_file_HC('data/stopwords.txt', False)

    stop = list(stop.keys())

    HC = []
    for word, freq in hist_HC.items():
        if excluding_stopwords:
            if word not in stop:
                HC.extend([word] * freq)
    return random.choice(HC)


# Sentiment analysis for HelloFresh.
hf_sentiment = 'single today to scratch but know very feel production know 5 a that at the we except much use 20 and lovely and miracles because to is a please i onion a aren\'t hello for bucks from in strips all this feels go cancel with market the that it\'s my fresh box have the shout with more new i meatballs tell had scampi all a really i time ingredients in able with 2 hf eating the and his gone garlic box discounted feel comfortable feel fresh my production garlic and a have hf all else in name email have garlic'
score_hf = SentimentIntensityAnalyzer().polarity_scores(hf_sentiment)

# Sentiment analysis for BlueApron.
ba_sentiment = 'and does dressed end weight with from recipes the started options so i and hate whatever as over weight whole content of went ba hey card i am those ingredients sauce really it potatoes to often does of were between when heat had trying having have send me and choices last bad how recipes do panko frozen fontina not needed know but got the so this smells know and everyone recipes pickled avoid arugula basalmic the of panko miso choices i gets was rice to idea in something the bad chicken the chicken both healthy blue the some smaller two'
score_ba = SentimentIntensityAnalyzer().polarity_scores(ba_sentiment)

# Sentiment analysis for HomeChef.
hc_sentiment = 'small and posts been support email we thoughts be good you of the the know for good and time be idea don\'t their card pick could the for of noticed desserts boxes are longer weekly me is time recipes decreasing customization appreciated it an be box ones know calorie up from glacé posted streak options it is the and if their has to and glacé other referral it me so seasoning of could comes to you contact thinly if place card has i weekly facts anyone the gold to under boxes pick referral help your good any the  time'
score_hc = SentimentIntensityAnalyzer().polarity_scores(hc_sentiment)


def main():
    hist_HF = process_file_HF('data/HelloFresh.txt', skip_title=True)
    # print(hist_HF)
    print('\n\nTotal number of words in the HelloFresh subreddit:', total_words_HF(hist_HF))
    print('Number of different words in the HelloFresh subreddit:', different_words_HF(hist_HF))

    t_HF = most_common_HF(hist_HF, excluding_stopwords=False)

    print('The most common words in the HelloFresh subreddit are:')
    for freq, word in t_HF[0:20]:
        print(word, '\t', freq)

    hist_HC = process_file_HC('data/HomeChef.txt', skip_title=True)
    # print(hist)
    print('Total number of words in the HomeChef subreddit:', total_words_HC(hist_HC))
    print('Number of different words in the HomeChef subreddit:', different_words_HC(hist_HC))

    t_HC = most_common_HC(hist_HC, excluding_stopwords=False)

    print('The most common words in the HomeChef subreddit are:')
    for freq, word in t_HC[0:20]:
        print(word, '\t', freq)

    words = process_file_HF('data/words.txt')
    words = process_file_HC('data/words.txt')
    words = process_file_BA('data/words.txt')

    hist_BA = process_file_BA('data/BlueApron.txt', skip_title=True)
    # print(hist)
    print('Total number of words in the BlueApron subreddit:', total_words_BA(hist_BA))
    print('Number of different words in the BlueApron subreddit:', different_words_BA(hist_BA))

    t_BA = most_common_BA(hist_BA, excluding_stopwords=False)

    print('The most common words in the BlueApron subreddit are:')
    for freq, word in t_BA[0:20]:
        print(word, '\t', freq)

    diff_HF = subtract(hist_HF, words)
    print("The words in the HelloFresh subreddit that aren't in the word file are:")
    for word in diff_HF.keys():
        print(word, end='\n ')

    diff_HC = subtract(hist_HC, words)
    print("The words in the HomeChef subreddit that aren't in the word file are:")
    for word in diff_HC.keys():
        print(word, end='\n ')

    diff_BA = subtract(hist_BA, words)
    print("The words in the BlueApron subreddit that aren't in the word file are:")
    for word in diff_BA.keys():
        print(word, end='\n ')

    print("\n\nHere are some random words from the HelloFresh subreddit:")
    for i in range(100):
        print(random_word_HF(hist_HF), end=' ')

    print("\n\nHere are some random words from the HomeChef subreddit:")
    for i in range(100):
        print(random_word_HC(hist_HC), end=' ')

    print("\n\nHere are some random words from the BlueApron subreddit:")
    for i in range(100):
        print(random_word_BA(hist_BA), end=' ')

    print(f'\n\n Here is the HelloFresh sentiment analysis scoring for some random words:\n {score_hf}')

    print(f'\n\n Here is the HomeChef sentiment analysis scoring for some random words:\n {score_hc}')

    print(f'\n\n Here is the BlueApron sentiment analysis scoring for some random words:\n {score_ba}')


# Graphing sentiment analysis: HelloFresh
sentiment_types = ['positive', 'neutral', 'negative']
hf_sent_results = [0.188, 0.788, 0.024]
Colors = ['green', 'gold', 'firebrick']
plt.bar(sentiment_types, hf_sent_results, color=Colors)
plt.title('HelloFresh Sentiment Analysis on Reddit', fontsize=14, color='mediumseagreen', weight='bold')
plt.xlabel('Sentiment', fontsize=14)
plt.ylabel('Score', fontsize=14)
plt.show()

# Graphing sentiment analysis: HomeChef
sentiment_types = ['positive', 'neutral', 'negative']
hc_sent_results = [0.159, 0.841, 0.00]
Colors = ['green', 'gold', 'firebrick']
plt.bar(sentiment_types, hc_sent_results, color=Colors)
plt.title('Home Chef Sentiment Analysis on Reddit', fontsize=14, color='darkgreen', weight='bold')
plt.xlabel('Sentiment', fontsize=14)
plt.ylabel('Score', fontsize=14)
plt.show()

# Graphing sentiment analysis: BlueApron
sentiment_types = ['positive', 'neutral', 'negative']
ba_sent_results = [0.033, 0.853, 0.114]
Colors = ['green', 'gold', 'firebrick']
plt.bar(sentiment_types, ba_sent_results, color=Colors)
plt.title('Blue Apron Sentiment Analysis on Reddit', fontsize=14, color='navy', weight='bold')
plt.xlabel('Sentiment', fontsize=14)
plt.ylabel('Score', fontsize=14)
plt.show()

# Graphing the Number of different words in each subreddit.
subreddit = ['HelloFresh', 'Home Chef', 'Blue Apron']
different_words = [367, 191, 369]
Colors = ['mediumseagreen', 'darkgreen', 'navy']
plt.bar(subreddit, different_words, color=Colors)
plt.title('n of Different Words in Each Subreddit', fontsize=14, weight='bold')
plt.xlabel('Brand', fontsize=14)
plt.ylabel('Number of Different Words', fontsize=14)
plt.show()


# cite: https://kandi.openweaver.com/python/jsvine/markovify

# HelloFresh Markov Text Generator
# Get raw text as string.
with open("data/HelloFresh.txt", encoding='utf8') as f_hello:
    for word in f_hello:
        text_hf = f_hello.read()
    else:
        text_hf = text_hf.replace('**END**', "")
        text_hf = text_hf.replace('**START**', "")

# Build the model.
text_model = markovify.Text(text_hf)

# Print five randomly-generated sentences
print(f'\nHelloFresh Markov Sentence Generator:\n')
for i in range(5):
    print(text_model.make_sentence(tries=300))


# Home Chef Markov Text Generator
# Get raw text as string.
with open("data/HomeChef.txt", encoding='utf8') as f_home:
    for word in f_home:
        text_hc = f_home.read()
    else:
        text_hc = text_hc.replace('**END**', "")
        text_hc = text_hc.replace('**START**', "")

# Build the model.
text_model = markovify.Text(text_hc)

# Print five randomly-generated sentences.
print(f'\nHomeChef Markov Sentence Generator:\n')
for i in range(5):
    print(text_model.make_sentence(tries=300))


# Blue Apron Markov Text Generator
# Get raw text as string.
with open("data/BlueApron.txt", encoding='utf8') as f_blue:
    for word in f_blue:
        text_ba = f_blue.read()
    else:
        text_ba = text_ba.replace('**END**', "")
        text_ba = text_ba.replace('**START**', "")

# Build the model.
text_model = markovify.Text(text_ba)

# Print five randomly-generated sentences.
print(f'\nBlue Apron Markov Sentence Generator:\n')
for i in range(5):
    print(text_model.make_sentence(tries=300))


if __name__ == '__main__':
    main()
