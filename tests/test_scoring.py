from devflow.scoring import weighted_score, evidence_confidence


def test_weighted_score_ignores_na():
    cats = [
        {"id":"security","score":80,"confidence":80,"applicable":True},
        {"id":"server_load","score":None,"confidence":0,"applicable":True},
        {"id":"seo","score":None,"confidence":100,"applicable":False},
    ]
    assert weighted_score(cats) == 80.0
    assert evidence_confidence(cats) < 80
