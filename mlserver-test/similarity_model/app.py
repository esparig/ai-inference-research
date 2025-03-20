import spacy
import wikipediaapi

nlp = spacy.load("en_core_web_lg")

wiki_wiki = wikipediaapi.Wikipedia('MyMovieEval (example@example.com)', 'en')
barbie = wiki_wiki.page('Barbie_(film)').summary
oppenheimer = wiki_wiki.page('Oppenheimer_(film)').summary

print(barbie)
print()
print(oppenheimer)

doc1 = nlp(barbie)
doc2 = nlp(oppenheimer)

print(doc1.similarity(doc2))
