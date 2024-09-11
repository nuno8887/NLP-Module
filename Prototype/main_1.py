import spacy
from spacy.tokens import Doc, Span
from spacy.pipeline import EntityRuler
from spacy.matcher import Matcher
import pprint

nlp = spacy.load("en_core_web_lg")

ruler = nlp.add_pipe('entity_ruler', before='ner')

split_patterns = [

    #FIRST PART-------------------------------------------
    {"label": "IF_CLOUSE", "pattern": [{"LEMMA": "if"}]},
    {"label": "THEN_CLOUSE", "pattern": [{"LEMMA": "then"}]},
    {"label": "AND_CLOUSE_NUM", "pattern": [{"LIKE_NUM": True}, {"LOWER": "and"}, {"LIKE_NUM": True}]},
    {"label": "AND_CLOUSE", "pattern": [{"LOWER": "and"}]},
    {"label": "OR_CLOUSE_NUM", "pattern": [{"LIKE_NUM": True}, {"LOWER": "or"}, {"LIKE_NUM": True}]},
    {"label": "OR_CLOUSE", "pattern": [{"LOWER": "or"}]},
    #---------------------------------------------------------

    # Define patterns for "nsubj", "prep", "pobj"
    {"label": "NOUN_PHRASE","pattern": [{"DEP": "nsubj"},{"DEP": "prep"},{"DEP": "pobj"}]},

    #LESS THAN
    {"label": "LESS_THAN", "pattern": [{"LOWER": "less"}, {"LOWER": "than"}]},# less than
    {"label": "LESS_THAN", "pattern": [{"LOWER": "fewer"}, {"LOWER": "than"}]},# fewer than
    {"label": "LESS_THAN", "pattern": [{"LOWER": "lower"}, {"LOWER": "than"}]},# lower than
    {"label": "LESS_THAN", "pattern": [{"LOWER": "smaller"}, {"LOWER": "than"}]},# smaller than

    #LESS or EQUAL TO
    {"label": "LESS_EQUAL", "pattern": [{"LOWER": "no"}, {"LOWER": "more"}, {"LOWER": "than"}]},# no more than
    {"label": "LESS_EQUAL", "pattern": [{"LOWER": "not"}, {"LOWER": "more"}, {"LOWER": "than"}]},# not more than
    {"label": "LESS_EQUAL", "pattern": [{"LOWER": "less"}, {"LOWER": "or"}, {"LOWER": "equal"}]}, # less or equal to
    {"label": "LESS_EQUAL", "pattern": [{"LOWER": "lower"}, {"LOWER": "or"}, {"LOWER": "equal"}]}, # lower or equal to
    {"label": "LESS_EQUAL", "pattern": [{"LOWER": "smaller"}, {"LOWER": "or"}, {"LOWER": "equal"}]}, # smaller or equal to
    {"label": "LESS_EQUAL", "pattern": [{"LOWER": "at"}, {"LOWER": "most"}]},  # at most
    {"label": "LESS_EQUAL", "pattern": [{"LOWER": "up"}, {"LOWER": "to"}]},  # up to
    {"label": "LESS_EQUAL", "pattern": [{"LOWER": "not"}, {"LOWER": "exceed"}]},  # not exceed



    #BIGGER THAN
    {"label": "BIGGER_THAN", "pattern": [{"LOWER": "bigger"}, {"LOWER": "than"}]}, # bigger than
    {"label": "BIGGER_THAN", "pattern": [{"LEMMA": "more"}, {"LOWER": "than"}]},# more than
    {"label": "BIGGER_THAN", "pattern": [{"LOWER": "exceed"}]},  # exceed


    #BIGGER or EQUAL TO
    {"label": "BIGGER_EQUAL", "pattern": [{"LOWER": "greater"}, {"LOWER": "or"}, {"LOWER": "equal"}]}, # greater or equal to
    {"label": "BIGGER_EQUAL", "pattern": [{"LOWER": "bigger"}, {"LOWER": "or"}, {"LOWER": "equal"}]}, # bigger or equal to
    {"label": "BIGGER_EQUAL", "pattern": [{"LOWER": "equal"}, {"LOWER": "or"}, {"LOWER": "greater"}, {"LOWER": "than"}]},  # equal or greater than
    {"label": "BIGGER_EQUAL", "pattern": [{"LOWER": "not"}, {"LOWER": "less"}, {"LOWER": "than"}]},  # not less than
    {"label": "BIGGER_EQUAL", "pattern": [{"LOWER": "not"}, {"LOWER": "less"}, {"LOWER": "than"}]},  # no less than
    {"label": "BIGGER_EQUAL", "pattern": [{"LOWER": "at"}, {"LOWER": "least"}]},  # at least
    

    #EQUAL TO
    {"label": "EQUAL_TO", "pattern": [{"LOWER": "equal"}]},# equal

    #BETWEEN
    {"label": "BETWEEN", "pattern": [{"LOWER": "between"}]},# between

    #NOTBETWEEN
    {"label": "NOTBETWEEN", "pattern": [{"LOWER": "not"}, {"IS_ALPHA": True, "OP": "*"}, {"LOWER": "between"}]}, #not... between
    {"label": "NOTBETWEEN", "pattern": [{"LOWER": "can't"}, {"IS_ALPHA": True, "OP": "*"}, {"LOWER": "between"}]},# can´t ... between
    {"label": "NOTBETWEEN", "pattern": [{"LOWER": "can"}, {"LOWER": "not"}, {"IS_ALPHA": True, "OP": "*"}, {"LOWER": "between"}]}, # can not ... between
    {"label": "NOTBETWEEN", "pattern": [{"LOWER": "cannot"}, {"IS_ALPHA": True, "OP": "*"}, {"LOWER": "between"}]},# cannot ... between
    {"label": "NOTBETWEEN", "pattern": [{"LOWER": "do"}, {"LOWER": "not"}, {"IS_ALPHA": True, "OP": "*"}, {"LOWER": "between"}]},# do not ... between
    {"label": "NOTBETWEEN", "pattern": [{"LOWER": "does"}, {"LOWER": "not"}, {"IS_ALPHA": True, "OP": "*"}, {"LOWER": "between"}]},# does not ... between
    {"label": "NOTBETWEEN", "pattern": [{"LOWER": "did"}, {"LOWER": "not"}, {"IS_ALPHA": True, "OP": "*"}, {"LOWER": "between"}]},# did not ... between
    {"label": "NOTBETWEEN", "pattern": [{"LOWER": "will"}, {"LOWER": "not"}, {"IS_ALPHA": True, "OP": "*"}, {"LOWER": "between"}]},#will not ... between


    # NUM and/or NUM
    {"label": "NUM_pairing", "pattern": [{"LIKE_NUM": True}, {"LOWER": "and"}, {"LIKE_NUM": True}]},
    {"label": "NUM_pairing", "pattern": [{"LIKE_NUM": True}, {"LOWER": "or"}, {"LIKE_NUM": True}]},
    {"label": "NUM", "pattern": [{"LIKE_NUM": True}]},
    
]

