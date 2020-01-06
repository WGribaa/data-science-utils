"""
# Made by Wael Gribaa , January 2020
# Contact at : g.wael@outlook.fr
# GitHub : https://github.com/Whole-Brain
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class ColumnInfos:
    """
    Each column of the pandas DataFrame is a object that holds its own infos and advices.
    """
    def __init__(self, index, name, n_rows, nulls, dtype, uniques, categories):
        """
        :param index: Number of the 0-indexed index in the DataFrame. Currently independent from the tru Index.
        :param name: name of the column.
        :param n_rows: Number of non-null values.
        :param nulls: Number of null values.
        :param dtype: dtype of the column.
        :param uniques: Number of uniques.
        :param categories: List of categories if less than the Helper parameter "max_categorisable".
        """
        self.index = index
        self.name = name
        self.n_rows = n_rows
        self.nulls = nulls
        self.dtype = dtype
        self.uniques = uniques
        self.categories = categories

    def has_advice(self):
        """
        Tells if the ColumnInfo presently holds an advice.
        :return: Boolean. True : yes, False = no.
        """
        return self.categories is not None

    def get_advice(self):
        """
        If it holds any advice, formats it then return it as a String.
        :return: Advice(s) as String to be printed as is.
        """
        if self.categories is None:
            return
        ret = "The column \"%s\" (index %d)" % (self.name, self.index)
        if self.uniques > 1:
            return ret+" should be casted into a %s." % \
                   ("category" if self.uniques > 2 else "boolean")
        else:
            return ret+"should be deleted."

    def __str__(self):
        return format_col_infos([self.name], {}, len(self.name))


class Helper:
    """
    A class that provides method toe quickly sea points of interest of a pandas Dataframe.
    """
    # Shows a different color for each type of a columns.
    color_dict = {"int64": "1;31;47", "float64": "1;33;47", "object": "1;32;47", "bool": "1;34;47",
                  "category": "1;36;47", "datetime64[ns]": "1;37;47", "timedelta64[ns]": "1;35;47"}

    # Levels of correlations given a pearson correlation value (0 to 1).
    # Reference : http://www.statstutor.ac.uk/resources/uploaded/pearsons.pdf page 4
    corr_categories_intervals = (0.2, 0.4, 0.6, 0.8, 1)
    corr_categories_names = ('very weak', 'weak', 'moderate',
                             'strong', 'very strong')

    def __init__(self, dataframe, max_categorisable=12, corr_annot=True, corr_cmap="RdYlGn", show_corr_matrix=True):
        """
        :param dataframe: The Dataframe to analyse
        :param max_categorisable: Maximum number of uniques for a column to be considered as categorisable.
        :param corr_annot: Shows or not the correlation value on the Heatmap.
        :param corr_cmap: Sets the colormap used for the correlation matrix.
        Check here : https://python-graph-gallery.com/92-control-color-in-seaborn-heatmaps/
        :param show_corr_matrix: Sets if the correlation matrix is wanted to be drawn with seaborn.
        """
        assert isinstance(dataframe, pd.DataFrame)
        self.dataframe = dataframe
        self.annot_corr = corr_annot
        self.corr_cmap = corr_cmap
        self.max_categorisable = max_categorisable
        self.show_corr_matrix = show_corr_matrix
        # The correlation matrix drawn with seaborn.
        self.corr = None
        # Dictionary of ColumnInfos, working along with the current class.
        self.dataframe_col_infos = {}

    def firstAnalysis(self, show_corr_matrix=True):
        """
        Launches basic hints for analyses :
        1- Extended info-like table.
        2- Correlation matrix and correlated pairs of characteristics.
        3- Relevant advices about columns.
        :return:
        """
        print("\n##### GENERAL DATAFRAME INFOS #####")
        print(self.analyze_columns())
        print("\n##### CORRELATION INFOS #####")
        print(self.analyze_correlations())
        print("\n##### GENERAL ADVICES #####")
        print(self.get_advices())
        if show_corr_matrix and self.show_corr_matrix and self.corr is not None:
            sns.heatmap(self.corr, cmap=self.corr_cmap, annot=self.annot_corr, xticklabels=self.corr.columns.values,
                        yticklabels=self.corr.columns.values, vmin=-1, vmax=1)
            plt.show()

    def analyze_columns(self):
        """
        Gives basic infos about the Dataframe, just like DataFrame.info(), but with some extras :
        - actually tells about the number of NaN per column.
        - informs about the number of uniques per column.
        - shows the unique values of a columns if they are less than the attribute max_categorisable (default=12).
        :return: All infos as formatted text to be printed as is.
        """
        cols = self.dataframe.columns
        n_cols = len(cols)
        n_rows = len(self.dataframe)
        indices = self.dataframe.index
        dataframe_main_infos = '\nThe dataframe has %s columns and %d rows.' % (n_cols, n_rows) + \
                               "\nIndices : from %d to %d (step= %d)" \
                               % (indices.start, indices.stop - indices.step, indices.step)
        self.dataframe_col_infos = {}
        maxlength = 0
        for i in range(0, len(cols)):
            name = cols[i]
            nulls = self.dataframe[cols[i]].isna().sum()
            uniques = len(self.dataframe[cols[i]].unique())
            coltype = str(self.dataframe[cols[i]].dtype)
            if maxlength < len(name):
                maxlength = len(name)
            categories = None
            if coltype == "category" or uniques <= self.max_categorisable:
                categories = list(self.dataframe[cols[i]].unique())
            self.dataframe_col_infos[i] = ColumnInfos(i, name, nulls, n_rows - nulls,
                                                      str(self.dataframe[cols[i]].dtype), uniques, categories)
        col_infos = format_col_infos(self.dataframe_col_infos, self.color_dict, maxlength)

        return dataframe_main_infos + "\n" + "\n".join(col_infos)

    def analyze_correlations(self):
        """
        Get the correlation of each pair of caracteristic and prints the correlation of strength of the correlated ones.
        :return:
        """
        self.corr = self.dataframe.corr()
        corr_infos = ""
        for i in range(len(self.corr) - 1):
            for j in range(i + 1, len(self.corr)):
                corr_value = self.corr.iloc[i][j]
                if pd.isnull(corr_value):
                    continue
                correlation_strength = get_interval(corr_value, self.corr_categories_intervals)
                if correlation_strength > 0:
                    corr_infos += "\n\"%s\" and \"%s\" have a %s %s correlation : %f" % (
                        self.dataframe.columns[i], self.dataframe.columns[j], self.corr_categories_names
                        [correlation_strength], "positive" if corr_value >= 0 else "negative",
                        corr_value)

        return corr_infos

    def get_advices(self):
        advices = []
        for i in range(len(self.dataframe_col_infos)):
            if self.dataframe_col_infos[i].has_advice():
                advices.append(self.dataframe_col_infos[i].get_advice())
        return "\n"+"\n".join(advices)


def format_col_infos(infos, color_dict, maxlength):
    """
    Format the infos passed as parameter so that they are displayed in a nice faschion in the console.
    :param infos: List or tuple of ColumnInfos instances. One per row.
    :param color_dict: Dictionary to set a color for each type of data.
    :param maxlength: Length of the longest name string. Need so each column of info is aligned.
    :return: A list of formatted strings to be joined with a line-return then to be displayed as is.
    """
    ret = []
    for i in range(len(infos)):
        colinfo = infos[i]
        ret.append(str(i) + ":\t\"" + colinfo.name + "\"" + "." * (
                maxlength + 2 - len(colinfo.name)) + "of type %s \t%s null values and %d uniques%s." % (
                       "\x1b[" + color_dict[str(colinfo.dtype)] + "m" + str(colinfo.dtype) + "\x1b[0m",
                       str(colinfo.n_rows), colinfo.uniques,
                       "" if not colinfo.categories else " [" + ", ".join(map(str, colinfo.categories)) + "]"))
    return ret


def get_interval(value, intervals):
    """
    Returns the index of the interval the value lies in.

    :param value: Value for which to find the interval.
    :param intervals: List or tuple of interval with values which represent the upper boundary of each interval.
    The first interval starts at 0 and ends ar the first value (excluded, except for the last interval).
    :return: Index in regard to the intervals list/tupple.
    """
    if value is None or isinstance(value, str):
        return
    for i in range(len(intervals)):
        if abs(value) < intervals[i]:
            return i
    return len(intervals) - 1