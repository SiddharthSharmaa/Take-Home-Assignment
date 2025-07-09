import ollama

def is_academic(affiliation: str, model_name: str = "llama3:8b") -> bool:
    """
    Check if an affiliation is academic using an LLM.

    Args:
        affiliation (str): The affiliation string to check.
        model_name (str): The model to use for classification.

    Returns:
        bool: True if the affiliation is considered academic, False otherwise.
    """

    prompt = f"""
    Is the following affiliation academic or not? Reply with only 'Yes' or 'No'.

    Affiliation: "{affiliation}"
    """

    response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
    answer = response['message']['content'].strip().lower()

    return answer.startswith("yes")


def is_pharma_biotech(affiliation: str, model_name: str = "llama3:8b") -> bool:
    """
    Check if an affiliation is related to the pharmaceutical or biotech industry using an LLM.

    Args:
        affiliation (str): The affiliation string to check.
        model_name (str): The Ollama model to use. Defaults to "llama3:8b".

    Returns:
        bool: True if the affiliation is considered pharmaceutical or biotech, False otherwise.
    """
    prompt = (
        f"Is the following affiliation related to pharmaceutical or biotech industry? "
        f"Reply with only 'Yes' or 'No'.\n\nAffiliation: \"{affiliation}\""
    )

    response = ollama.chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response["message"]["content"].strip().lower()
    return answer.startswith("yes")