ruler.add_patterns(split_patterns)


# Sample text
# TTabelaRegistos must have no more than 2 TTabelaSubRegistos and Camp is equal to 2 and Lamp is less than 4 and TTable is equal to 5.
#Each TTabelaRegistos must have no more than 2 TTabelaSubRegistos if CampoInteiroA of TTabelaRegistos is bigger than 10.

#doc = nlp("User_GDAI must have no more than 2 TTabelaSubRegistos and Camp is equal to 2 and Lamp is less than 4 and User_GDAI is equal to 5.")

# Function to split sentence spans based on conjunctions and clauses
def split_sentence_spans(doc):
    if_start = 0
    clause_spans = []
    current_clause = None

    for token in doc:
        if token.ent_type_ == "IF_CLOUSE":
            clause_spans.append(Span(doc, if_start, token.i))
            if_start = token.i
            current_clause = "IF"
        elif token.ent_type_ == "THEN_CLOUSE":
            clause_spans.append(Span(doc, if_start, token.i))
            if_start = token.i
            current_clause = "THEN"
        elif token.ent_type_ in ("AND_CLOUSE", "OR_CLOUSE"):
            clause_spans.append(Span(doc, if_start, token.i))
            if_start = token.i

    if if_start != 0:
        clause_spans.append(Span(doc, if_start, len(doc)))
    
    # If no spans were added, add the entire doc as a single span
    if not clause_spans:
        clause_spans.append(Span(doc, 0, len(doc)))

    return [span for span in clause_spans if span.text.strip()]

