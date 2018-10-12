from nltk.tokenize import sent_tokenize, word_tokenize
import string, nltk
from nltk.corpus import stopwords


def get_basic_dict():

    lookup_dict = {
        'restaurant': ['drink',
                       'eat',
                       'hungry',
                       'pizzeria',
                       'lunch',
                       'fast-food',
                       'restaurant'],

        'bar': ['drink',
                'cocktails',
                'pub',
                'bar',
                'beer',
                'bar'],

        'pharmacy': ['store',
                     'drug',
                     'pharmacy',
                     'pills',
                     'sick',
                     'paracetamol',
                     'pharmacy'],
        }

    return lookup_dict


class WeightedLocation:
    def __init__(self, location, score):
        self.location = location
        self.score = score

    def get_location(self):
        return self.location

    def get_score(self):
        return self.score


def occurrence_fun_generator(words):
    def calc_dict_score(input_dict):
        dict_words = input_dict
        presence_score = 1

        score_list = [0]

        for word in words:
            if word in dict_words:
                score_list.append(presence_score)

        score_sum = sum(score_list)
        return score_sum

    return calc_dict_score


def basic_classifier(words):
    lookup_dict = get_basic_dict()

    recommendations = []

    for location, keywords in lookup_dict.items():
        basic_scorer = occurrence_fun_generator(words)
        location_score = basic_scorer(keywords)
        recommendations.append(WeightedLocation(location, location_score))

    return recommendations


def get_best_recommendation(recommendations):
    best_weighted_location = max(recommendations, key=lambda x: x.get_score())

    return best_weighted_location.get_location()


def get_sanitized_words(text):
    stop_words = stopwords.words('english')

    remove_punctuation_map = dict((ord(char), None)
                                  for char in string.punctuation)
    tokens = nltk.word_tokenize(text.lower().translate(remove_punctuation_map))
    return [word for word in tokens if word not in stop_words]


def get_location_recommendation(text):
    words = get_sanitized_words(text)

    recommendations = basic_classifier(words)
    location = get_best_recommendation(recommendations)

    return location
