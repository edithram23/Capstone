import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Define the folder path
folder_path = "u1314-14afsl141-smasdads-12234"

# Construct the updated file path
updated_file_path = os.path.join(folder_path, "updated_titanic.csv")

# Check if the updated file exists
if not os.path.exists(updated_file_path):
    print(f"Error: The file {updated_file_path} does not exist.")
else:
    # Load the updated DataFrame
    try:
        df = pd.read_csv(updated_file_path)
    except Exception as e:
        print(f"Error reading {updated_file_path}: {e}")
        df = None

    if df is not None:
        # 1. Bar Plot: Survived vs. Sex
        try:
            plt.figure(figsize=(8, 6))
            sns.countplot(x="Sex", hue="Survived", data=df)
            plt.title("Survival Rate by Sex")
            plt.xlabel("Sex")
            plt.ylabel("Number of Passengers")
            plt.savefig(os.path.join(folder_path, "survived_vs_sex.png"))
            plt.close()
            print("Bar plot: Survived vs. Sex created successfully.")
        except Exception as e:
            print(f"Error creating Survived vs. Sex bar plot: {e}")

        # 2. Histogram: Age Distribution
        try:
            plt.figure(figsize=(8, 6))
            sns.histplot(
                df["Age"].dropna(), kde=True
            )  # Drop NaN values for the histogram
            plt.title("Age Distribution")
            plt.xlabel("Age")
            plt.ylabel("Frequency")
            plt.savefig(os.path.join(folder_path, "age_distribution.png"))
            plt.close()
            print("Histogram: Age Distribution created successfully.")
        except Exception as e:
            print(f"Error creating Age Distribution histogram: {e}")

        # 3. Box Plot: Fare vs. Pclass
        try:
            plt.figure(figsize=(8, 6))
            sns.boxplot(x="Pclass", y="Fare", data=df)
            plt.title("Fare Distribution by Passenger Class")
            plt.xlabel("Passenger Class")
            plt.ylabel("Fare")
            plt.savefig(os.path.join(folder_path, "fare_vs_pclass.png"))
            plt.close()
            print("Box plot: Fare vs. Pclass created successfully.")
        except Exception as e:
            print(f"Error creating Fare vs. Pclass box plot: {e}")

        # 4. Scatter Plot: Age vs. Fare
        try:
            plt.figure(figsize=(8, 6))
            sns.scatterplot(x="Age", y="Fare", data=df)
            plt.title("Age vs. Fare")
            plt.xlabel("Age")
            plt.ylabel("Fare")
            plt.savefig(os.path.join(folder_path, "age_vs_fare.png"))
            plt.close()
            print("Scatter plot: Age vs. Fare created successfully.")
        except Exception as e:
            print(f"Error creating Age vs. Fare scatter plot: {e}")

        # 5. Count Plot: Pclass
        try:
            plt.figure(figsize=(8, 6))
            sns.countplot(x="Pclass", data=df)
            plt.title("Passenger Class Distribution")
            plt.xlabel("Passenger Class")
            plt.ylabel("Number of Passengers")
            plt.savefig(os.path.join(folder_path, "pclass_distribution.png"))
            plt.close()
            print("Count plot: Pclass created successfully.")
        except Exception as e:
            print(f"Error creating Pclass count plot: {e}")

        # 6. Bar Plot: Survived vs. Pclass
        try:
            plt.figure(figsize=(8, 6))
            sns.countplot(x="Pclass", hue="Survived", data=df)
            plt.title("Survival Rate by Passenger Class")
            plt.xlabel("Passenger Class")
            plt.ylabel("Number of Passengers")
            plt.savefig(os.path.join(folder_path, "survived_vs_pclass.png"))
            plt.close()
            print("Bar plot: Survived vs. Pclass created successfully.")
        except Exception as e:
            print(f"Error creating Survived vs. Pclass bar plot: {e}")

        # 7. Bar Plot: Survived vs. Embarked
        try:
            plt.figure(figsize=(8, 6))
            sns.countplot(x="Embarked", hue="Survived", data=df)
            plt.title("Survival Rate by Embarkation Point")
            plt.xlabel("Embarkation Point")
            plt.ylabel("Number of Passengers")
            plt.savefig(os.path.join(folder_path, "survived_vs_embarked.png"))
            plt.close()
            print("Bar plot: Survived vs. Embarked created successfully.")
        except Exception as e:
            print(f"Error creating Survived vs. Embarked bar plot: {e}")

        # 8. Violin Plot: Age vs. Sex
        try:
            plt.figure(figsize=(8, 6))
            sns.violinplot(x="Sex", y="Age", data=df)
            plt.title("Age Distribution by Sex")
            plt.xlabel("Sex")
            plt.ylabel("Age")
            plt.savefig(os.path.join(folder_path, "age_vs_sex.png"))
            plt.close()
            print("Violin plot: Age vs. Sex created successfully.")
        except Exception as e:
            print(f"Error creating Age vs. Sex violin plot: {e}")

        # 9. Facet Grid (Small Multiples): Age Distribution by Survival
        try:
            g = sns.FacetGrid(df, col="Survived", height=4, aspect=1.2)
            g.map(sns.histplot, "Age")
            g.set_titles("Survived = {col_name}")
            plt.savefig(os.path.join(folder_path, "age_distribution_by_survival.png"))
            plt.close()
            print("Facet Grid: Age Distribution by Survival created successfully.")
        except Exception as e:
            print(f"Error creating Age Distribution by Survival facet grid: {e}")

        # 10. Stacked Bar Plot: Pclass vs. Survived
        try:
            # Create a contingency table
            contingency_table = pd.crosstab(df["Pclass"], df["Survived"])

            # Plotting the stacked bar plot
            contingency_table.plot(kind="bar", stacked=True, figsize=(8, 6))
            plt.title("Survival by Passenger Class")
            plt.xlabel("Passenger Class")
            plt.ylabel("Number of Passengers")
            plt.legend(["Not Survived", "Survived"])
            plt.savefig(os.path.join(folder_path, "pclass_vs_survived_stacked.png"))
            plt.close()
            print("Stacked Bar Plot: Pclass vs. Survived created successfully.")

        except Exception as e:
            print(f"Error creating Pclass vs. Survived stacked bar plot: {e}")
