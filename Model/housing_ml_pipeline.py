#!/usr/bin/env python3
"""
Housing Price Prediction ML Pipeline

Este script contiene el pipeline completo de machine learning para predecir
precios de viviendas basado en el dataset de Ames Housing.

Autor: Tu equipo
Fecha: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_score, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.inspection import permutation_importance
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
import joblib
import warnings
from scipy.stats import uniform, randint
warnings.filterwarnings('ignore')


def safe_handle_nans(data):
    """
    Maneja valores NaN de forma segura, solo para datos numéricos.
    
    Args:
        data: Array o DataFrame a procesar
        
    Returns:
        Array o DataFrame sin NaN (solo si es numérico)
    """
    # Si no es un array de numpy, devolver tal como está
    if not hasattr(data, 'dtype'):
        return data
    
    # Solo procesar si es claramente numérico
    if data.dtype in [np.float32, np.float64, np.int32, np.int64]:
        try:
            if np.isnan(data).any():
                return np.nan_to_num(data, nan=0.0)
        except (TypeError, ValueError):
            pass
    elif data.dtype == 'object':
        # Para object arrays, intentar convertir a float solo las columnas numéricas
        try:
            # Si es un array 2D, procesar columna por columna
            if len(data.shape) > 1:
                for i in range(data.shape[1]):
                    try:
                        col_float = data[:, i].astype(float)
                        if np.isnan(col_float).any():
                            data[:, i] = np.nan_to_num(col_float, nan=0.0)
                    except (TypeError, ValueError):
                        # Si no se puede convertir, dejar tal como está
                        pass
        except (TypeError, ValueError):
            pass
    
    return data


def drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina columnas no útiles para el modelo.
    Aplica lo mismo a train y test para mantener consistencia.
    
    Args:
        df: DataFrame a limpiar
        
    Returns:
        DataFrame con columnas eliminadas
    """
    cols_to_drop = [
        "Id",
        "Utilities",
        "Condition2",
        "LandSlope",
        "LowQualFinSF",
        "MiscVal",
        "Street",
        "RoofMatl",
        "Heating"
    ]
    df_out = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    return df_out


def limpiar_df(df):
    """
    Limpia el DataFrame aplicando reglas específicas para manejar valores NaN.
    
    Args:
        df: DataFrame a limpiar
        
    Returns:
        DataFrame limpio
    """
    out = df.copy()

    # Reglas de limpieza
    cols_moda = [
        "MSZoning",
        "BsmtQual","BsmtCond","BsmtExposure",
        "BsmtFinType1","BsmtFinType2",
        "FireplaceQu","GarageType",
        "GarageYrBlt",  # numérica pero por moda 
        "GarageFinish","GarageQual","GarageCond",
    ]
    cols_media = ["LotFrontage", "MasVnrArea"]
    cols_drop  = ["MasVnrType", "MiscFeature","PoolQC","Alley"]

    # Mantener solo las que EXISTEN (evita KeyError)
    def existen(cols): 
        return [c for c in cols if c in out.columns]

    cols_moda_ok  = existen(cols_moda)
    cols_media_ok = existen(cols_media)
    cols_drop_ok  = existen(cols_drop)

    # Imputación por MODA (categóricas + GarageYrBlt)
    if cols_moda_ok:
        imp_mode = SimpleImputer(strategy="most_frequent")
        out[cols_moda_ok] = imp_mode.fit_transform(out[cols_moda_ok])

    # Asegurar que las de MEDIA sean numéricas
    if cols_media_ok:
        out[cols_media_ok] = out[cols_media_ok].apply(
            pd.to_numeric, errors="coerce"
        )
        imp_mean = SimpleImputer(strategy="mean")
        out[cols_media_ok] = imp_mean.fit_transform(out[cols_media_ok])

    # Eliminar columnas con demasiados NaN
    if cols_drop_ok:
        out = out.drop(columns=cols_drop_ok)

    return out