# Split the document into spans
#clause_spans = split_sentence_spans(doc)
#print (f"clause_spans: {clause_spans}")
def classify_spans(clause_spans):
    main_CLOUSE = {
        "MAIN": [],
        "AND_MAIN": [],
        "OR_MAIN": []
    }
    if_CLOUSE = {
        "IF_MAIN": [],
        "IF_AND_MAIN": [],
        "IF_OR_MAIN": [],
        "THEN": []
    }
    
    current_clause = "MAIN"
    
    for span in clause_spans:
        if any(token.ent_type_ == "IF_CLOUSE" for token in span):
            current_clause = "IF_MAIN"
            if_CLOUSE[current_clause].append(span[1:].text.strip())  # Skip the first token ("if")
        elif any(token.ent_type_ == "THEN_CLOUSE" for token in span):
            current_clause = "THEN"
            if_CLOUSE[current_clause].append(span[1:].text.strip())  # Skip the first token ("then")
        elif any(token.ent_type_ == "AND_CLOUSE" for token in span):
            if current_clause == "IF_MAIN":
                if_CLOUSE["IF_AND_MAIN"].append(span[1:].text.strip())  # Skip the conjunction ("and")
            else:
                main_CLOUSE["AND_MAIN"].append(span[1:].text.strip())  # Skip the conjunction ("and")
        elif any(token.ent_type_ == "OR_CLOUSE" for token in span):
            if current_clause == "IF_MAIN":
                if_CLOUSE["IF_OR_MAIN"].append(span[1:].text.strip())  # Skip the conjunction ("or")
            else:
                main_CLOUSE["OR_MAIN"].append(span[1:].text.strip())  # Skip the conjunction ("or")
        else:
            if current_clause == "IF_MAIN":
                if_CLOUSE[current_clause].append(span.text.strip())
            else:
                main_CLOUSE["MAIN"].append(span.text.strip())
    
    return main_CLOUSE, if_CLOUSE

#main_CLOUSE, if_CLOUSE = classify_spans(clause_spans)

#print("main_CLOUSE:", main_CLOUSE)
#print("if_CLOUSE:", if_CLOUSE)

