"""Small helper to build a visitor badge label."""


def badge_label(first_name, last_name, company):
    # Builds the text printed on a visitor badge.
    label = first_name.strip() + " " + last_name.strip()
    if company:
        label += " (" + company + ")"
    return label[:40]
