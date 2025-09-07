def harvesine(lat1, lon1, lat2, lon2) -> float:
    """
    Calculate the harvesine distance between two points.
    """
    from math import sin, cos, sqrt, atan2, radians

    R = 3958.8  # Earth's radius in miles

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dLat = lat2 - lat1
    dLon = lon2 - lon1
    a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c  # in miles
    return distance


def driving_time(lat1, lon1, lat2, lon2, speed_mph=60):
    """
    Calculate the driving time between two points in hours.

    Use harvesine formula to calculate the distance between two points.
    Then divide the distance by the speed to get the time.
    """
    distance = harvesine(lat1, lon1, lat2, lon2)
    return distance / speed_mph
