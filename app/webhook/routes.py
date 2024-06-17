from flask import Blueprint, json, request

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    return {}, 200

@webhook.route('/')
def root():
    print ('Welcome to the webhook assessment test run')
    return 'Welcome to the webhook assessment test run'
    