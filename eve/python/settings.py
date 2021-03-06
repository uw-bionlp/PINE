# (C) 2019 The Johns Hopkins University Applied Physics Laboratory LLC.

import logging
import os

LOGGER = logging.getLogger("pine.eve." + __name__)

collections = {
    'schema': {
        'creator_id': {'type': 'jhed', 'required': True},
        'annotators': {'type': 'list', 'schema':{'type':'string'}},
        'viewers': {'type': 'list', 'schema':{'type':'string'}},
        'labels': {'type': 'list','required': True},
        'metadata': {'type': 'dict'},
        'archived': {'type': 'boolean'},
        'configuration': {'type': 'dict'}
    },
    'item_methods': ['GET', 'PUT', 'PATCH']
}

documents = {
    'schema': {
        'creator_id': {'type': 'jhed', 'required': True},
        'collection_id': {'type': 'objectid', 'required': True},
        'overlap': {'type': 'integer'},
        'text': {'type': 'string'},
        'uri': {'type':'string'},
        'metadata': {'type': 'dict'},
        "has_annotated" : {'type' : 'dict'}
    },
    'item_methods': ['GET', 'PUT', 'PATCH'],
    'mongo_indexes':{'doc_creator_id': [('creator_id', 1)], 'doc_collection_id':[('collection_id', 1)]}
}

iaa_reports = {
    'schema' :{
        'collection_id' : { 'type' : 'objectid' },
        'num_of_annotators' : {'type' : 'integer'},
        'num_of_agreement_docs': {'type' : 'integer'},
        'num_of_labels' : { 'type' : 'integer'},
        'per_doc_agreement' : { 'type' : 'list'},
        'per_label_agreement': {'type': 'list'},
        'overall_agreement': {'type': 'dict'},
        'labels_per_annotator': {'type': 'dict'},
    },
    'item_methods': ['GET', 'PUT', 'PATCH'],
    'versioning': True

}


annotations = {
    'schema': {
        'creator_id': {'type': 'jhed', 'required': True},
        'collection_id': {'type': 'objectid', 'required': True},
        'document_id': {'type': 'objectid', 'required': True},
        'annotation': {'type': 'list'}
    },
    'mongo_indexes':{'ann_creator_id': [('creator_id', 1)], 'ann_collection_id':[('collection_id', 1)], 'ann_document_id':[('document_id',1)]},
    'item_methods':['GET', 'PUT', 'PATCH'],
    'versioning':True
}

pipelines = {
    'schema': {
        '_id':{'type':'objectid', 'required':True},
        'title': {'type': 'string', 'required': True},
        'name': {'type': 'string', 'required': True},
        'description': {'type': 'string'},
        'parameters': {'type': 'dict'}
    }
}

users = {
    'schema': {
        '_id':{'type': 'jhed', 'required': True},
        'firstname': {'type': 'string', 'required': True},
        'lastname': {'type': 'string', 'required': True},
        'email': {'type': 'string'},
        'description': {'type': 'string'},
        'role': {
            'type': 'list',
            'allowed': ['administrator', 'user'],
        },
        'passwdhash': {'type': 'string'}
    },
    'item_url': 'regex("[a-z]{4,9}[0-9]{1,4}")',
    #'item_lookup_field': '_id', # Name of object field ex. mongo object id here
    'query_objectid_as_string': True,
    'item_methods':['GET', 'PUT', 'DELETE']
}

classifiers = {
    'schema': {
        'collection_id': {'type': 'objectid', 'required': True},
        'overlap':{'type':'float', 'required':True},
        'pipeline_id':{'type':'objectid', 'required':True},
        'parameters':{'type':'dict'},
        'labels':{'type':'list', 'required':True},
        'filename':{'type':'string'},
        'train_every': {'type': 'integer', 'default': 100},
        'annotated_document_count': {'type': 'integer', 'default': 0}
    },
    'mongo_indexes':{'class_pipeline_id': [('pipeline_id', 1)], 'class_collection_id':[('collection_id', 1)]},
    'item_methods':['GET', 'PUT', 'PATCH'],
    'versioning':True
}

metrics = {
    'schema': {
        'collection_id': {'type': 'objectid', 'required': True},
        'classifier_id': {'type': 'objectid', 'required': True},
        'classifier_db_version': {'type': 'integer'},
        'documents': {'type': 'list', 'required': True},
        'annotations': {'type': 'list', 'required': True},
        'folds': {'type': 'list'},
        'metrics': {'type': 'list'},
        'metric_averages' : {'type': 'dict'},
        'filename': {'type': 'string'},
        'trained_classifier_db_version': {'type': 'integer'}
    },
    'mongo_indexes':{'metrics_classifier_id': [('classifier_id', 1)], 'doc_collection_id':[('collection_id', 1)]},
    'item_methods':['GET', 'PUT', 'PATCH'],
    'versioning':True
}

next_instances = {
    'schema':{
        'classifier_id':{'type':'objectid', 'required':True},
        'document_ids':{'type':'list', 'required':True},
        'overlap_document_ids':{'type':'dict', 'required':True}
    },
    'mongo_indexes':{'next_classifier_id': [('classifier_id', 1)]},
    'item_methods':['GET', 'PUT', 'PATCH']
}

parsed = {
    'schema': {
        'collection_id': {'type': 'objectid', 'required': True},
        '_id':{'type':'objectid', 'required':True},
        'text': {'type': 'string'},
        'spacy':{'type':'string'}
    },
    'mongo_indexes':{'doc_collection_id':[('collection_id', 1)]},
    'item_methods':['GET', 'PUT', 'PATCH']
}

DOMAIN={
    'collections':collections,
    'documents':documents,
    'annotations':annotations,
    'classifiers':classifiers,
    'metrics':metrics,
    'users':users,
    'pipelines':pipelines,
    'next_instances':next_instances,
    'parsed':parsed,
    'iaa_reports' : iaa_reports
}


if os.environ.get("MONGO_URI"):
    MONGO_URI = os.environ.get("MONGO_URI")
    #LOGGER.info("Eve using MONGO_URI={}".format(MONGO_URI))
else:
    MONGO_HOST = "localhost"
    MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
    LOGGER.info("Eve using MONGO_HOST={} and MONGO_PORT={}".format(MONGO_HOST, MONGO_PORT))

# Skip these if your db has no auth. But it really should.
#MONGO_USERNAME = '<your username>'
#MONGO_PASSWORD = '<your password>'
MONGO_DBNAME = 'pmap_nlp'

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PUT']

PAGINATION = False


