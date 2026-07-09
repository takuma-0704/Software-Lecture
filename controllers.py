"""
controllers.py - シーケンス図の RecipeController / RecommendationController に相当
"""
from models import Recipe, DailyRecommendation
from recipe_service import RecipeService


class RecipeController:
    """レシピ検索フローを制御する（シーケンス図①）"""

    def __init__(self, service: RecipeService):
        self._service = service

    def search_recipes(self, ingredient: str, food_type: str) -> list[Recipe]:
        """食材・ジャンルでレシピを検索して返す"""
        return self._service.search_recipe(ingredient, food_type)

    def get_recipe(self, recipe_id: int) -> Recipe | None:
        """レシピIDで詳細を取得する"""
        return self._service.get_recipe_detail(recipe_id)

    def get_additional_ingredients(self, recipe_id: int) -> list:
        """使用食材一覧を取得する（ユースケース図「追加食材を見る」）"""
        return self._service.recommend_ingredient(recipe_id)

    def add_recipe(self, form) -> Recipe:
        """フォームから送られてきた内容で新しいレシピを作成する"""
        return self._service.add_recipe(
            recipe_name=form.get("recipe_name", ""),
            food_type=form.get("food_type", ""),
            cook_time=form.get("cook_time", ""),
            difficulty=form.get("difficulty", ""),
            ingredients_text=form.get("ingredients", ""),
            steps_text=form.get("steps", ""),
        )


class RecommendationController:
    """今日のおすすめフローを制御する（おすすめシーケンス図）"""

    def __init__(self, service: RecipeService):
        self._service = service

    def get_recommendation(self) -> DailyRecommendation | None:
        """今日のおすすめ料理とレシピ情報を返す"""
        return self._service.get_today_recommendation()
