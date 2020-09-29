import models as m


def nan_to_none(value):
    return None if value != value else value


def find_institution_id(session, institution_name):
    institution_id = session.query(m.Institution.id).filter_by(name=institution_name).one()
    return institution_id[0]


def find_compound_ids(session):
    return {
        'mehg': session.query(m.Compound.id).filter_by(name='MeHg').one()[0],
        'total_hg': session.query(m.Compound.id).filter_by(name='Total Hg').one()[0],
        'percent_loi': session.query(m.Compound.id).filter_by(name='% LOI').one()[0]
    }


def find_isotope_ids(session):
    return {
        '199Hg-FeS': session.query(m.Isotope.id).filter_by(name='199Hg-FeS').one()[0],
        'nano-200HgS': session.query(m.Isotope.id).filter_by(name='nano-200HgS').one()[0],
        '201Hg-humic': session.query(m.Isotope.id).filter_by(name='201Hg-humic').one()[0],
        '202Hg2+': session.query(m.Isotope.id).filter_by(name='202Hg2+').one()[0],
        'Ambient Hg': session.query(m.Isotope.id).filter_by(name='Ambient Hg').one()[0]
    }


def find_system_sample_id(session, query_dict):
    sample_id = session.query(m.Sample.id).filter_by(**query_dict)
    return sample_id[0] if sample_id.count() > 0 else None


def insert_record(session, model, create_params):
    new_record = model(**create_params)
    session.add(new_record)
    session.commit()
    return new_record
