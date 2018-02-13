from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

def TestReviews():
    pos_list = []
    neg_list = []
    with open('pos_reviews.txt', 'r') as f1, open('neg_reviews.txt', 'r') as f2:
        pos_list = f1.readlines()[0:1200]
        neg_list = f2.readlines()[0:1200]

    print (len(pos_list))
    print (len(neg_list))
    all_reviews = neg_list + pos_list
    labels = [0] * len(neg_list) + [1] * len(pos_list)
    text_clf = Pipeline([('vectorizer', TfidfVectorizer()),
                        ('classifier', LinearSVC()),
    ])

    text_clf.fit(all_reviews, labels)
    str1 = "I ordered 1 year Vogue on November 7th, and received 1 copy on December 14 (it was scheduled for end of January).Love Vogue for superb high fashion, make up, great pics. My favorite fashion magazine."
    str2 = "I really love Alexa. She keeps my shopping list efficiently on my phone. She greets me with interesting facts each morning and a joke and the weather if I ask. She sounds great when I ask her to play my favorite station. There are a lot of things she does that I don't even know yet....however, every once in awhile I am denied because I don't have amazon prime......"
    str3 = "I have fine hair. This oil, no matter how little I use, just weighs down my hair and makes it look oily. I didn't notice any change in the actual health of my hair. Maybe people with dry, curly hair can use it."
    str4 = "The roses were not fresh and already wilting when I got them. I could have gotten a better quality from Safeway much cheaper."
    str5 = "IF you enjoy musical numbers you will love this. This movie cuts into a musical number WAY too much for my taste. One number and then minutes of story and then another number and another and another. P.T. Barnum released in 1999 with Lloyd Bridges tells the STORY of Barnum with loads of detail THIS IS MUSICAL NUMBERS - your choice. YOU HAVE BEEN WARNED."

    print (text_clf.predict([str1, str2, str3, str4, str5]))

if __name__ == '__main__':
    TestReviews()