def formating_clauses(doc):
    Subject = None
    Object = None
    Preposition = None
    Numbers = {}
    Relations = {}

    allowed_labels = {"LESS_THAN", "LESS_EQUAL", "BIGGER_THAN", "BIGGER_EQUAL", "EQUAL_TO", "BETWEEN", "NOTBETWEEN"}

    # Determine the entity label to use for numbers
    entity_label = "EQUAL_TO"  # Default label
    for ent in doc.ents:
        if ent.label_ in allowed_labels:
            entity_label = ent.label_
            break

    for token in doc:
        if token.dep_ == "nsubj":
            Subject = token.text
            # Capture compound subjects
            for child in token.children:
                if child.dep_ == "conj":
                    Subject += ' and ' + child.text
        elif token.dep_ == "pobj" and not token.like_num:
            Preposition = token.text
        elif token.dep_ == "dobj" and not token.like_num:
            Object = token.text
            # Capture compound objects
            for child in token.children:
                if child.dep_ == "conj":
                    Object += ' and ' + child.text
         # Handle the tokens if they are part of "NUM_pairing" or "NUM" entities
    for ent in doc.ents:
        if ent.label_ in {"NUM_pairing", "NUM"}:
            if entity_label not in Numbers:
                Numbers[entity_label] = []
            Numbers[entity_label].append(ent.text)

    
    # Check if "NOUN_PHRASE" is in the phrase
    has_noun_phrase = any(ent.label_ == "NOUN_PHRASE" for ent in doc.ents)
       
    if Subject and not Object and not Preposition:
        for key in Numbers:
            Relations[Subject] = Numbers[key][0]
            break
    
    elif Subject and Preposition and not Object and has_noun_phrase:
        if has_noun_phrase:
            for key in Numbers:
                Relations[Subject] = Numbers[key][0]
                break
        else:
            for key in Numbers:
                Relations[Preposition] = Numbers[key][0]
                break
    
    elif Object:
        for key in Numbers:
            Relations[Object] = Numbers[key][0]
            break
     



    # Optional: print the variables and dictionary to see the extracted information
    #print("Subject:", Subject)
    #print("Object:", Object)
    #print("Preposition:", Preposition)
    #print("Numbers:", Numbers)
    #print("Relations:", Relations)
    
    # Return the variables and dictionary if needed
    return Subject, Object, Preposition, Numbers, Relations


def classify_relations(main_CLOUSE, if_CLOUSE):
    docs = []
    dic_main_CLOUSE = {
        "MAIN": [],
        "AND": [],
        "OR": []
    }
    dic_if_CLOUSE = {
        "MAIN": [],
        "AND": [],
        "OR": [],
        "THEN": []
    }

    # Process main_CLOUSE
    for key, clauses in main_CLOUSE.items():
        for idx, clause in enumerate(clauses, 1):
            doc = nlp(clause)
            docs.append(doc)
            #print(f"\nDependencies for {key} clause: {clause}")
            Subject, Object, Preposition, Numbers, Relations = formating_clauses(doc)
            
            # Construct the structure for each clause
            clause_info = [
                {"Subject": Subject},
                {"Object": Object},
                {"Preposision": Preposition},
                {"NUM": Numbers},
                {"Relations": Relations}
            ]
            
            if key == "MAIN":
                dic_main_CLOUSE["MAIN"].append({str(idx): clause_info})
            elif key == "AND_MAIN":
                dic_main_CLOUSE["AND"].append({str(idx): clause_info})
            elif key == "OR_MAIN":
                dic_main_CLOUSE["OR"].append({str(idx): clause_info})

    # Process if_CLOUSE
    for key, clauses in if_CLOUSE.items():
        for idx, clause in enumerate(clauses, 1):
            doc = nlp(clause)
            docs.append(doc)
            #print(f"\nDependencies for {key} clause: {clause}")
            Subject, Object, Preposition, Numbers, Relations = formating_clauses(doc)
            
            # Construct the structure for each clause
            clause_info = [
                {"Subject": Subject},
                {"Object": Object},
                {"Preposision": Preposition},
                {"NUM": Numbers},
                {"Relations": Relations}
            ]
            
            if key == "IF_MAIN":
                dic_if_CLOUSE["MAIN"].append({str(idx): clause_info})
            elif key == "IF_AND_MAIN":
                dic_if_CLOUSE["AND"].append({str(idx): clause_info})
            elif key == "IF_OR_MAIN":
                dic_if_CLOUSE["OR"].append({str(idx): clause_info})
            elif key == "THEN":
                dic_if_CLOUSE["THEN"].append({str(idx): clause_info})

    return docs, dic_main_CLOUSE, dic_if_CLOUSE


# Call the function
#docs, dic_main_CLOUSE, dic_if_CLOUSE = classify_relations(main_CLOUSE, if_CLOUSE)

