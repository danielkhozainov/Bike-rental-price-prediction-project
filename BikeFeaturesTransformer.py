{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8060f785-ea0a-49f7-a9d2-9bdb87b82af2",
   "metadata": {},
   "outputs": [],
   "source": [
    "# features.py\n",
    "from sklearn.base import BaseEstimator, TransformerMixin\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "\n",
    "class BikeFeaturesTransformer(BaseEstimator, TransformerMixin):\n",
    "    def __init__(self, season_threshold=0.05):\n",
    "        self.season_threshold = season_threshold\n",
    "        self.common_seasons_ = None\n",
    "\n",
    "    def fit(self, X, y=None):\n",
    "        # Определяем частые категории для Seasons\n",
    "        counts = X['Seasons'].value_counts(normalize=True)\n",
    "        self.common_seasons_ = counts[counts >= self.season_threshold].index.tolist()\n",
    "        return self\n",
    "\n",
    "    def transform(self, X):\n",
    "        X_out = X.copy()\n",
    "\n",
    "        # Группируем редкие сезоны в 'Other'\n",
    "        X_out['Seasons_grouped'] = X_out['Seasons'].apply(\n",
    "            lambda s: s if s in self.common_seasons_ else 'Other'\n",
    "        )\n",
    "\n",
    "        # Создаём признак пика спроса: Evening или Late Evening\n",
    "        X_out['is_peak_hour'] = (\n",
    "            X_out['Time_Period_Evening'] | X_out['Time_Period_Late Evening']\n",
    "        ).astype(int)\n",
    "\n",
    "        # Удаляем исходные бинарные колонки времени\n",
    "        time_cols = [c for c in X_out.columns if c.startswith('Time_Period_')]\n",
    "        X_out = X_out.drop(columns=time_cols)\n",
    "\n",
    "        return X_out"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
