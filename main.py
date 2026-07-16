"""
main.py - Flaskアプリのエントリーポイント
ブラウザで http://localhost:5000 にアクセスして使う

起動方法: python main.py
"""
from flask import Flask, render_template, request, redirect, url_for
from data_recipes import RecipeDB
from recipe_service import RecipeService
from controllers import RecipeController, RecommendationController

app = Flask(__name__)

# 依存性の注入
db = RecipeDB()
service = RecipeService(db)
recipe_ctrl = RecipeController(service)
recommend_ctrl = RecommendationController(service)


# ---------------------------------------------------------------
# ホーム画面（状態遷移図: ホーム画面）
# ---------------------------------------------------------------
@app.route("/")
def home():
    # プルダウン用のおすすめ食材を取得して渡す
    featured = db.get_featured_ingredients()
    return render_template("home.html", featured_ingredients=featured)


# ---------------------------------------------------------------
# レシピ検索（シーケンス図①: 検索フロー）
# ---------------------------------------------------------------
@app.route("/search")
def search():
    ingredient = request.args.get("ingredient", "").strip()
    food_type = request.args.get("food_type", "").strip()
    recipe_name = request.args.get("recipe_name", "").strip()

    # 状態遷移: 食材入力中 → 検索中 → 料理一覧表示 or 検索失敗
    recipes = recipe_ctrl.search_recipes(ingredient, food_type, recipe_name)
    no_results = len(recipes) == 0

    return render_template(
        "results.html",
        recipes=recipes,
        ingredient=ingredient,
        food_type=food_type,
        recipe_name=recipe_name,
        no_results=no_results,
    )


# ---------------------------------------------------------------
# レシピ詳細（シーケンス図①: step10〜16）
# ---------------------------------------------------------------
@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipe = recipe_ctrl.get_recipe(recipe_id)
    if recipe is None:
        return redirect(url_for("home"))

    # ユースケース図: 追加食材を見る / 簡単なレシピを見る
    ingredients = recipe_ctrl.get_additional_ingredients(recipe_id)
    back = request.args.get("back", "search")

    return render_template(
        "recipe.html",
        recipe=recipe,
        ingredients=ingredients,
        back=back,
    )


# ---------------------------------------------------------------
# 今日のおすすめ（おすすめシーケンス図）
# ---------------------------------------------------------------
@app.route("/recommend")
def recommend():
    rec = recommend_ctrl.get_recommendation()
    return render_template("recommend.html", rec=rec)

# ---------------------------------------------------------------
# レシピを追加（自分でレシピを投稿する機能）
# ---------------------------------------------------------------
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        new_recipe = recipe_ctrl.add_recipe(request.form)
        # 追加が終わったら、そのレシピの詳細ページへ遷移
        return redirect(url_for("recipe_detail", recipe_id=new_recipe.recipe_id))

    return render_template("add_recipe.html")


# ---------------------------------------------------------------
# 食材一覧ページ（★ここに新しく左寄せで追加します）
# ---------------------------------------------------------------
@app.route("/ingredients")
def ingredients_list():
    all_ingredients = db.get_all_unique_ingredients()
    return render_template("ingredients.html", ingredients=all_ingredients)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)