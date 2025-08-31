def calculate_grade(total_awards):
    # Example grading logic (customize as needed)
    if total_awards >= 100_000_000_000:
        return 'F'
    elif total_awards >= 50_000_000_000:
        return 'D'
    elif total_awards >= 10_000_000_000:
        return 'C'
    elif total_awards >= 1_000_000_000:
        return 'B'
    else:
        return 'A'