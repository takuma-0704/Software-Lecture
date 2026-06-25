"""
models.py - クラス図をもとに定義したデータモデル
"""
from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Ingredient:
    ingredient_id: int
    ingredient_name: str
    amount: str = ""

    def get_ingredient_name(self) -> str:
        return self.ingredient_name


@dataclass
class RecipeStep:
    step_no: int
    description: str

    def show_step(self) -> str:
        return f"手順{self.step_no}: {self.description}"


@dataclass
class Recipe:
    recipe_id: int
    recipe_name: str
    food_type: str
    cook_time: str = ""
    difficulty: str = ""
    ingredients: List[Ingredient] = field(default_factory=list)
    steps: List[RecipeStep] = field(default_factory=list)

    def show_recipe(self) -> str:
        return "\n".join([
            f"【{self.recipe_name}】",
            f"  ジャンル : {self.food_type}",
            f"  調理時間 : {self.cook_time}",
            f"  難易度   : {self.difficulty}",
        ])

    def show_ingredients(self) -> str:
        lines = ["  ＜使用食材＞"]
        for ing in self.ingredients:
            lines.append(f"    - {ing.ingredient_name}  {ing.amount}")
        return "\n".join(lines)

    def show_steps(self) -> str:
        lines = ["  ＜作り方＞"]
        for step in self.steps:
            lines.append(f"    {step.show_step()}")
        return "\n".join(lines)


@dataclass
class DailyRecommendation:
    recommendation_id: int
    date: date
    recipes: List[Recipe] = field(default_factory=list)

    def show_today_recipe(self) -> str:
        lines = [f"=== 今日のおすすめ ({self.date}) ==="]
        for recipe in self.recipes:
            lines.append(recipe.show_recipe())
        return "\n".join(lines)


@dataclass
class User:
    user_id: int
    name: str

    def input_ingredient(self) -> str:
        return input("使いたい食材を入力してください: ")

    def input_food_type(self) -> str:
        return input("料理ジャンルを入力してください: ")

    def view_recipe(self, recipe: Recipe) -> None:
        print(recipe.show_recipe())
        print(recipe.show_ingredients())
        print(recipe.show_steps())


@dataclass
class Admin:
    admin_id: int
    name: str

    def manage_recipe(self) -> None:
        print(f"[管理者: {self.name}] レシピ管理モードを開始します")

    def manage_ingredient(self) -> None:
        print(f"[管理者: {self.name}] 食材管理モードを開始します")

    def set_daily_recommendation(self, recommendation: DailyRecommendation) -> None:
        print(f"[管理者: {self.name}] 本日のおすすめを設定しました: {recommendation.date}")
