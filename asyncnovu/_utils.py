# Function to format Novu server responses.
def format(code, r) -> dict[str, str]:
    """
    Function to parse Novu server responses into a consistent format.

            Parameters:
                    code (int): Status code returned by Novu.
                    r (dict): Dictionary representation of the response JSON returned by Novu.

            Returns:
                dict: Formatted dictionary representation of the Novu response JSON.

    """

    response = {"status_code": code}
    if "data" in r:
        response["detail"] = r["data"]
    else:
        r.pop("statusCode", None)
        response["detail"] = r
    return response
