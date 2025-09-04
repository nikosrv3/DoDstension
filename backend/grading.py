def calculate_grade(total_awards):
    # Example grading logic (customize as needed)
    if total_awards >= 100_000_000_000:
        return 4
    elif total_awards >= 50_000_000_000:
        return 3
    elif total_awards >= 10_000_000_000:
        return 2
    elif total_awards >= 1_000_000_000:
        return 1
    else:
        return 0