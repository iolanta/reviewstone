from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score

def text_classifier(vectorizer, transformer, classifier):
    return Pipeline(
            [("vectorizer", vectorizer),
            ("transformer", transformer),
            ("classifier", classifier)],
            )

def TestClassifier(all_reviews, labels):
    vect = CountVectorizer(ngram_range = (1, 2))

    for clf in [MultinomialNB, LinearSVC, KNeighborsClassifier, LogisticRegression, DecisionTreeClassifier]:
        print clf.__name__
        print 'precision: %f' % (cross_val_score(text_classifier(vect,
            TfidfTransformer(), clf()), all_reviews, labels, cv = 5, scoring = 'precision').mean())
        print 'recall: %f' % (cross_val_score(text_classifier(vect,
            TfidfTransformer(), clf()), all_reviews, labels, cv = 5, scoring = 'recall').mean())
        print '\n'

def ReviewsTone():
    pos_list = []
    neg_list = []
    with open('pos_reviews.txt', 'r') as f1, open('neg_reviews.txt', 'r') as f2:
        pos_list = f1.readlines()[0:1200]
        neg_list = f2.readlines()[0:1200]
    all_reviews = neg_list + pos_list
    labels = [0] * len(neg_list) + [1] * len(pos_list)

    TestClassifier(all_reviews, labels)

    clf = text_classifier(CountVectorizer(ngram_range = (1, 2)), TfidfTransformer(), LinearSVC())
    clf.fit(all_reviews, labels)

    str1 = "Great content! Happy reading with this magazine! Also a good tool for learning English. Love it!"
    str2 = "Great product but tiny tiny tiny. I'm happy with it, I needed a new bronzer this is my first Balm product and i'm quite happy with."
    str3 = "My kid was not happy with this thing. And it stinks, like smells bad. Comes crushed and took a few days to retain its shape. Did I tell you it stinks?"
    str4 = "It is was a nice shirt but the first time washing in warm water abs drying on extra low the shirt shrunk one size and I can no longer wear it. Will never buy this brand again!"

    print clf.predict([str1, str2, str3, str4])

if __name__ == '__main__':
    ReviewsTone()
