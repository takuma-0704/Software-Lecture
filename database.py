"""
database.py - サンプルデータを持つインメモリDB
シーケンス図の Model(DB) に相当
"""
from datetime import date
from models import Recipe, Ingredient, RecipeStep, DailyRecommendation


class RecipeDB:

    def __init__(self):
        self._recipes: list[Recipe] = []
        self._daily_recommendation: DailyRecommendation | None = None
        self._load_sample_data()

    def find_recipes_by_condition(self, ingredient: str = "", food_type: str = "") -> list[Recipe]:
        """条件に一致するレシピを検索する"""
        results = self._recipes
        if ingredient:
            results = [
                r for r in results
                if ingredient in r.recipe_name
                or any(ingredient in ing.ingredient_name for ing in r.ingredients)
            ]
        if food_type:
            results = [r for r in results if r.food_type == food_type]
        return results

    def find_recipe_by_id(self, recipe_id: int) -> Recipe | None:
        """IDでレシピを取得する"""
        return next((r for r in self._recipes if r.recipe_id == recipe_id), None)

    def get_today_recommendation(self) -> DailyRecommendation | None:
        """今日のおすすめを取得する"""
        return self._daily_recommendation

    def add_recipe(self, recipe: Recipe) -> None:
        self._recipes.append(recipe)

    def set_recommendation(self, recommendation: DailyRecommendation) -> None:
        self._daily_recommendation = recommendation

    def _load_sample_data(self):
        recipes = [
            Recipe(
                recipe_id=1, recipe_name="鶏肉の照り焼き",
                food_type="和食", cook_time="20分", difficulty="簡単",
                ingredients=[
                    Ingredient(1, "鶏もも肉", "300g"),
                    Ingredient(2, "醤油", "大さじ3"),
                    Ingredient(3, "みりん", "大さじ2"),
                    Ingredient(4, "砂糖", "大さじ1"),
                ],
                steps=[
                    RecipeStep(1, "鶏もも肉を一口大に切る"),
                    RecipeStep(2, "醤油・みりん・砂糖を合わせてタレを作る"),
                    RecipeStep(3, "フライパンで鶏肉を中火で焼く"),
                    RecipeStep(4, "タレを加えて絡めながら煮詰める"),
                ],
            ),
            Recipe(
                recipe_id=2, recipe_name="豆腐の味噌汁",
                food_type="和食", cook_time="10分", difficulty="簡単",
                ingredients=[
                    Ingredient(5, "豆腐", "1/2丁"),
                    Ingredient(6, "わかめ", "適量"),
                    Ingredient(7, "だし汁", "400ml"),
                    Ingredient(8, "味噌", "大さじ2"),
                ],
                steps=[
                    RecipeStep(1, "だし汁を鍋に入れて火にかける"),
                    RecipeStep(2, "豆腐を一口大に切り加える"),
                    RecipeStep(3, "わかめを加える"),
                    RecipeStep(4, "味噌を溶かして完成"),
                ],
            ),
            Recipe(
                recipe_id=3, recipe_name="麻婆豆腐",
                food_type="中華", cook_time="20分", difficulty="普通",
                ingredients=[
                    Ingredient(9,  "豆腐", "1丁"),
                    Ingredient(10, "豚ひき肉", "100g"),
                    Ingredient(11, "豆板醤", "小さじ1"),
                    Ingredient(12, "甜麺醤", "小さじ1"),
                    Ingredient(13, "片栗粉", "大さじ1"),
                ],
                steps=[
                    RecipeStep(1, "豆腐を一口大に切り水切りする"),
                    RecipeStep(2, "ひき肉と豆板醤・甜麺醤を炒める"),
                    RecipeStep(3, "豆腐と水を加えて煮込む"),
                    RecipeStep(4, "片栗粉でとろみをつけて完成"),
                ],
            ),
            Recipe(
                recipe_id=4, recipe_name="パスタアラビアータ",
                food_type="イタリアン", cook_time="25分", difficulty="普通",
                ingredients=[
                    Ingredient(14, "パスタ", "200g"),
                    Ingredient(15, "トマト缶", "1缶"),
                    Ingredient(16, "にんにく", "2片"),
                    Ingredient(17, "唐辛子", "1本"),
                    Ingredient(18, "オリーブオイル", "大さじ2"),
                ],
                steps=[
                    RecipeStep(1, "パスタを塩茹でする"),
                    RecipeStep(2, "フライパンでにんにくと唐辛子を炒める"),
                    RecipeStep(3, "トマト缶を加えて煮込む"),
                    RecipeStep(4, "茹でたパスタと合わせて完成"),
                ],
            ),
            Recipe(
                recipe_id=5, recipe_name="卵チャーハン",
                food_type="中華", cook_time="15分", difficulty="簡単",
                ingredients=[
                    Ingredient(19, "ご飯", "200g"),
                    Ingredient(20, "卵", "2個"),
                    Ingredient(21, "長ねぎ", "1/4本"),
                    Ingredient(22, "醤油", "大さじ1"),
                ],
                steps=[
                    RecipeStep(1, "卵を溶いておく"),
                    RecipeStep(2, "フライパンを強火で熱しご飯を炒める"),
                    RecipeStep(3, "卵・長ねぎを加えて炒める"),
                    RecipeStep(4, "醤油で味付けして完成"),
                ],
            ),
        ]
        for r in recipes:
            self.add_recipe(r)

        self.set_recommendation(DailyRecommendation(
            recommendation_id=1,
            date=date.today(),
            recipes=[recipes[0], recipes[2], recipes[4]],
        ))
