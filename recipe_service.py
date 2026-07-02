"""
recipe_service.py - クラス図の RecipeService に相当するサービス層
シーケンス図の Service レイヤーを担う
"""
from models import Recipe, Ingredient, DailyRecommendation
from data_recipes import RecipeDB


class RecipeService:

    def __init__(self, db: RecipeDB):
        self._db = db

    def search_recipe(self, ingredient: str = "", food_type: str = "") -> list[Recipe]:
        """食材・ジャンルでレシピを検索する（シーケンス図 step4-6）"""
        results = self._db.find_recipes_by_condition(ingredient, food_type)
        return results[:5]

    def get_recipe_detail(self, recipe_id: int) -> Recipe | None:
        """レシピ詳細を取得する（シーケンス図 step12-13）"""
        return self._db.find_recipe_by_id(recipe_id)

    def get_today_recommendation(self) -> DailyRecommendation | None:
        """今日のおすすめを取得する（おすすめシーケンス図 step3-4）"""
        return self._db.get_today_recommendation()

    def recommend_ingredient(self, recipe_id: int) -> list[Ingredient]:
        """使用食材一覧を返す（ユースケース図「追加食材を見る」）"""
        recipe = self._db.find_recipe_by_id(recipe_id)
        return recipe.ingredients if recipe else []