def identify_modal_operators(doc):
    modal_label = "MODAL_OPERATOR_PERMISSION"  # Default value

    # Initialize the SpaCy matcher and add the patterns
    matcher = Matcher(nlp.vocab)
    modal_patterns = [
        {"label": "MODAL_OPERATOR_PROHIBITION", "pattern": [{"LOWER": "must"}, {"LOWER": "not"}]},# must not
        {"label": "MODAL_OPERATOR_PERMISSION", "pattern": [{"LOWER": "can"}]},# can
        {"label": "MODAL_OPERATOR_PERMISSION", "pattern": [{"LOWER": "may"}]},# may
        {"label": "MODAL_OPERATOR_OBLIGATION", "pattern": [{"LOWER": "must"}, {"LOWER": {"NOT_IN": ["not"]}}]},  # must (not followed by "not")
        {"label": "MODAL_OPERATOR_OBLIGATION", "pattern": [{"LOWER": "shall"}]},# shall
        {"label": "MODAL_OPERATOR_OBLIGATION", "pattern": [{"LOWER": "can"}, {"LOWER": "only"}]},# can only
    ]

    for pattern in modal_patterns:
        matcher.add(pattern["label"], [pattern["pattern"]])

    # Apply the matcher to the document
    matches = matcher(doc)

    # Check for matches and assign the modal label
    for match_id, start, end in matches:
        modal_label = nlp.vocab.strings[match_id]
        break  # Stop after finding the first relevant match

    return modal_label

def extract_main_info(dic_main_CLOUSE):
    main_info = []

    for clause in dic_main_CLOUSE.get("MAIN", []):
        for key, details in clause.items():
            info = {
                "Subject": None,
                "Object": None,
                "Preposition": None,
                "Number_1": None,
                "Number_2": None,
                "Relations": {},
                "Numerical_Relationships": None
            }
            
            for detail in details:
                if "Subject" in detail:
                    info["Subject"] = detail["Subject"]
                elif "Object" in detail:
                    info["Object"] = detail["Object"]
                elif "Preposision" in detail:
                    info["Preposition"] = detail["Preposision"]
                elif "NUM" in detail:
                    for num_type, values in detail["NUM"].items():
                        if num_type not in ["NUM", "NUM_pairing"]:
                            numbers = values[0].split(' and ')
                            info["Number_1"] = numbers[0]
                            if len(numbers) > 1:
                                info["Number_2"] = numbers[1]
                            info["Numerical_Relationships"] = num_type
                elif "Relations" in detail:
                    info["Relations"] = detail["Relations"]

            main_info.append(info)

    return main_info

def generate_sbvr_rule(modal_label, main_info):
    sbvr_rule = ""

    for info in main_info:
        subject = info["Subject"]
        preposition = info["Preposition"]
        number_1 = info["Number_1"]
        number_2 = info["Number_2"]
        numerical_relationship = info["Numerical_Relationships"]

        # Construct the rule based on the available information
        if numerical_relationship and number_1:
            if numerical_relationship == "NOTBETWEEN" and number_2:
                rule = f"Each {subject} that is part of {preposition} must not have a value between {number_1} and {number_2}."
            elif numerical_relationship == "BETWEEN" and number_2:
                rule = f"Each {subject} that is part of {preposition} must have a value between {number_1} and {number_2}."
            elif numerical_relationship == "LESS_THAN":
                rule = f"Each {subject} that is part of {preposition} must have a value less than {number_1}."
            elif numerical_relationship == "LESS_EQUAL":
                rule = f"Each {subject} that is part of {preposition} must have a value less or equal to {number_1}."
            elif numerical_relationship == "BIGGER_THAN":
                rule = f"Each {subject} that is part of {preposition} must have a value greater than {number_1}."
            elif numerical_relationship == "BIGGER_EQUAL":
                rule = f"Each {subject} that is part of {preposition} must have a value greater or equal to {number_1}."
            elif numerical_relationship == "EQUAL_TO":
                rule = f"Each {subject} that is part of {preposition} must have a value equal to {number_1}."
        else:
            rule = f"Each {subject} that is part of {preposition} must have a value of {number_1}."

        # Add modal operator
        if modal_label == "MODAL_OPERATOR_PERMISSION":
            rule = rule.replace("must", "may")
        elif modal_label == "MODAL_OPERATOR_OBLIGATION":
            rule = rule.replace("must", "must")
        elif modal_label == "MODAL_OPERATOR_PROHIBITION":
            rule = rule.replace("must", "must not")

        sbvr_rule = rule
        break  # Since we are creating a single rule, we can break after the first iteration

    return sbvr_rule

