# src/utils.py
def parse_tags(tags_str):
    """Parse a comma-separated string into a list of tags."""
    return [tag.strip() for tag in tags_str.split(',') if tag.strip()]