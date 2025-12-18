



def filter_by_priority(cases, priority):
    result = []
    for case in cases:
        if case["priority"] == priority:
            result.append(case)
    return result