def substitute_keys(main_info, validation):
    # Create a dictionary from the validation list for quick lookup
    validation_dict = {v: k for item in validation for k, v in item.items()}
    
    # Create a new list for the updated main_info
    updated_main_info = []

    # Iterate through each item in main_info
    for info in main_info:
        # Create a new dictionary to store updated keys
        updated_info = {}
        
        for key, value in info.items():
            if key in ['Subject', 'Object', 'Preposition'] and value in validation_dict:
                updated_key = validation_dict[value]
                updated_info[updated_key] = value
            else:
                updated_info[key] = value
        
        # Add the updated dictionary to the new list
        updated_main_info.append(updated_info)
                
    return updated_main_info

def append_additional_info(updated_main_info, phrase, sbvr_rule, modal_label):
    for info in updated_main_info:
        info['NL'] = phrase
        info['SBVR'] = sbvr_rule
        info['MODAL_OPERATOR'] = modal_label
    return updated_main_info

validation = [
{'NOUN':'User_GDAI'},
{'VERB':'TTabelaRegistos'},
{'NOUN':'CampoTextoA'},
{'NOUN':'CampoInteiroA'}
]
def main(phrase, validation):

    doc = nlp(phrase)
    clause_spans = split_sentence_spans(doc)
    main_CLOUSE, if_CLOUSE = classify_spans(clause_spans)
    docs, dic_main_CLOUSE, dic_if_CLOUSE = classify_relations(main_CLOUSE, if_CLOUSE)

    # Identify modal operators
    modal_label = identify_modal_operators(doc)

     # Extract main clause information
    main_info = extract_main_info(dic_main_CLOUSE)

    # Generate SBVR rule
    sbvr_rule = generate_sbvr_rule(modal_label, main_info)

    updated_main_info = substitute_keys(main_info, validation)

    # Append additional information
    updated_main_info = append_additional_info(updated_main_info, phrase, sbvr_rule, modal_label)


    return docs, dic_main_CLOUSE, dic_if_CLOUSE, phrase, modal_label, main_info, phrase, sbvr_rule, updated_main_info

# TTabelaRegistos must have no more than 2 TTabelaSubRegistos and Camp is equal to 2 and Lamp is less than 4 and TTable is equal to 5.
#Each TTabelaRegistos must have no more than 2 TTabelaSubRegistos if CampoInteiroA of TTabelaRegistos is bigger than 10.
#User_GDAI must have no more than 2 TTabelaSubRegistos and Camp is equal to 2 and Lamp is less than 4 and User_GDAI is equal to 5.
#The CampoInteiroA of TTabelaRegistos must be a value between 10 and 20.
#The CampoTextoA of TTabelaRegistos must not exceed 200 characters.
#Each TTabelaRegistos must have no more than 2 TTabelaSubRegistos
#The CampoInteiroA of TTabelaRegistos must not be a value between 5 and 10.

#"""
phrase = "The CampoInteiroA of TTabelaRegistos must not be a value between 5 and 10."

docs, dic_main_CLOUSE, dic_if_CLOUSE, text, modal_labels, main_info, phrase, sbvr_rule, updated_main_info = main(phrase, validation)

# Print the updated dictionaries
"""
print(text)
print()
print("dic_main_CLOUSE")
pprint.pprint(dic_main_CLOUSE)
print()
print("dic_if_CLOUSE")
pprint.pprint(dic_if_CLOUSE)
print()
print(docs)
print(modal_labels)
print(main_info)
print(phrase)
print(sbvr_rule)
"""
print(updated_main_info)
#"""



