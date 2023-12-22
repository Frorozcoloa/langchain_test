from sentence_transformers import SentenceTransformer, util
import pandas as pd
from typing import Dict, List, Tuple

from utils import save_csv




def get_model():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def get_data()->Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    trends  = pd.read_csv("datasets_output/trends.csv")
    user = pd.read_csv("datasets_output/users_description.csv")
    products = pd.read_csv("datasets_output/products_TOPIC.csv")
    return trends, user, products

def scoring_calculated(model, serie_main, serie_compare)->Dict:
    """Returns a dictionary with the score of each topic"""
    
    embl_main = model.encode(serie_main)
    embl_compare = model.encode(serie_compare)
    score = util.cos_sim(embl_main, embl_compare)
    return score.mean(axis=1)


def get_score_trends(model, trends: pd.DataFrame, user: pd.DataFrame, products: pd.DataFrame)->pd.DataFrame:
    """Returns a dataframe with the score of each topic"""
    title_trends = trends["product_to_sell"]
    description_trends = trends["product_decription"]
    
    title_product = products["type_classes"]
    description_product = products["class_description"]
    
    # Scoring title
    st_trends_producto = scoring_calculated(model, title_product, title_trends)
    sd_trends_producto = scoring_calculated(model, description_product, description_trends)
    std_trends_producto = scoring_calculated(model, title_product, description_trends)
    std_trends_producto = scoring_calculated(model, description_product, title_trends)
    
    score = st_trends_producto + sd_trends_producto + std_trends_producto + std_trends_producto
    products["score"] = score
    print(products.sort_values(by="score", ascending=False))
    
    #Scoring user and product
    title_user = user["topic_name"]
    description_user = user["topic_description"]
    filter_title_user = products[products["score"] > 0.2]["type_classes"]
    filter_description_user = products[products["score"] > 0.2]["class_description"]
    
    st_person_producto = scoring_calculated(model, title_user, filter_title_user)
    sd_person_producto = scoring_calculated(model, description_user,filter_description_user)
    std_person_producto = scoring_calculated(model, title_user, filter_description_user)
    std_person_producto = scoring_calculated(model, description_user, filter_title_user)
    
    score = st_person_producto + sd_person_producto + std_person_producto + std_person_producto
    user["score"] = score
    user = user.sort_values(by="score", ascending=False)
    save_csv(user, "user_score")

if __name__ == "__main__":
    model = get_model()
    trends, user, products = get_data()
    get_score_trends(model, trends, user, products)
    
    