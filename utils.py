import json
import pandas as pd
from typing import Dict, List


def text2json(text: str) -> List[Dict]:
    """Converts a text to a json

    Args:
        text (str): text to convert

    Returns:
        List[Dict]: json
    """
    text = text.replace("```", "").replace("json", "")
    return json.loads(text)


def save_csv(topics_raw: List[Dict], file_path: str) -> None:
    """Save topics in a csv file

    Args:
        topics_raw (List[Dict]): topics to save
        file_path (str): file_path to save the topics

    """
    df = pd.DataFrame.from_dict(topics_raw)
    complted_name_file = file_path + ".csv"
    df.to_csv(complted_name_file)
