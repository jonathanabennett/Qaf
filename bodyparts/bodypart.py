class BodyPart:
    """A BodyPart is used for the damage model. Stats include
1) Injuries list
2) thresholds
3) blood points"""

    owner = attr.ib(default=None)
    injuries = attr.ib()
    threshold = attr.ib()
    blood_points = attr.ib()
    current_bp = attr.ib()