def impute_missing(df):
    """
    Imputa valores faltantes usando estrategias apropiadas.
    
    Args:
        df: DataFrame con valores faltantes
        
    Returns:
        DataFrame sin valores faltantes
    """
    df_out = df.copy()

    # Numéricas → media
    num_cols = df_out.select_dtypes(include=["int64","float64"]).columns
    imp_mean = SimpleImputer(strategy="mean")
    df_out[num_cols] = imp_mean.fit_transform(df_out[num_cols])

    # Categóricas → moda
    cat_cols = df_out.select_dtypes(include=["object","category"]).columns
    imp_mode = SimpleImputer(strategy="most_frequent")
    df_out[cat_cols] = imp_mode.fit_transform(df_out[cat_cols])

    return df_out


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Añade características de ingeniería derivadas útiles para modelos.
    
    Args:
        df: DataFrame original
        
    Returns:
        DataFrame con nuevas características
    """
    out = df.copy()

    # Helpers
    def safe_div(num, den):
        den = den.replace(0, np.nan) if isinstance(den, pd.Series) else (np.nan if den == 0 else den)
        return num / den

    # Edades / tiempos
    out["HouseAge"]     = out["YrSold"] - out["YearBuilt"]
    out["RemodAge"]     = out["YrSold"] - out["YearRemodAdd"]
    out["AgeAtRemodel"] = out["YearRemodAdd"] - out["YearBuilt"]

    # A veces GarageYrBlt puede estar vacío o dar negativo: lo limpiamos
    out["GarageAge"] = out["YrSold"] - out["GarageYrBlt"]
    out.loc[out["GarageYrBlt"].isna(), "GarageAge"] = np.nan
    out.loc[out["GarageAge"] < 0, "GarageAge"] = np.nan

    # Superficies
    out["BsmtFinSF"]   = out["BsmtFinSF1"].fillna(0) + out["BsmtFinSF2"].fillna(0)
    out["TotalSF"]     = out["1stFlrSF"].fillna(0) + out["2ndFlrSF"].fillna(0) + out["TotalBsmtSF"].fillna(0)
    out["TotalPorchSF"]= out["OpenPorchSF"].fillna(0) + out["EnclosedPorch"].fillna(0) \
                       + out["3SsnPorch"].fillna(0) + out["WoodDeckSF"].fillna(0)

    # Baños / habitaciones
    out["TotalBath"]   = (
        out["FullBath"].fillna(0) + 0.5*out["HalfBath"].fillna(0)
        + out["BsmtFullBath"].fillna(0) + 0.5*out["BsmtHalfBath"].fillna(0)
    )
    out["RoomsPlusBathEq"] = out["TotRmsAbvGrd"].fillna(0) + out["FullBath"].fillna(0) + 0.5*out["HalfBath"].fillna(0)

    # Lote / proporciones
    out["LotFrontageRatio"] = safe_div(out["LotFrontage"], out["LotArea"])
    out["LotAreaPerRoom"]   = safe_div(out["LotArea"], out["TotRmsAbvGrd"].replace(0, np.nan))

    # Garage
    out["GarageScore"] = out["GarageCars"].fillna(0) * out["GarageArea"].fillna(0)

    # Indicadores binarios útiles
    out["HasPool"]       = (out["PoolArea"].fillna(0) > 0).astype(int)
    out["HasFireplace"]  = (out["Fireplaces"].fillna(0) > 0).astype(int)
    out["Remodeled"]     = (out["YearRemodAdd"] != out["YearBuilt"]).astype(int)
    out["Has2ndFlr"]     = (out["2ndFlrSF"].fillna(0) > 0).astype(int)
    out["HasBsmt"]       = (out["TotalBsmtSF"].fillna(0) > 0).astype(int)
    out["HasGarage"]     = (out["GarageArea"].fillna(0) > 0).astype(int)
    out["HasFence"]      = (~out["Fence"].isna()).astype(int)

    # Temporada de venta
    season_map = {
        12: "Invierno", 1: "Invierno", 2: "Invierno",
        3: "Primavera", 4: "Primavera", 5: "Primavera",
        6: "Verano", 7: "Verano", 8: "Verano",
        9: "Otoño", 10: "Otoño", 11: "Otoño"
    }
    out["SeasonSold"] = out["MoSold"].map(season_map)

    return out


def build_group_slices(preprocessor, X_train, categoricas):
    """
    Construye grupos de slices para análisis de importancia de características.
    
    Args:
        preprocessor: ColumnTransformer usado
        X_train: DataFrame de entrenamiento
        categoricas: Lista de columnas categóricas
        
    Returns:
        Tupla con grupos, columnas numéricas y total esperado
    """
    ohe = preprocessor.named_transformers_['cat']
    num_cols = [c for c in X_train.columns if c not in categoricas]
    groups = {}

    ptr = 0
    drop_adjust = 1 if ohe.drop is not None else 0
    for col, cats in zip(categoricas, ohe.categories_):
        k = max(0, len(cats) - drop_adjust)
        if k > 0:
            groups[col] = np.arange(ptr, ptr + k)
        else:
            groups[col] = np.array([], dtype=int)
        ptr += k

    # numéricas: van después del bloque OHE
    for i, col in enumerate(num_cols):
        groups[col] = np.array([ptr + i])

    total_expected = ptr + len(num_cols)
    return groups, num_cols, total_expected


def get_feature_names_safe(preprocessor, X_train, categoricas):
    """
    Obtiene nombres de características de forma segura.
    
    Args:
        preprocessor: ColumnTransformer usado
        X_train: DataFrame de entrenamiento
        categoricas: Lista de columnas categóricas
        
    Returns:
        Array con nombres de características
    """
    try:
        return np.array(preprocessor.get_feature_names_out())
    except Exception:
        ohe_inside = preprocessor.named_transformers_['cat']
        ohe_names = ohe_inside.get_feature_names_out(categoricas)
        num_cols = [c for c in X_train.columns if c not in categoricas]
        names = np.r_[ [f"cat__{n}" for n in ohe_names], num_cols ]
        return np.array(names, dtype=object)


def grouped_permutation_importance(model, X, y, groups, n_repeats=8, random_state=42):
    """
    Calcula importancia por permutación agrupada.
    
    Args:
        model: Modelo entrenado
        X: Características
        y: Variable objetivo
        groups: Grupos de características
        n_repeats: Número de repeticiones
        random_state: Semilla aleatoria
        
    Returns:
        Diccionario con importancias
    """
    rng = np.random.RandomState(random_state)
    # baseline: -RMSE (entre más alto mejor)
    y_pred = model.predict(X)
    baseline = -np.sqrt(np.mean((y - y_pred) ** 2))

    importances = {}
    for name, idxs in groups.items():
        if len(idxs) == 0:
            importances[name] = 0.0
            continue
        drops = []
        for _ in range(n_repeats):
            perm = rng.permutation(X.shape[0])
            Xp = X.copy()
            Xp[:, idxs] = Xp[perm][:, idxs]  # permutar el BLOQUE del feature
            y_pred_p = model.predict(Xp)
            score_p = -np.sqrt(np.mean((y - y_pred_p) ** 2))
            drops.append(baseline - score_p)
        importances[name] = float(np.mean(drops))
    return importances


def train_models(train_path="data/train.csv", test_path="data/test.csv"):
    """
    Entrena múltiples modelos de machine learning.
    
    Args:
        train_path: Ruta al archivo de entrenamiento
        test_path: Ruta al archivo de prueba
        
    Returns:
        Diccionario con modelos entrenados y métricas
    """
    print("Cargando datos...")
    
    # Cargar datos
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    test_ids = test["Id"].copy()
    
    # Aplicar pipeline de limpieza
    print("Limpiando datos...")
    train = drop_columns(train)
    train = limpiar_df(train)
    train = add_engineered_features(train)
    train = impute_missing(train)
    
    test = drop_columns(test)
    test = limpiar_df(test)
    test = add_engineered_features(test)
    test = impute_missing(test)
    
    # Separar características y objetivo
    X_train = train.drop("SalePrice", axis=1)
    y_train = train["SalePrice"]
    X_test = test.copy()
    
    # Preprocesamiento
    print("Preprocesando características...")
    cat_selector = make_column_selector(dtype_include=["object", "category"])
    categoricas = cat_selector(X_train)
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), categoricas)
        ],
        remainder="passthrough"
    )
    
    # Transformar características
    X_train_trans = preprocessor.fit_transform(X_train)
    X_test_trans = preprocessor.transform(X_test)
    
    # Manejo de NaNs (solo para datos numéricos)
    X_train_trans = safe_handle_nans(X_train_trans)
    X_test_trans = safe_handle_nans(X_test_trans)
    
    models = {}
    predictions = {}
    
    # 1. Regresión Lineal
    print("Entrenando Regresión Lineal...")
    linreg = LinearRegression()
    linreg.fit(X_train_trans, y_train)
    y_pred_linreg = linreg.predict(X_test_trans)
    
    models['linear_regression'] = linreg
    predictions['linear_regression'] = y_pred_linreg
    
    # Guardar submission
    submission_linreg = pd.DataFrame({
        "Id": test_ids,
        "SalePrice": y_pred_linreg
    })
    submission_linreg.to_csv("submission_linreg.csv", index=False)
    print("Archivo submission_linreg.csv creado!")
    
    # 2. Random Forest
    print("Entrenando Random Forest...")
    rf = RandomForestRegressor(
        n_estimators=500,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train_trans, y_train)
    y_pred_rf = rf.predict(X_test_trans)
    
    models['random_forest'] = rf
    predictions['random_forest'] = y_pred_rf
    
    # Guardar submission
    submission_rf = pd.DataFrame({
        "Id": test_ids,
        "SalePrice": y_pred_rf
    })
    submission_rf.to_csv("submission_rf.csv", index=False)
    print("Archivo submission_rf.csv creado!")
    
    # 3. XGBoost
    print("Entrenando XGBoost...")
    y_train_log = np.log1p(y_train)
    
    xgb = XGBRegressor(
        n_estimators=1000,
        learning_rate=0.05,
        max_depth=3,
        subsample=0.6,
        colsample_bytree=0.8,
        reg_lambda=0.8,
        random_state=42,
        n_jobs=-1,
        tree_method="hist"
    )
    xgb.fit(X_train_trans, y_train_log)
    y_pred_xgb = np.expm1(xgb.predict(X_test_trans))
    y_pred_xgb = np.clip(y_pred_xgb, 0, None)
    
    models['xgboost'] = xgb
    predictions['xgboost'] = y_pred_xgb
    
    # Guardar submission
    submission_xgb = pd.DataFrame({
        "Id": test_ids,
        "SalePrice": y_pred_xgb
    })
    submission_xgb.to_csv("submission_xgb.csv", index=False)
    print("Archivo submission_xgb.csv creado!")
    
    # Guardar pipeline completo
    pipeline_full = Pipeline([('preprocessor', preprocessor), ('model', xgb)])
    joblib.dump(pipeline_full, 'xgb_full_pipeline.pkl')
    print("Pipeline completo guardado: xgb_full_pipeline.pkl")
    
    return {
        'models': models,
        'predictions': predictions,
        'preprocessor': preprocessor,
        'X_train': X_train,
        'y_train': y_train,
        'categoricas': categoricas
    }


def analyze_feature_importance(results):
    """
    Analiza la importancia de las características.
    
    Args:
        results: Resultados del entrenamiento
        
    Returns:
        DataFrames con análisis de importancia
    """
    print("Analizando importancia de características...")
    
    preprocessor = results['preprocessor']
    X_train = results['X_train']
    y_train = results['y_train']
    categoricas = results['categoricas']
    xgb = results['models']['xgboost']
    
    # Transformar datos
    X_train_trans = preprocessor.transform(X_train)
    
    # Construir grupos
    groups, num_cols, total_expected = build_group_slices(preprocessor, X_train, categoricas)
    
    # Análisis de dimensionalidad
    ohe = preprocessor.named_transformers_['cat']
    drop_adjust = 1 if ohe.drop is not None else 0
    
    dim_rows = []
    ptr = 0
    for col, cats in zip(categoricas, ohe.categories_):
        k = max(0, len(cats) - drop_adjust)
        dim_rows.append((col, len(cats), k))
        ptr += k
    for col in num_cols:
        dim_rows.append((col, np.nan, 1))
    
    dim_df = pd.DataFrame(dim_rows, columns=["col_original", "categorias_observadas", "cols_en_transform"])
    dim_df = dim_df.sort_values(["categorias_observadas", "cols_en_transform"], ascending=[False, False])
    
    print("\n== Resumen de dimensionalidad (por columna original) ==")
    print(dim_df)
    
    # Importancia XGBoost (gain) agregada
    feature_names = get_feature_names_safe(preprocessor, X_train, categoricas)
    booster = xgb.get_booster()
    scores_gain = booster.get_score(importance_type='gain')
    imp_arr_gain = np.array([scores_gain.get(f"f{i}", 0.0) for i in range(X_train_trans.shape[1])], dtype=float)
    
    # Agregar sumando el bloque de dummies por cada columna original
    agg_gain = []
    for col, idxs in groups.items():
        agg_gain.append((col, float(imp_arr_gain[idxs].sum())))
    agg_gain_df = (
        pd.DataFrame(agg_gain, columns=["feature", "importance_gain"])
        .sort_values("importance_gain", ascending=False)
        .reset_index(drop=True)
    )
    
    # Importancia post-OHE por feature individual
    post_ohe_df = (
        pd.DataFrame({"feature_trans": feature_names, "importance_gain": imp_arr_gain})
        .sort_values("importance_gain", ascending=False)
        .reset_index(drop=True)
    )
    
    # Permutation Importance AGRUPADA
    group_perm = grouped_permutation_importance(xgb, X_train_trans, y_train, groups, n_repeats=8, random_state=42)
    perm_df = (
        pd.DataFrame(list(group_perm.items()), columns=["feature", "perm_importance_rmse_drop"])
        .sort_values("perm_importance_rmse_drop", ascending=False)
        .reset_index(drop=True)
    )
    
    # Guardar rankings
    dim_df.to_csv("resumen_dimensionalidad.csv", index=False)
    post_ohe_df.to_csv("importancias_post_ohe_gain.csv", index=False)
    agg_gain_df.to_csv("importancias_agregadas_gain.csv", index=False)
    perm_df.to_csv("importancias_agregadas_permutation.csv", index=False)
    
    print("\nTop 15 (agregado por columna original - gain):")
    print(agg_gain_df.head(20))
    print("\nTop 15 (agregado por columna original - permutation):")
    print(perm_df.head(20))
    
    return {
        'dimensionality': dim_df,
        'aggregated_gain': agg_gain_df,
        'post_ohe': post_ohe_df,
        'permutation': perm_df
    }


def train_top20_model(results, importance_analysis, test_path="data/test.csv"):
    """
    Entrena modelo con las top 20 características más importantes.
    
    Args:
        results: Resultados del entrenamiento completo
        importance_analysis: Análisis de importancia
        test_path: Ruta al archivo de prueba
        
    Returns:
        Modelo entrenado con top 20 características
    """
    print("Entrenando modelo con top 20 características...")
    
    # Obtener top 20 características
    top_k = 20
    top_features = importance_analysis['permutation'].nlargest(top_k, 'perm_importance_rmse_drop')['feature'].tolist()
    print("Top-20 columnas originales (principal):")
    print(top_features)
    
    X_train = results['X_train']
    y_train = results['y_train']
    categoricas = results['categoricas']
    
    # Separar cuáles de esas 20 son categóricas vs numéricas
    top_cats = [c for c in top_features if c in categoricas]
    top_nums = [c for c in top_features if c not in categoricas]
    
    # Preprocesador limitado a las Top-20
    transformers_top = []
    if len(top_cats) > 0:
        ohe_top = OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False)
        transformers_top.append(("cat", ohe_top, top_cats))
    if len(top_nums) > 0:
        transformers_top.append(("num", "passthrough", top_nums))
    
    preprocessor_top = ColumnTransformer(
        transformers=transformers_top,
        remainder="drop"
    )
    
    # Transformar train/test con el nuevo preprocesador
    X_train_top = preprocessor_top.fit_transform(X_train)
    
    # Manejo defensivo de NaNs (solo para datos numéricos)
    X_train_top = safe_handle_nans(X_train_top)
    
    # Modelo XGBoost con top 20
    xgb_top = XGBRegressor(
        n_estimators=1000,
        learning_rate=0.02,
        max_depth=2,
        subsample=0.6,
        colsample_bytree=0.7,
        reg_lambda=0.6,
        random_state=10,
        n_jobs=-1,
        tree_method="hist"
    )
    
    # CV para validar performance
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_rmse = -cross_val_score(
        xgb_top, X_train_top, y_train,
        scoring="neg_root_mean_squared_error",
        cv=cv
    ).mean()
    print(f"CV RMSE (log1p target) con Top-20: {cv_rmse:.5f}")
    
    # Entrenar modelo
    xgb_top.fit(X_train_top, y_train)
    
    # Procesar datos de test
    test = pd.read_csv(test_path)
    test_ids = test["Id"].copy()
    test = drop_columns(test)
    test = limpiar_df(test)
    test = add_engineered_features(test)
    test = impute_missing(test)
    
    X_test_top = preprocessor_top.transform(test)
    X_test_top = safe_handle_nans(X_test_top)
    
    # Predecir
    y_pred_test_top = np.expm1(xgb_top.predict(X_test_top))
    y_pred_test_top = np.clip(y_pred_test_top, 0, None)
    
    # Guardar submission
    submission_top = pd.DataFrame({
        "Id": test_ids,
        "SalePrice": y_pred_test_top
    })
    submission_top.to_csv("submission_xgb_top20.csv", index=False)
    print("Archivo guardado: submission_xgb_top20.csv")
    
    # Guardar pipeline top-20
    pipeline_top = Pipeline([('preprocessor_top', preprocessor_top), ('model', xgb_top)])
    joblib.dump(pipeline_top, 'xgb_top20_pipeline.pkl')
    print("Pipeline top-20 guardado: xgb_top20_pipeline.pkl")
    
    return xgb_top, preprocessor_top


def random_search_optimization(X_train, y_train, model_type="xgboost", n_iter=50, cv=5, random_state=42):
    """
    Realiza optimización de hiperparámetros usando Random Search.
    
    Args:
        X_train: Características de entrenamiento
        y_train: Variable objetivo
        model_type: Tipo de modelo ("xgboost", "random_forest", "linear")
        n_iter: Número de iteraciones para Random Search
        cv: Número de folds para cross-validation
        random_state: Semilla aleatoria
        
    Returns:
        Mejor modelo encontrado y resultados de búsqueda
    """
    print(f"\n=== RANDOM SEARCH OPTIMIZATION - {model_type.upper()} ===")
    print(f"Realizando {n_iter} iteraciones con {cv}-fold CV...")
    
    # Definir distribuciones de hiperparámetros según el modelo
    if model_type.lower() == "xgboost":
        param_distributions = {
            'n_estimators': randint(100, 2000),
            'learning_rate': uniform(0.01, 0.3),
            'max_depth': randint(2, 10),
            'subsample': uniform(0.6, 0.4),
            'colsample_bytree': uniform(0.6, 0.4),
            'reg_lambda': uniform(0.1, 2.0),
            'reg_alpha': uniform(0.0, 1.0),
            'min_child_weight': randint(1, 10)
        }
        base_model = XGBRegressor(
            random_state=random_state,
            n_jobs=-1,
            tree_method="hist"
        )
        
    elif model_type.lower() == "random_forest":
        param_distributions = {
            'n_estimators': randint(50, 1000),
            'max_depth': [None] + list(range(5, 50)),
            'min_samples_split': randint(2, 20),
            'min_samples_leaf': randint(1, 10),
            'max_features': ['sqrt', 'log2', None] + list(range(1, min(20, X_train.shape[1]))),
            'bootstrap': [True, False]
        }
        base_model = RandomForestRegressor(
            random_state=random_state,
            n_jobs=-1
        )
        
    elif model_type.lower() == "linear":
        param_distributions = {
            'fit_intercept': [True, False],
            'normalize': [True, False]
        }
        base_model = LinearRegression()
        
    else:
        raise ValueError(f"Modelo no soportado: {model_type}. Usa 'xgboost', 'random_forest', o 'linear'")
    
    # Configurar Random Search
    random_search = RandomizedSearchCV(
        estimator=base_model,
        param_distributions=param_distributions,
        n_iter=n_iter,
        cv=cv,
        scoring='neg_root_mean_squared_error',
        random_state=random_state,
        n_jobs=-1,
        verbose=1
    )
    
    # Ejecutar búsqueda
    print("Iniciando búsqueda de hiperparámetros...")
    random_search.fit(X_train, y_train)
    
    # Mostrar resultados
    print(f"\n✅ Búsqueda completada!")
    print(f"Mejor score (RMSE): {-random_search.best_score_:.4f}")
    print(f"Mejores parámetros:")
    for param, value in random_search.best_params_.items():
        print(f"  {param}: {value}")
    
    # Mostrar top 5 configuraciones
    results_df = pd.DataFrame(random_search.cv_results_)
    top_5 = results_df.nlargest(5, 'mean_test_score')[['mean_test_score', 'std_test_score', 'params']]
    print(f"\nTop 5 configuraciones:")
    for i, (idx, row) in enumerate(top_5.iterrows(), 1):
        print(f"{i}. Score: {-row['mean_test_score']:.4f} (+/- {row['std_test_score']*2:.4f})")
        print(f"   Parámetros: {row['params']}")
    
    return random_search.best_estimator_, random_search


def train_models_with_optimization(train_path="data/train.csv", test_path="data/test.csv", 
                                 optimize_models=True, n_iter=50, cv=5):
    """
    Entrena modelos con optimización de hiperparámetros usando Random Search.
    
    Args:
        train_path: Ruta al archivo de entrenamiento
        test_path: Ruta al archivo de prueba
        optimize_models: Si True, usa Random Search para optimizar hiperparámetros
        n_iter: Número de iteraciones para Random Search
        cv: Número de folds para cross-validation
        
    Returns:
        Diccionario con modelos optimizados y predicciones
    """
    print("=== ENTRENAMIENTO CON OPTIMIZACIÓN DE HIPERPARÁMETROS ===")
    
    # Cargar y procesar datos
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    test_ids = test["Id"].copy()
    
    # Aplicar pipeline de limpieza
    print("Procesando datos...")
    train = drop_columns(train)
    train = limpiar_df(train)
    train = add_engineered_features(train)
    train = impute_missing(train)
    
    test = drop_columns(test)
    test = limpiar_df(test)
    test = add_engineered_features(test)
    test = impute_missing(test)
    
    # Separar características y objetivo
    X_train = train.drop("SalePrice", axis=1)
    y_train = train["SalePrice"]
    X_test = test.copy()
    
    # Preprocesamiento
    print("Preprocesando características...")
    cat_selector = make_column_selector(dtype_include=["object", "category"])
    categoricas = cat_selector(X_train)
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), categoricas)
        ],
        remainder="passthrough"
    )
    
    # Transformar características
    X_train_trans = preprocessor.fit_transform(X_train)
    X_test_trans = preprocessor.transform(X_test)
    
    # Manejo de NaNs (solo para datos numéricos)
    X_train_trans = safe_handle_nans(X_train_trans)
    X_test_trans = safe_handle_nans(X_test_trans)
    
    models = {}
    predictions = {}
    search_results = {}
    
    if optimize_models:
        # 1. Optimizar XGBoost
        print("\n" + "="*50)
        best_xgb, xgb_search = random_search_optimization(
            X_train_trans, y_train, "xgboost", n_iter=n_iter, cv=cv
        )
        models['xgboost_optimized'] = best_xgb
        search_results['xgboost'] = xgb_search
        
        # Predecir con XGBoost optimizado
        y_pred_xgb = best_xgb.predict(X_test_trans)
        y_pred_xgb = np.clip(y_pred_xgb, 0, None)
        predictions['xgboost_optimized'] = y_pred_xgb
        
        # Guardar submission
        submission_xgb = pd.DataFrame({
            "Id": test_ids,
            "SalePrice": y_pred_xgb
        })
        submission_xgb.to_csv("submission_xgb_optimized.csv", index=False)
        print("Archivo submission_xgb_optimized.csv creado!")
        
        # 2. Optimizar Random Forest
        print("\n" + "="*50)
        best_rf, rf_search = random_search_optimization(
            X_train_trans, y_train, "random_forest", n_iter=n_iter, cv=cv
        )
        models['random_forest_optimized'] = best_rf
        search_results['random_forest'] = rf_search
        
        # Predecir con Random Forest optimizado
        y_pred_rf = best_rf.predict(X_test_trans)
        predictions['random_forest_optimized'] = y_pred_rf
        
        # Guardar submission
        submission_rf = pd.DataFrame({
            "Id": test_ids,
            "SalePrice": y_pred_rf
        })
        submission_rf.to_csv("submission_rf_optimized.csv", index=False)
        print("Archivo submission_rf_optimized.csv creado!")
        
        # 3. Optimizar Linear Regression
        print("\n" + "="*50)
        best_lr, lr_search = random_search_optimization(
            X_train_trans, y_train, "linear", n_iter=n_iter, cv=cv
        )
        models['linear_regression_optimized'] = best_lr
        search_results['linear_regression'] = lr_search
        
        # Predecir con Linear Regression optimizado
        y_pred_lr = best_lr.predict(X_test_trans)
        predictions['linear_regression_optimized'] = y_pred_lr
        
        # Guardar submission
        submission_lr = pd.DataFrame({
            "Id": test_ids,
            "SalePrice": y_pred_lr
        })
        submission_lr.to_csv("submission_lr_optimized.csv", index=False)
        print("Archivo submission_lr_optimized.csv creado!")
        
    else:
        # Entrenar modelos con parámetros por defecto
        print("Entrenando modelos con parámetros por defecto...")
        results = train_models(train_path, test_path)
        models = results['models']
        predictions = results['predictions']
    
    # Guardar modelos optimizados
    if optimize_models:
        joblib.dump(models, 'optimized_models.pkl')
        print("Modelos optimizados guardados: optimized_models.pkl")
        
        # Guardar resultados de búsqueda
        joblib.dump(search_results, 'search_results.pkl')
        print("Resultados de búsqueda guardados: search_results.pkl")
    
    return {
        'models': models,
        'predictions': predictions,
        'search_results': search_results if optimize_models else None,
        'preprocessor': preprocessor,
        'X_train': X_train,
        'y_train': y_train,
        'categoricas': categoricas
    }


def evaluate_models_locally(train_path="data/train.csv"):
    """
    Evalúa los modelos localmente usando train/test split.
    
    Args:
        train_path: Ruta al archivo de entrenamiento
    """
    print("Evaluando modelos localmente...")
    
    # Cargar y limpiar datos
    train = pd.read_csv(train_path)
    train = drop_columns(train)
    train = limpiar_df(train)
    train = add_engineered_features(train)
    train = impute_missing(train)
    
    # Separar características y objetivo
    X = train.drop("SalePrice", axis=1)
    y = train["SalePrice"]
    
    # Split local (80/20)
    X_train_local, X_valid, y_train_local, y_valid = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Preprocesador
    cat_selector = make_column_selector(dtype_include=["object", "category"])
    categoricas = cat_selector(X_train_local)
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), categoricas)
        ],
        remainder="passthrough"
    )
    
    # Transformar datos
    X_train_local_trans = preprocessor.fit_transform(X_train_local)
    X_valid_trans = preprocessor.transform(X_valid)
    
    # Modelo 1: LinearRegression
    linreg = LinearRegression()
    linreg.fit(X_train_local_trans, y_train_local)
    y_pred_valid = linreg.predict(X_valid_trans)
    
    rmse_lin = np.sqrt(mean_squared_error(y_valid, y_pred_valid))
    r2_lin = r2_score(y_valid, y_pred_valid)
    print("LinearRegression - RMSE:", rmse_lin, " R²:", r2_lin)
    
    # Modelo 2: RandomForest
    rf = RandomForestRegressor(
        n_estimators=500, random_state=42, n_jobs=-1
    )
    rf.fit(X_train_local_trans, y_train_local)
    y_pred_valid_rf = rf.predict(X_valid_trans)
    
    rmse_rf = np.sqrt(mean_squared_error(y_valid, y_pred_valid_rf))
    r2_rf = r2_score(y_valid, y_pred_valid_rf)
    print("RandomForest - RMSE:", rmse_rf, " R²:", r2_rf)


def generate_visualizations(df, df_limpio, df_limpio_sin_NaN):
    """
    Genera todas las visualizaciones del análisis exploratorio.
    
    Args:
        df: DataFrame original
        df_limpio: DataFrame después de eliminar columnas
        df_limpio_sin_NaN: DataFrame después de limpiar NaN
    """
    print("Generando visualizaciones...")
    
    # 1. Gráfico de varianza de columnas eliminadas
    cols_dropeadas = ["Id","Alley","Utilities","Condition2","3SsnPorch","PoolArea","PoolQC","LandSlope"]
    num_cols_dropeadas = df[cols_dropeadas].select_dtypes(include=["int64","float64"]).columns
    varianzas_drop = df[num_cols_dropeadas].var().sort_values()
    
    plt.figure(figsize=(6, 4))
    varianzas_drop.plot(kind="barh", color="tomato", edgecolor="black")
    plt.title("Varianza de columnas numéricas eliminadas", fontsize=14)
    plt.xlabel("Varianza", fontsize=12)
    plt.ylabel("Columnas", fontsize=12)
    plt.tight_layout()
    plt.savefig("varianza_columnas_eliminadas.png", dpi=160, bbox_inches='tight')
    plt.show()
    
    # 2. Gráficos de columnas categóricas eliminadas
    categoricas = ["Alley","Utilities","Condition2","PoolQC","LandSlope"]
    fig, axes = plt.subplots(nrows=1, ncols=len(categoricas), figsize=(16,4))
    
    for i, col in enumerate(categoricas):
        freqs = df[col].value_counts(normalize=True).head(3)
        axes[i].bar(freqs.index, freqs.values, color="skyblue", edgecolor="black")
        axes[i].set_title(col)
        axes[i].set_ylim(0, 1)
        axes[i].tick_params(axis='x', rotation=45)
        axes[i].set_ylabel("Proporción")
    
    plt.suptitle("Top 3 categorías más frecuentes en columnas eliminadas", fontsize=14)
    plt.tight_layout()
    plt.savefig("categorias_eliminadas.png", dpi=160, bbox_inches='tight')
    plt.show()
    
    # 3. Histogramas de columnas numéricas (original)
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns
    df[num_cols].hist(figsize=(50, 25), bins=100, edgecolor="black")
    plt.suptitle("Distribución de columnas numéricas (original)", fontsize=16)
    plt.savefig("histogramas_numericas_original.png", dpi=160, bbox_inches='tight')
    plt.show()
    
    # 4. Histogramas de columnas categóricas (original)
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    fig, axes = plt.subplots(nrows=len(cat_cols)//3 + 1, ncols=3, figsize=(18, 4*len(cat_cols)//3))
    
    for i, col in enumerate(cat_cols):
        ax = axes.flatten()[i]
        freqs = df[col].value_counts(normalize=True)
        sns.barplot(x=freqs.index, y=freqs.values, ax=ax, palette="Set2")
        ax.set_title(f"Distribución de {col}")
        ax.set_ylabel("Proporción")
        ax.set_xlabel("")
        ax.tick_params(axis="x", rotation=45)
    
    plt.tight_layout()
    plt.savefig("distribucion_categoricas_original.png", dpi=160, bbox_inches='tight')
    plt.show()
    
    # 5. Histogramas después de limpieza
    num_cols_limpio = df_limpio_sin_NaN.select_dtypes(include=["int64", "float64"]).columns
    df_limpio_sin_NaN[num_cols_limpio].hist(figsize=(50, 25), bins=500, edgecolor="black")
    plt.suptitle("Distribución de columnas numéricas (después de limpieza)", fontsize=16)
    plt.savefig("histogramas_numericas_limpio.png", dpi=160, bbox_inches='tight')
    plt.show()
    
    # 6. Distribución categóricas después de limpieza
    cat_cols_limpio = df_limpio_sin_NaN.select_dtypes(include=["object", "category"]).columns
    fig, axes = plt.subplots(nrows=len(cat_cols_limpio)//3 + 1, ncols=3, figsize=(18, 4*len(cat_cols_limpio)//3))
    
    for i, col in enumerate(cat_cols_limpio):
        ax = axes.flatten()[i]
        freqs = df_limpio_sin_NaN[col].value_counts(normalize=True)
        sns.barplot(x=freqs.index, y=freqs.values, ax=ax, palette="Set2")
        ax.set_title(f"Distribución de {col}")
        ax.set_ylabel("Proporción")
        ax.set_xlabel("")
        ax.tick_params(axis="x", rotation=45)
    
    plt.tight_layout()
    plt.savefig("distribucion_categoricas_limpio.png", dpi=160, bbox_inches='tight')
    plt.show()


def analyze_unique_values(df, title="Análisis de Valores Únicos"):
    """
    Analiza y muestra valores únicos por columna de forma detallada.
    
    Args:
        df: DataFrame a analizar
        title: Título para el análisis
    """
    print(f"\n=== {title} ===")
    
    # Conteo de valores únicos por columna
    unique_counts = df.nunique()
    
    # Convertir a DataFrame para mejor visualización
    resumen = pd.DataFrame({
        "columna": unique_counts.index,
        "valores_unicos": unique_counts.values
    })
    
    # Mostrar todas las filas
    pd.set_option("display.max_rows", None)
    print("Conteo de valores únicos por columna:")
    print(resumen)
    
    # Estadísticas generales
    total_columns = len(df.columns)
    columns_single_value = (unique_counts == 1).sum()
    columns_low_cardinality = (unique_counts <= 5).sum()
    columns_high_cardinality = (unique_counts > 100).sum()
    
    print(f"\nEstadísticas generales:")
    print(f"- Total de columnas: {total_columns}")
    print(f"- Columnas con un solo valor: {columns_single_value}")
    print(f"- Columnas con baja cardinalidad (≤5 valores): {columns_low_cardinality}")
    print(f"- Columnas con alta cardinalidad (>100 valores): {columns_high_cardinality}")
    
    # Top 10 columnas con más valores únicos
    print("\nTop 10 columnas con más valores únicos:")
    top_unique = unique_counts.sort_values(ascending=False).head(10)
    print(top_unique)
    
    # Columnas con menos valores únicos (potenciales categóricas)
    print("\nColumnas con menos valores únicos (potenciales categóricas):")
    low_unique = unique_counts.sort_values(ascending=True).head(10)
    print(low_unique)
    
    return resumen, top_unique, low_unique


def analyze_collinearity(df, target_col="SalePrice", threshold=0.8, save_plots=True):
    """
    Analiza la colinealidad entre variables numéricas.
    
    Args:
        df: DataFrame con los datos
        target_col: Nombre de la columna objetivo
        threshold: Umbral de correlación para considerar colinealidad alta
        save_plots: Si guardar los gráficos generados
        
    Returns:
        dict: Diccionario con resultados del análisis
    """
    print(f"\n=== ANÁLISIS DE COLINEALIDAD ===")
    
    # Seleccionar solo variables numéricas
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if target_col in numeric_cols:
        numeric_cols.remove(target_col)
    
    print(f"Analizando {len(numeric_cols)} variables numéricas...")
    
    # Calcular matriz de correlación
    corr_matrix = df[numeric_cols].corr()
    
    # Encontrar pares altamente correlacionados
    high_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) >= threshold:
                high_corr_pairs.append({
                    'var1': corr_matrix.columns[i],
                    'var2': corr_matrix.columns[j],
                    'correlation': corr_val,
                    'abs_correlation': abs(corr_val)
                })
    
    # Ordenar por correlación absoluta
    high_corr_pairs = sorted(high_corr_pairs, key=lambda x: x['abs_correlation'], reverse=True)
    
    print(f"\nPares de variables con correlación ≥ {threshold}:")
    if high_corr_pairs:
        for pair in high_corr_pairs:
            print(f"  {pair['var1']} ↔ {pair['var2']}: {pair['correlation']:.4f}")
    else:
        print(f"  No se encontraron pares con correlación ≥ {threshold}")
    
    # Análisis de correlación con la variable objetivo
    if target_col in df.columns:
        target_corr = df[numeric_cols + [target_col]].corr()[target_col].drop(target_col)
        target_corr = target_corr.sort_values(key=abs, ascending=False)
        
        print(f"\nTop 15 variables más correlacionadas con {target_col}:")
        for var, corr in target_corr.head(15).items():
            print(f"  {var}: {corr:.4f}")
    
    # Crear visualizaciones
    if save_plots:
        # 1. Heatmap de correlación completa
        plt.figure(figsize=(20, 16))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=False, cmap='RdBu_r', center=0,
                   square=True, cbar_kws={"shrink": .8})
        plt.title('Matriz de Correlación - Variables Numéricas', fontsize=16, pad=20)
        plt.tight_layout()
        plt.savefig('matriz_correlacion_completa.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 2. Heatmap de correlaciones altas solamente
        if high_corr_pairs:
            # Crear matriz solo con variables altamente correlacionadas
            high_corr_vars = list(set([pair['var1'] for pair in high_corr_pairs] + 
                                    [pair['var2'] for pair in high_corr_pairs]))
            high_corr_matrix = df[high_corr_vars].corr()
            
            plt.figure(figsize=(12, 10))
            mask = np.triu(np.ones_like(high_corr_matrix, dtype=bool))
            sns.heatmap(high_corr_matrix, mask=mask, annot=True, cmap='RdBu_r', center=0,
                       square=True, cbar_kws={"shrink": .8}, fmt='.3f')
            plt.title(f'Correlaciones Altas (≥ {threshold})', fontsize=16, pad=20)
            plt.tight_layout()
            plt.savefig('correlaciones_altas.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        # 3. Gráfico de correlación con variable objetivo
        if target_col in df.columns:
            plt.figure(figsize=(12, 8))
            top_vars = target_corr.head(20)
            colors = ['red' if x < 0 else 'blue' for x in top_vars.values]
            bars = plt.barh(range(len(top_vars)), top_vars.values, color=colors, alpha=0.7)
            plt.yticks(range(len(top_vars)), top_vars.index)
            plt.xlabel('Correlación con SalePrice')
            plt.title('Top 20 Variables Más Correlacionadas con SalePrice', fontsize=14, pad=20)
            plt.grid(axis='x', alpha=0.3)
            
            # Añadir valores en las barras
            for i, (bar, value) in enumerate(zip(bars, top_vars.values)):
                plt.text(value + (0.01 if value >= 0 else -0.01), bar.get_y() + bar.get_height()/2, 
                        f'{value:.3f}', ha='left' if value >= 0 else 'right', va='center', fontsize=9)
            
            plt.tight_layout()
            plt.savefig('correlacion_con_target.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    # Calcular VIF (Variance Inflation Factor) para detectar multicolinealidad
    print(f"\n=== ANÁLISIS VIF (Variance Inflation Factor) ===")
    vif_data = calculate_vif(df[numeric_cols])
    
    print("VIF por variable (VIF > 10 indica multicolinealidad):")
    high_vif = vif_data[vif_data['VIF'] > 10].sort_values('VIF', ascending=False)
    if not high_vif.empty:
        print(high_vif.to_string(index=False))
    else:
        print("  No se encontraron variables con VIF > 10")
    
    # Guardar resultados
    results = {
        'correlation_matrix': corr_matrix,
        'high_correlation_pairs': high_corr_pairs,
        'target_correlations': target_corr if target_col in df.columns else None,
        'vif_data': vif_data,
        'high_vif_vars': high_vif
    }
    
    # Guardar datos en CSV
    if high_corr_pairs:
        high_corr_df = pd.DataFrame(high_corr_pairs)
        high_corr_df.to_csv('pares_correlacion_altas.csv', index=False)
        print(f"\n✅ Resultados guardados en 'pares_correlacion_altas.csv'")
    
    vif_data.to_csv('vif_analysis.csv', index=False)
    print(f"✅ Análisis VIF guardado en 'vif_analysis.csv'")
    
    return results


def calculate_vif(df):
    """
    Calcula el VIF (Variance Inflation Factor) para detectar multicolinealidad.
    
    Args:
        df: DataFrame con variables numéricas
        
    Returns:
        DataFrame con VIF por variable
    """
    from sklearn.linear_model import LinearRegression
    
    vif_data = pd.DataFrame()
    vif_data["Variable"] = df.columns
    vif_data["VIF"] = [variance_inflation_factor(df.values, i) for i in range(df.shape[1])]
    
    return vif_data


def variance_inflation_factor(X, feature_idx):
    """
    Calcula el VIF para una variable específica.
    
    Args:
        X: Array de características
        feature_idx: Índice de la variable a analizar
        
    Returns:
        float: VIF de la variable
    """
    from sklearn.linear_model import LinearRegression
    
    # Variable objetivo
    y = X[:, feature_idx]
    
    # Variables predictoras (todas excepto la variable objetivo)
    X_features = np.delete(X, feature_idx, axis=1)
    
    # Ajustar modelo de regresión
    lr = LinearRegression()
    lr.fit(X_features, y)
    
    # Calcular R²
    y_pred = lr.predict(X_features)
    r_squared = 1 - (np.sum((y - y_pred) ** 2) / np.sum((y - np.mean(y)) ** 2))
    
    # Calcular VIF
    if r_squared >= 0.999:  # Evitar división por cero
        return float('inf')
    
    vif = 1 / (1 - r_squared)
    return vif


def analyze_missing_values(df, title="Análisis de Valores Faltantes"):
    """
    Analiza y muestra valores faltantes de forma detallada.
    
    Args:
        df: DataFrame a analizar
        title: Título para el análisis
    """
    print(f"\n=== {title} ===")
    
    # Conteo de NaN por columna
    nulos_por_columna = df.isnull().sum()
    
    # Convertir a DataFrame para mejor visualización
    resumen = pd.DataFrame({
        "columna": nulos_por_columna.index,
        "conteo_NaN": nulos_por_columna.values
    })
    
    # Mostrar todas las filas
    pd.set_option("display.max_rows", None)
    print("Conteo de NaN por columna:")
    print(resumen)
    
    # Top 10 columnas con más NaN
    print("\nTop 10 columnas con más valores faltantes:")
    top_nan = df.isna().sum().sort_values(ascending=False).head(10)
    print(top_nan)
    
    # Estadísticas generales
    total_nan = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    percentage_nan = (total_nan / total_cells) * 100
    
    print(f"\nEstadísticas generales:")
    print(f"- Total de valores faltantes: {total_nan}")
    print(f"- Total de celdas: {total_cells}")
    print(f"- Porcentaje de valores faltantes: {percentage_nan:.2f}%")
    
    # Columnas sin NaN
    columns_sin_nan = df.columns[df.isnull().sum() == 0]
    print(f"- Columnas sin valores faltantes: {len(columns_sin_nan)}")
    
    # Columnas con NaN
    columns_con_nan = df.columns[df.isnull().sum() > 0]
    print(f"- Columnas con valores faltantes: {len(columns_con_nan)}")
    
    return resumen, top_nan


def exploratory_data_analysis(train_path="data/train.csv"):
    """
    Realiza análisis exploratorio de datos completo.
    
    Args:
        train_path: Ruta al archivo de entrenamiento
    """
    print("=== ANÁLISIS EXPLORATORIO DE DATOS ===")
    
    # Cargar datos
    df = pd.read_csv(train_path)
    print(f"Datos cargados: {df.shape}")
    
    # Configurar pandas para mostrar todas las columnas
    pd.set_option("display.max_columns", None)
    
    # 1. Información básica
    print("\n1. INFORMACIÓN BÁSICA:")
    print("Columnas:", df.columns.tolist())
    print("\nPrimeras 10 filas:")
    print(df.head(10))
    
    # 2. Aplicar pipeline de limpieza paso a paso
    print("\n2. APLICANDO PIPELINE DE LIMPIEZA:")
    
    # Paso 1: Eliminar columnas
    df_limpio = drop_columns(df)
    print(f"Después de eliminar columnas: {df_limpio.shape}")
    
    # Paso 2: Limpiar NaN
    df_limpio = limpiar_df(df_limpio)
    print(f"Después de limpiar NaN: {df_limpio.shape}")
    
    # Paso 3: Añadir características
    df_limpio = add_engineered_features(df_limpio)
    print(f"Después de añadir características: {df_limpio.shape}")
    
    # Paso 4: Imputar faltantes
    df_limpio_sin_NaN = impute_missing(df_limpio)
    print(f"Después de imputar faltantes: {df_limpio_sin_NaN.shape}")
    
    # 3. Análisis de valores únicos
    analyze_unique_values(df_limpio, "ANÁLISIS DE VALORES ÚNICOS POR COLUMNA")
    
    # 4. Análisis de NaN ANTES de la limpieza final
    analyze_missing_values(df_limpio, "ANÁLISIS DE VALORES FALTANTES (ANTES DE IMPUTACIÓN)")
    
    # 5. Análisis de NaN DESPUÉS de la limpieza final
    analyze_missing_values(df_limpio_sin_NaN, "ANÁLISIS DE VALORES FALTANTES (DESPUÉS DE IMPUTACIÓN)")
    
    # 6. Análisis de colinealidad
    collinearity_results = analyze_collinearity(df_limpio_sin_NaN, target_col="SalePrice", threshold=0.8)
    
    # 7. Verificar que no quedan NaN después de limpieza
    total_nan_final = df_limpio_sin_NaN.isnull().sum().sum()
    print(f"\n7. VERIFICACIÓN FINAL:")
    print(f"Total de valores faltantes después de limpieza: {total_nan_final}")
    if total_nan_final == 0:
        print("✅ ¡No quedan valores faltantes!")
    else:
        print("⚠️  Aún hay valores faltantes que revisar")
    
    # 8. Generar visualizaciones
    generate_visualizations(df, df_limpio, df_limpio_sin_NaN)
    
    print("\n✅ Análisis exploratorio completado!")
    return df, df_limpio, df_limpio_sin_NaN


def run_collinearity_analysis(train_path="data/train.csv", threshold=0.8):
    """
    Ejecuta solo el análisis de colinealidad.
    
    Args:
        train_path: Ruta al archivo de entrenamiento
        threshold: Umbral de correlación para considerar colinealidad alta
    """
    print("=== ANÁLISIS DE COLINEALIDAD INDEPENDIENTE ===")
    
    # Cargar y limpiar datos
    df = pd.read_csv(train_path)
    df_clean = drop_columns(df)
    df_clean = limpiar_df(df_clean)
    df_clean = add_engineered_features(df_clean)
    df_clean = impute_missing(df_clean)
    
    # Ejecutar análisis de colinealidad
    results = analyze_collinearity(df_clean, target_col="SalePrice", threshold=threshold)
    
    print("\n✅ Análisis de colinealidad completado!")
    return results


def main(optimize_models=False, n_iter=50, cv=5):
    """
    Función principal que ejecuta todo el pipeline.
    
    Args:
        optimize_models: Si True, usa Random Search para optimizar hiperparámetros
        n_iter: Número de iteraciones para Random Search (solo si optimize_models=True)
        cv: Número de folds para cross-validation (solo si optimize_models=True)
    """
    print("=== HOUSING PRICE PREDICTION ML PIPELINE ===")
    print("Iniciando pipeline completo...")
    
    # 0. Análisis exploratorio de datos
    df, df_limpio, df_limpio_sin_NaN = exploratory_data_analysis()
    
    if optimize_models:
        print("\n🚀 MODO OPTIMIZACIÓN ACTIVADO")
        print(f"Usando Random Search con {n_iter} iteraciones y {cv}-fold CV")
        
        # 1. Entrenar modelos con optimización
        results = train_models_with_optimization(
            optimize_models=True, 
            n_iter=n_iter, 
            cv=cv
        )
        
        # 2. Analizar importancia de características
        importance_analysis = analyze_feature_importance(results)
        
        # 3. Entrenar modelo con top 20 características
        top20_model, top20_preprocessor = train_top20_model(results, importance_analysis)
        
        # 4. Evaluar modelos localmente
        evaluate_models_locally()
        
        print("\n=== PIPELINE CON OPTIMIZACIÓN COMPLETADO ===")
        print("Archivos generados:")
        print("- submission_xgb_optimized.csv")
        print("- submission_rf_optimized.csv")
        print("- submission_lr_optimized.csv")
        print("- submission_xgb_top20.csv")
        print("- optimized_models.pkl")
        print("- search_results.pkl")
        print("- xgb_top20_pipeline.pkl")
        print("- resumen_dimensionalidad.csv")
        print("- importancias_post_ohe_gain.csv")
        print("- importancias_agregadas_gain.csv")
        print("- importancias_agregadas_permutation.csv")
        print("- varianza_columnas_eliminadas.png")
        print("- categorias_eliminadas.png")
        print("- histogramas_numericas_original.png")
        print("- distribucion_categoricas_original.png")
        print("- histogramas_numericas_limpio.png")
        print("- distribucion_categoricas_limpio.png")
        print("- feature_importance_post_ohe.png")
        print("- feature_importance_aggregated_gain.png")
        print("- feature_importance_aggregated_permutation.png")
        
    else:
        print("\n📊 MODO ESTÁNDAR")
        print("Usando parámetros por defecto")
        
        # 1. Entrenar modelos
        results = train_models()
        
        # 2. Analizar importancia de características
        importance_analysis = analyze_feature_importance(results)
        
        # 3. Entrenar modelo con top 20 características
        top20_model, top20_preprocessor = train_top20_model(results, importance_analysis)
        
        # 4. Evaluar modelos localmente
        evaluate_models_locally()
        
        print("\n=== PIPELINE ESTÁNDAR COMPLETADO ===")
        print("Archivos generados:")
        print("- submission_linreg.csv")
        print("- submission_rf.csv") 
        print("- submission_xgb.csv")
        print("- submission_xgb_top20.csv")
        print("- xgb_full_pipeline.pkl")
        print("- xgb_top20_pipeline.pkl")
        print("- resumen_dimensionalidad.csv")
        print("- importancias_post_ohe_gain.csv")
        print("- importancias_agregadas_gain.csv")
        print("- importancias_agregadas_permutation.csv")
        print("- varianza_columnas_eliminadas.png")
        print("- categorias_eliminadas.png")
        print("- histogramas_numericas_original.png")
        print("- distribucion_categoricas_original.png")
        print("- histogramas_numericas_limpio.png")
        print("- distribucion_categoricas_limpio.png")
        print("- feature_importance_post_ohe.png")
        print("- feature_importance_aggregated_gain.png")
        print("- feature_importance_aggregated_permutation.png")


if __name__ == "__main__":
    main()
