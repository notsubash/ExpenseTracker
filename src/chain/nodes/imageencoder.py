import base64

def encode_image(image_input):
    if isinstance(image_input, str):
        # If it's a file path
        with open(image_input, "rb") as image_file:
            image_data = image_file.read()
    else:
        # If it's a file-like object (e.g., UploadedFile)
        image_data = image_input.read()

    encoded_image = base64.b64encode(image_data).decode('utf-8')
    return encoded_image

def image_encoder_node(state):
    new_state = state.copy()

    image_location = state.get("image_location")
    image_base64 = state.get("image_base64")

    if image_location:
        image_base64 = encode_image(image_location.strip())
    elif not image_base64:
        raise ValueError("No image location or base64 data provided")

    new_state["image_base64"] = image_base64

    return new_state