import models as m


def nan_to_none(value):
    return None if value != value else value


def find_institution_id(session, institution_name):
    institution_id = session.query(m.Institution.id).filter_by(name=institution_name).one()
    return institution_id[0]


def find_compound_ids(session):
    return {
        "mehg": session.query(m.Compound.id).filter_by(name='MeHg').one()[0],
        "total_hg": session.query(m.Compound.id).filter_by(name='Total Hg').one()[0],
        "percent_loi": session.query(m.Compound.id).filter_by(name='% LOI').one()[0]
    }


def sample_exists(session, sample_id, institution_id):
    print('Found sample id.')
    return session.query(m.Sample).filter_by(lab_sample_id=sample_id, institution_id=institution_id).count() > 0
