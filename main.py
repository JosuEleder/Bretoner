import os, random
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))
path = ROOT_DIR + "/data/Freeling/"
firstword = 0

POS_map = {"A":"adjective", "D":"determiner", "N":"noun", "P":"pronoun", "R":"adverb", "V":"verb", "C":"conjunction", "I":"interjection", "W":"date", "Z":"number", "S":"preposition", "F":"punctuation"}
subpos_map = {"O":"ordinal", "Q":"qualificative", "P":"possessive", "A":"article", "D":"demonstrative", "I":"indefinite", "T":"interrogative", "E":"exclamative"}
type_map = {"C":"common", "P":"proper", "0":"none"}
conjtype_map = {"C":"coordinating", "S":"subordinating", "0":"none"}
prontype_map = {"D":"demonstrative", "I":"indefinite", "T":"interrogative", "E":"exclamative", "P":"personal", "R":"relative", "0":"none"}
advtype_map = {"N":"negative", "G":"general", "0":"none"}
numtype_map = {"d":"partitive", "m":"currency", "p":"percentage", "u":"unit", "0":"none"}
verbtype_map = {"M":"main", "A":"auxiliary", "S":"semiauxiliary"}
punct_map = {"Fd":"colon", "Fc":"comma", "Flt":"curlybracket_close", "Fla":"curlybracket_open", "Fs":"etc", "Fat":"exclamationmark_close", "Faa":"exclamationmark_open", "Fg":"hyphen", "Fz":"other", "Fpt":"parenthesis_close", "Fpa":"parenthesis_open", "Ft":"percentage", "Fp":"period", "Fit":"questionmark_close", "Fia":"questionmark_open", "Fe":"quotation", "Frc":"quotation_close", "Fra":"quotation_open", "Fx":"semicolon", "Fh":"slash", "Fct":"squarebracket_close", "Fca":"squarebracket_open"}
degree_map = {"S":"superlative", "V":"evaluative", "0":"positive"}
gender_map = {"F":"feminine", "M":"masculine", "C":"common", "0":"none"}
number_map = {"S":"singular", "P":"plural","N":"invariable", "0":"none"}
neclass_map = {"S":"person", "G":"location", "O":"organization", "V":"other", "0":"none"}
possessorpers_map = {"1":"1", "2":"2","3":"3", "0":"none"}
possessornum_map = {"S":"singular", "P":"plural","N":"invariable", "0":"none"}
person_map = {"1":"1", "2":"2","3":"3", "0":"none"}
proncase_map = {"N":"nominative", "A":"accusative", "D":"dative", "O":"oblique", "0":"none"}
polite_map = {"P":"polite", "0":"none"}
mood_map = {"I":"indicative", "S":"subjunctive", "M":"imperative", "P":"participle", "G":"gerund", "N":"infinitive", "0":"none"}
tense_map = {"P":"present", "I":"imperfect", "F":"future", "S":"past", "C":"conditional", "0":"none"}

dictionary = []
#Carga del diccionario Freeling ES 4.2
def load_dictionary ():
    entry = {}
    #abaciales abacial AQ0CP00
    filelist = os.listdir(path)
    for file in filelist:
        with open(path + file) as f:
            for line in f:
                (form, lemma, features) = line.split()
                POS = POS_map[features[0]]
                subpos = degree = gender = number = person = possessorpers = possessornum = neclass = polite = mood = tense = "none"
                if POS=="adjective":
                    subpos = subpos_map[features[1]]
                    degree = degree_map[features[2]]
                    gender = gender_map[features[3]]
                    number = number_map[features[4]]
                    possessorpers = possessorpers_map[features[5]]
                    possessornum = possessornum_map[features[6]]
                if POS=="noun":
                    subpos = type_map[features[1]]
                    gender = gender_map[features[2]]
                    number = number_map[features[3]]
                    possessorpers = possessorpers_map[features[5]]
                    possessornum = possessornum_map[features[6]]
                    neclass = neclass_map[features[4]]
                if POS=="conjunction":
                    subpos = conjtype_map[features[1]]
                if POS=="determiner":
                    subpos = subpos_map[features[1]]
                    person = person_map[features[2]]
                    gender = gender_map[features[3]]
                    number = number_map[features[4]]
                    proncase = possessorpers = "none"
                    possessornum = possessornum_map[features[5]]
                if POS=="pronoun":
                    subpos = prontype_map[features[1]]
                    person = person_map[features[2]]
                    gender = gender_map[features[3]]
                    number = number_map[features[4]]
                    proncase = proncase_map[features[5]]
                    polite = polite_map[features[6]]
                if POS=="adverb":
                    subpos = advtype_map[features[1]]
                if POS=="number":
                    subpos = numtype_map[features[1]]
                if POS=="verb":
                    subpos = verbtype_map[features[1]]
                    mood = mood_map[features[2]]
                    tense = tense_map[features[3]]
                    person = person_map[features[4]]
                    number = number_map[features[5]]
                    gender = gender_map[features[6]]
                if POS=="punctuation":
                    subpos = punct_map[features]
                entry = {"form": form, "lemma":lemma, "POS":POS, "subpos":subpos, "degree":degree, "gender":gender, "number":number, "person":person, "possessorpers":possessorpers, "possessornum":possessornum, "neclass":neclass, "polite":polite, "mood":mood, "tense":tense, "features":features}
                dictionary.append(entry)

def get_sentence():
    #frase formada por: determinante, sustantivo, adjetivo, verbo presente, determinante, sustantivo, adverbio
    genders = ["feminine", "masculine"]
    numbers = ["singular", "plural"]
    moods = ["indicative", "subjunctive"]
    tenses = ["present", "imperfect", "future", "past", "conditional"]
    gender = genders[random.randint(0, len(genders)-1)]
    number = numbers[random.randint(0, len(numbers)-1)]
    mood = moods[random.randint(0, len(moods)-1)]
    tense = tenses[random.randint(0, len(tenses)-1)]
    person = "3"
    global firstword; firstword=0

    sentence = get_noun_phrase(gender, number)
    sentence = sentence + " " + get_verb_phrase(mood, tense, number, person)
    sentence = sentence + " " + get_noun_phrase(gender, number)

    print(sentence)

def get_noun_phrase(gender, number):
    #sintagma formado por: determinante, sustantivo, adjetivo
    global firstword
    phrase = get_word("determiner", gender, number)
    if firstword==0: phrase = phrase.capitalize()
    firstword += 1
    phrase = phrase + " " + get_word("noun", gender, number)
    phrase = phrase + " " + get_word("adjective", gender, number)
    return (phrase)

def get_verb_phrase(mood, tense, number, person):
    #sintagma formado por: verbo
    phrase = get_verb(mood, tense, number, person)
    return (phrase)

def get_word(POS, gender, number):
    words=[d["form"] for d in dictionary if (d["POS"]==POS and d["gender"]==gender and d["number"]==number)]
    word = words[random.randint(0, len(words)-1)]
    return(word)

def get_verb(mood, tense, number, person):
    POS="verb"
    verbs=[d["form"] for d in dictionary if (d["POS"]==POS and d["mood"]==mood and d["tense"]==tense and d["person"]==person) and d["number"]==number]
    if len(verbs)==0: verbs=[d["form"] for d in dictionary if (d["POS"]==POS and d["mood"]=="indicative" and d["tense"]==tense and d["person"]==person) and d["number"]==number]
    verb = verbs[random.randint(0, len(verbs)-1)]
    return(verb)

load_dictionary()
get_sentence()