# data-science-utils
Tools for effective Data analysis and models

AnalysisHelper is a quick tool that will help you have a quick grasp of your DataFrame.
As you would do with pd.DataFrame.info(), now you can import this module and simply create a Helper object that will give you first aid informations listed below. It can now apply its own advices if you want it to !

General Dataframe infos : 
* Number of columns and rows
* Range and step of indices.
* Extended columns infos : name, number of non-nulls, number of nulls and number of unique values. if less that a specified value, it will also show the list of uniques (check the attribute "max_categorisable below).

Correlation infos :
* If wanted, a correlation matrix as a seaborn heatmap (needs seaborn module).
* Pairs of columns that are, at least, weakly correlated.

General advices (1):
* Advices about columns. Shows you which columns should be deleted as adding no information, and which columns should be casted to categorical.
* Tests quite accurately if a column represents a date, and advices you to convert it into a DateTime if so.

(1) Those advices can now be applied by the Helper itself. Check the methods and constructor arguments below.

HOW TO USE:
1- Import the AnalysisHelper.py and add it like a module
2- Once you have read your dataset into a pandas DataFrame, create a AnalysisHelper.Helper object by passing it the DataFrame as the argument. Check the parameters listed below to customize the behaviour of the Helper.
3- The Helper will automatically make its first analysis of the columns. If you want to do it manually, you can call the method "Helper.analyze()"
4- If you didn't set the argument "apply_advice" as True, you can still apply them after the analysis by calling the method "Helper.apply_advices()" of your instance.

Main parameters which can be passed to the firstAnalysis() method :
- dataframe (pandas.DataFrame) [mandatory] : the dataframe to analyze.
- max_categorizable (int) [default=12] : The maximum number of uniques in a column for it to be considered as worth casted into a categorical. Also, the uniques of a column will be listed if the number of uniques are within this number.
- show_corr_matrix (bool) [default=True] : If true, the seaborn heatmap of the correlation matrix will be shown (as a figure).
- corr_annot (bool) [default=True] : If true, the value of each Pearson correlation will be shown inside the seaborn heatmap.
- corr_cmap (string) [default="RdY1Gn"] : Tells which colormap will be used to represent the range of strength of the pearson correlation values in the seaborn heatmap. The cmap has to be a valid colormap from the seaborn heatmaps package. Check https://python-graph-gallery.com/92-control-color-in-seaborn-heatmaps/
- apply_advice (bool) [default=False] : If true, automatically applies the advices of the first analysis and reruns it.


Made by Wael Gribaa in January 2020.
Feel free to contact me at : g.wael@outlook.fr
I am open to suggestions. Thank you.
