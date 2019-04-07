from flask import Flask, request, render_template
from medacy.ner import Model
from spacy.displacy import EntityRenderer
import random

app = Flask(__name__)


def init_models():
    """Creates a dictionary containing all the medaCy models used in this demo."""
    all_models = {}

    # FDA Drug Labels
    fda_entities = [
        'dose', 'inactiveingredient', 'routeofadministration', 'duration', 'corecomposition',
        'activeingredient', 'volumeofdistribution', 'adversereaction', 'tradename', 'company', 'frequency',
        'co-administereddrug'
    ]
    all_models["fda"] = Model.load_external('medacy_model_FDA_nanodrug_labels')

    # Clinical Notes
    clinical_entities = ['Drug', 'Form', 'Route', 'ADE', 'Reason', 'Frequency', 'Duration', 'Dosage', 'Strength']
    all_models["clinical"] = Model.load_external('medacy_model_clinical_notes')

    # Create list of all entities
    # all_entities = list(set(fda_entities + clinical_entities))
    all_entities = [*fda_entities, *clinical_entities]

    return all_models, all_entities


def random_color():
    """Returns the hex code for a random light color."""
    rand = lambda: random.randint(100, 255)
    return '#%02X%02X%02X' % (rand(), rand(), rand())


def init_displacy(entities):
    """Instantiate the EntityRenderer with a custom color scheme"""
    colors = ["#9AF4CC", "#f49ac2", "#F9C8DE", "#C2F49A", "#F49AC2"]
    # Randomly map colors to entities
    color_scheme = {k.upper(): random_color() for k in entities}
    print(color_scheme)
    er = EntityRenderer(
        options={
            "colors": color_scheme
        }
    )
    return er


@app.route('/', methods=["POST"])
def render_medacy():
    global models, er
    model_name = request.form["model"]
    input_text = request.form["text"]

    selected_model = models[model_name]
    prediction = selected_model.predict(input_text)
    entity_tuples = prediction.get_entity_annotations()

    displacy_list = []
    for e in entity_tuples:
        displacy_dict = {"start": int(e[1]), "end": int(e[2]), "label": e[0]}
        displacy_list.append(displacy_dict)
    html = er.render_ents(input_text, displacy_list, "")
    formatted_entities = html  # TODO integrate output into displayed page

    return render_template("index.html", predictions=formatted_entities)


@app.route('/')
def initial_output():
    """The page before any interaction takes place"""
    return render_template("index.html")


if __name__ == '__main__':
    models, all_entities = init_models()
    er = init_displacy(all_entities)
    print("For Vagrant, view at http://127.0.0.1:5000/")
    app.run(host='0.0.0.0', port=5000)
