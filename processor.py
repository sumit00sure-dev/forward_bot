from config import DEFAULT_CAPTION

def process_caption(old):
    if not old:
        return DEFAULT_CAPTION
    return f"{old}\n\n{DEFAULT_CAPTION}"