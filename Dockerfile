FROM python:2.7-onbuild
ENV COUCH http://localhost:5984
ENTRYPOINT python zergling.py
