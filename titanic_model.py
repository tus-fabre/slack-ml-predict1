#!/usr/bin/env python
# coding: utf-8
#
# [FILE] titanic_model.py
#
# [DESCRIPTION]
#  タイタニック号での生存者を予測するための関数を定義する
#
# [NOTES]
#  必要なソフトウェア
#  $ pip install xgboost
#  $ pip install pandas
#
# 参考
#  https://zenn.dev/nishimoto/articles/4f24d5be7ac463
#
import warnings
import pandas as pd
import xgboost as xgb

warnings.filterwarnings("ignore") # 警告文無視用

#
# [FUNCTION] createModel()
#
# [DESCRIPTION]
#  トレーニング用ファイルからモデルを生成する
# 
# [INPUTS]
#  train_file - トレーニング用CSVファイル
#
# [OUTPUTS]
#  決定木の勾配ブースティングアルゴリズムに基づく分類モデル
#
def createModel(train_file):
    df_train = pd.read_csv(train_file)

    # トレーニングの前処理
    df_train["Age"]  = df_train["Age"].fillna(df_train["Age"].mean())
    df_train["Fare"] = df_train["Fare"].fillna(df_train["Fare"].mean())
    df_train["Embarked"] = df_train["Embarked"].fillna(df_train["Embarked"].mode()[0])
    df_train.drop(["Name", "Ticket", "Cabin"], axis=1, inplace=True)
    df_train["Sex"] = df_train["Sex"].replace({"male": 0, "female": 1})
    df_train = pd.get_dummies(df_train)

    # 説明変数、目的変数への分割
    train_y = df_train["Survived"]
    train_x = df_train.drop("Survived", axis=1)

    # 機械学習アルゴリズムの宣言と学習
    model = xgb.XGBClassifier()
    model.fit(train_x, train_y)
    
    return model

#
# [FUNCTION] predictSurvivors()
#
# [DESCRIPTION]
#  テストデータをトレーニングモデルから結果を予測する
# 
# [INPUTS]
#  model - createModel()の返り値（分類モデル）
#  test_file - 予測するCSVファイル
#  result_file - 予測結果を保存するファイル
#
# [OUTPUTS]
#
def predictSurvivors(model, test_file, result_file):
    df_test  = pd.read_csv(test_file)

    # testの前処理
    df_test["Age"] = df_test["Age"].fillna(df_test["Age"].mean())
    df_test["Fare"] = df_test["Fare"].fillna(df_test["Fare"].mean())
    df_test["Embarked"] = df_test["Embarked"].fillna(df_test["Embarked"].mode()[0])
    df_test.drop(["Name", "Ticket", "Cabin"], axis=1, inplace=True)
    df_test["Sex"] = df_test["Sex"].replace({"male": 0, "female": 1})
    df_test = pd.get_dummies(df_test)
    test_x = df_test # testにSurvived列はないのでdrop不要

    # 予測結果をファイルに保存
    result = model.predict(test_x)
    pd.DataFrame({
        "PassengerId": test_x["PassengerId"],
        "Survived": result
    }).to_csv(result_file, index=False)

#
# END OF FILE
#