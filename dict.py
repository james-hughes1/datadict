import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pathlib
import warnings

warnings.filterwarnings("ignore", "is_categorical_dtype")


def num_summary(data):
    # Outputs Quantiles for numerical variables
    print("Five number summary\n+-----------+")
    print(f"Maximum: {np.max(data):>17.3f}")
    print(f"Upper quartile: {np.quantile(data, 0.75):>10.3f}")
    print(f"Median: {np.median(data):>18.3f}")
    print(f"Lower Quartile: {np.quantile(data, 0.25):>10.3f}")
    print(f"Minimum: {np.min(data):>17.3f}\n")


def show_correlation(corr_df, colname):
    # Outputs the most correlated other variable in the dataframe
    corrs = corr_df.iloc[i].drop(colname)
    most_correlated = corrs.apply(np.abs).idxmax()
    print(
        "\nMost correlated column: "
        f"{most_correlated} ({corrs[most_correlated]:.3f})"
    )


# Create output folder
output_path = pathlib.Path("figures/")
output_path.mkdir(exist_ok=True)

# Read in the data
df_path = input("Enter dataset filepath: ")

df = pd.read_csv(df_path)
cols = df.columns

# Create a numeric df for correlation finding;
# For categoric variables, convert them to a dummy where 1
# indicates the modal class, as a proxy for the true variable
df_numeric = df.copy()
for col in cols:
    if col in df.select_dtypes(exclude=["number"]).columns:
        df_numeric[col] = 1 * (df[col] == df[col].value_counts().idxmax())
corr_df = df_numeric.corr().fillna(0.0)

# Select target class and date columns
target = input("Enter target column: ")
if target not in cols:
    print("Error: No such column in dataframe.\n")
    target = None

date = input("Enter date column: ")
if date not in cols:
    print("Error: No such column in dataframe.\n")
    date = None
else:
    df[date] = pd.to_datetime(df[date])

for i, col in enumerate(cols):
    print("\n\n\nSUMMARY OF COLUMN: ", col)
    if col in df.select_dtypes(exclude=["number"]).columns:
        # Treat as non-numeric
        if col != date:
            print("Variable type: Categorical\n")
            freq_vals = df[col].value_counts()
            print("Most common values \n+-----------+")
            print("Value                Count      Percentage")
            for j in range(min(10, len(freq_vals))):
                print(
                    f"{freq_vals.index[j]:<21}{freq_vals.iloc[j]:<12}"
                    f"{freq_vals.iloc[j]*100/len(df):.1f}%"
                )
            show_correlation(corr_df, col)
            # Plot heatmap of contingencies with target
            if target:
                fig, ax = plt.subplots(1, 1, figsize=(10, 10))
                sns.heatmap(
                    pd.crosstab(df[col], df[target]),
                    annot=True,
                    fmt="g",
                    ax=ax,
                )
                plt.savefig(f"figures/{col}_contingency.png")
        else:
            print(
                f"Date column from {df[date].dt.date.min()}"
                f" to {df[date].dt.date.max()}"
            )

    else:
        if len(df[col].unique()) / len(df) < 0.1:
            # Treat as discrete
            print("Variable type: Discrete\n")
            num_summary(df[col])
            freq_vals = df[col].value_counts()
            print("Most common values \n+-----------+")
            print("Value                Count      Percentage")
            for j in range(min(10, len(freq_vals))):
                print(
                    f"{freq_vals.index[j]:<21.3f}{freq_vals.iloc[j]:<12}"
                    f"{freq_vals.iloc[j]*100/len(df):.1f}%"
                )
        else:
            # Treat as continuous
            print("Variable type: Continuous\n")
            num_summary(df[col])
            print("Location and spread\n+-----------+")
            print(f"Mean:                            {np.mean(df[col]):.3f}")
            print(
                f"(Unbiased) standard deviation:   "
                f"{np.std(df[col], ddof=1):.3f}\n"
            )
        show_correlation(corr_df, col)
        # Plot either a line plot (date) or boxplots
        if target:
            fig, ax = plt.subplots(1, 1, figsize=(10, 10))
            if date:
                df_time = (
                    df[[date, target, col]].groupby(by=[date, target]).mean()
                )
                sns.lineplot(df_time, x=date, y=col, hue=target, ax=ax)
            else:
                sns.boxplot(df, y=col, x=target, ax=ax)
            plt.savefig(f"figures/{col}_plot.png")
