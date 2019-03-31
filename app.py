from flask import Flask, request, render_template
from medacy.ner.pipelines import FDANanoDrugLabelPipeline, ClinicalPipeline
from medacy.ner import Model
from spacy.displacy import EntityRenderer
from random import choice

app = Flask(__name__)


def init_models():
    all_models = {}

    # FDA Drug Labels
    # fda_entities = ['dose', 'inactiveingredient', 'routeofadministration', 'duration', 'corecomposition',
    #             'activeingredient', 'volumeofdistribution', 'adversereaction', 'tradename', 'company', 'frequency',
    #             'co-administereddrug']
    # fda_pipeline = FDANanoDrugLabelPipeline(metamap=False, entities=fda_entities)
    # fda_model = Model(fda_pipeline)
    # fda_model.load("FIXME")  # TODO replace with actual model
    # all_models["fda"] = fda_model

    # Clinical Notes
    clinical_entities = ["CellLine", "Dose", "DoseDuration", "DoseDurationUnits", "DoseFrequency", "DoseRoute",
                         "DoseUnits", "Endpoint", "EndpointUnitOfMeasure", "GroupName", "GroupSize", "SampleSize",
                         "Sex", "Species", "Strain", "TestArticle", "TestArticlePurity", "TestArticleVerification",
                         "TimeAtDose", "TimeAtFirstDose", "TimeAtLastDose", "TimeEndpointAssessed", "TimeUnits",
                         "Vehicle"]
    clinical_pipeline = ClinicalPipeline(metamap=None, entities=clinical_entities)
    clinical_model = Model(clinical_pipeline)
    clinical_model.load_external('medacy_model_clinical_notes')
    all_models["clinical"] = clinical_model


    # Create list of all entities
    # all_entities = list(set(fda_entities + clinical_entities))
    all_entities = clinical_entities

    return all_models, all_entities


def init_displacy(entities):
    """Instantiate the EntityRenderer with a custom color scheme"""
    colors = ["#4C2C04", "#1C1505", "#6F663F", "#284D1", "#162C25"]
    # Randomly map colors to entities
    color_scheme = {k: choice(colors) for k in entities}
    er = EntityRenderer(options={"colors": color_scheme})
    return er


@app.route('/medacy')
def render_medacy():
    global models, er
    model_name = request.args.get("model")
    input_text = request.args.get("text")

    selected_model = models[model_name]
    prediction = selected_model.predict(input_text)
    entity_tuples = prediction.get_entity_annotations()

    displacy_list = []
    for e in entity_tuples:
        displacy_dict = {"start": int(e[1]), "end": int(e[2]), "label": e[0]}
        displacy_list.append(displacy_dict)

    html = er.render_ents(input_text, displacy_list, "_")
    formatted_entities = html  # TODO integrate output into displayed page

    return render_template("index.html", predictions=formatted_entities)


@app.route('/')
def initial_output():
    """The page before any interaction takes place"""
    return render_template("index.html")


if __name__ == '__main__':
    models, all_entities = init_models()
    er = init_displacy(all_entities)
    # app.run(host='0.0.0.0', port=5000)
    app.run(port=5000)
    # app.run(host="0.0.0.0")