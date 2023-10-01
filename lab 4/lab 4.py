import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

# Загрузка стоп-слов
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))
blog_data = [
    "Why it’s helpful to understand AI as a data scientist Although currently, not all data scientists make use of AI, the trends are certainly pointing in the direction of increased AI usage. This means that data scientists with an in-depth knowledge of AI will be able to take advantage of new work opportunities – and indeed, those with a background in AI are highly valued by companies of all types. If you are a working data scientist, it may be worthwhile to build up your expertise in AI, as it is a lucrative and rapidly expanding field with job potential that will increase for the foreseeable future. AI Data Scientist Salary and Job Growth Dat Given the incredible functions AI experts are able to unlock, they are much sought-after by companies of all types, and therefore promise high salaries to skilled candidates. Now is an excellent time to enter the workforce as an AI data scientist. While the Bureau of Labor Statistics does not provide data exclusively focused on individuals with AI expertise, it reports stellar pay for positions that frequently include AI skills, such as software engineers, quality assurance analysts, and testers, who earn a median annual salary of $120,730. This number is even higher for professionals working in the domain of software publishing, who earn a median annual salary of $130,180. The job outlook for the positions listed above is similarly exceptional. The BLS reports a projected job growth rate of 25% by 2031, greatly outpacing most other industries. If you have been contemplating a career in AI engineering, this should come as great encouragement.",
    "Education is an extraordinarily diverse industry. Across institutions, hundreds of different departments exist with intersecting and entirely different data stores, some of which are necessary but others not. This is different in higher education. Educational bureaucracies are present in grades K-12, with comparable data needs. They are sifting through this data to figure out which is one of the specialties of data science and is central to data science applications in education. Education is one of many disciplines here with many functions, however. Data science itself is different in all cases. Some data scientists specialize in database architecture building, while others interpret and analyze data to generate comprehensible reports for educators. Data Security Because of the prevalence of the internet in all realms of life, cyber security has become a hot-button topic. It will increasingly continue to do so indefinitely. That’s why the Bureau of Labor Statistics predicts that jobs related to cyber security and computer science will generally grow from 2021-2031, making such jobs lucrative and highly secure. For computers to function well, they need good cybersecurity software to prevent hackers from obtaining sensitive data and exploiting it. This software should also detect potentially threatening data downloaded on one’s computer. Data scientists can function as the cyber-security software of an entire organization, storing data manually and protecting it in real time from potential online threats. Data science in education is, therefore, fundamental. Moreover, the data records educational intuitions possess and which they need to function appropriately contain highly sensitive information, including the personal and health information of students, faculty, and staff. Hence, educational institutions need something more substantial than software to protect and manage their data. The more sensitive the data is, and the larger the institution becomes, the more data science becomes necessary. This is exactly why data scientists are also critical to the government, healthcare, and the financial industry.",
]


def preprocess_text(text):
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum()]
    words = [word for word in words if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)


processed_data = [preprocess_text(text) for text in blog_data]

vectorizer = TfidfVectorizer(max_df=2, min_df=0.85, stop_words="english")  # Измененные значения max_df и min_df
tfidf = vectorizer.fit_transform(processed_data)

num_topics = 5
nmf = NMF(n_components=num_topics, random_state=1)
nmf.fit(tfidf)

feature_names = vectorizer.get_feature_names()
for topic_idx, topic in enumerate(nmf.components_):
    print(f"Topic #{topic_idx + 1}:")
    print([feature_names[i] for i in topic.argsort()[:-10 - 1:-1]])