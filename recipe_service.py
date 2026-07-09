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

    def add_recipe(
        self,
        recipe_name: str,
        food_type: str,
        cook_time: str,
        difficulty: str,
        ingredients_text: str,
        steps_text: str,
    ) -> Recipe:
        """ユーザーが入力したフォームの内容から新しいレシピを作って保存する"""
        new_id = self._db.get_next_recipe_id()

        # 食材欄: 1行につき「食材名,分量」の形式を想定（分量は省略可）
        ingredients: list[Ingredient] = []
        for i, line in enumerate(ingredients_text.splitlines()):
            line = line.strip()
            if not line:
                continue
            if "," in line:
                name, amount = line.split(",", 1)
            elif "、" in line:
                name, amount = line.split("、", 1)
            else:
                name, amount = line, ""
            ingredients.append(
                Ingredient(
                    ingredient_id=i * 1000 + new_id,
                    ingredient_name=name.strip(),
                    amount=amount.strip(),
                )
            )

        # 手順欄: 1行につき1手順として扱う
        steps = []
        step_no = 1
        for line in steps_text.splitlines():
            line = line.strip()
            if not line:
                continue
            from models import RecipeStep
            steps.append(RecipeStep(step_no=step_no, description=line))
            step_no += 1

        recipe = Recipe(
            recipe_id=new_id,
            recipe_name=recipe_name.strip(),
            food_type=food_type.strip(),
            cook_time=cook_time.strip(),
            difficulty=difficulty.strip(),
            ingredients=ingredients,
            steps=steps,
        )
        self._db.add_recipe(recipe)
        return recipe
