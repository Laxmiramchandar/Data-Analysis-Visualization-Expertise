import numpy as np
import pandas as pd
from scipy import stats

class StatisticalAnalyzer:
    """
    Statistical Analysis and Hypothesis Testing Module
    """

    def __init__(self, df):
        self.df = df.copy()

    def descriptive_stats(self, numeric_cols=None):
        """Calculates mean, median, std, min, 25%, 50%, 75%, max, skewness, and kurtosis."""
        if numeric_cols is None:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()

        res = {}
        for col in numeric_cols:
            series = self.df[col].dropna()
            res[col] = {
                'count': len(series),
                'mean': round(float(series.mean()), 2),
                'std': round(float(series.std()), 2),
                'min': round(float(series.min()), 2),
                '25%': round(float(series.quantile(0.25)), 2),
                'median': round(float(series.median()), 2),
                '75%': round(float(series.quantile(0.75)), 2),
                'max': round(float(series.max()), 2),
                'skewness': round(float(series.skew()), 2),
                'kurtosis': round(float(series.kurt()), 2)
            }
        return pd.DataFrame(res).T

    def correlation_matrix(self, numeric_cols=None, method='pearson'):
        """Computes correlation matrix for specified numerical columns."""
        if numeric_cols is None:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        return self.df[numeric_cols].corr(method=method).round(3)

    def pearson_correlation_test(self, col1, col2):
        """Computes Pearson correlation coefficient and p-value with 95% CI."""
        valid = self.df[[col1, col2]].dropna()
        res = stats.pearsonr(valid[col1], valid[col2])
        r = res.statistic
        p_val = res.pvalue
        ci = res.confidence_interval(confidence_level=0.95)
        
        return {
            'col1': col1,
            'col2': col2,
            'r_statistic': round(float(r), 4),
            'p_value': float(p_val),
            'is_significant_5pct': bool(p_val < 0.05),
            'r_squared': round(float(r**2), 4),
            'ci_lower': round(float(ci.low), 4),
            'ci_upper': round(float(ci.high), 4)
        }

    def two_sample_ttest(self, group_col, value_col, group1_val, group2_val):
        """Performs two-sample independent t-test between two groups with 95% CI."""
        g1 = self.df[self.df[group_col] == group1_val][value_col].dropna()
        g2 = self.df[self.df[group_col] == group2_val][value_col].dropna()
        
        res = stats.ttest_ind(g1, g2, equal_var=False)
        t_stat = res.statistic
        p_val = res.pvalue
        
        # Cohen's d
        n1, n2 = len(g1), len(g2)
        var1, var2 = g1.var(ddof=1), g2.var(ddof=1)
        pooled_sd = np.sqrt(((n1 - 1)*var1 + (n2 - 1)*var2) / (n1 + n2 - 2)) if (n1 + n2 - 2) > 0 else 0
        cohens_d = abs((g1.mean() - g2.mean()) / pooled_sd) if pooled_sd > 0 else 0.0
        
        try:
            ci = res.confidence_interval(confidence_level=0.95)
            ci_lower, ci_upper = round(float(ci.low), 4), round(float(ci.high), 4)
        except AttributeError:
            ci_lower, ci_upper = None, None

        return {
            'group1': group1_val,
            'group1_mean': round(float(g1.mean()), 2),
            'group2': group2_val,
            'group2_mean': round(float(g2.mean()), 2),
            'test_statistic': round(float(t_stat), 4),
            'p_value': float(p_val),
            'is_significant_5pct': bool(p_val < 0.05),
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'cohens_d': round(float(cohens_d), 4)
        }

    def one_way_anova(self, category_col, value_col):
        """Performs One-Way ANOVA across multiple categorical groups."""
        groups = [group[value_col].dropna().values for _, group in self.df.groupby(category_col)]
        f_stat, p_val = stats.f_oneway(*groups)
        
        # Eta Squared
        all_data = np.concatenate(groups)
        grand_mean = all_data.mean()
        ss_total = np.sum((all_data - grand_mean)**2)
        ss_between = sum([len(g) * (g.mean() - grand_mean)**2 for g in groups])
        eta_squared = ss_between / ss_total if ss_total > 0 else 0.0
        
        return {
            'category_column': category_col,
            'value_column': value_col,
            'test_statistic': round(float(f_stat), 4),
            'p_value': float(p_val),
            'is_significant_5pct': bool(p_val < 0.05),
            'eta_squared': round(float(eta_squared), 4)
        }
        
    def tukey_hsd_test(self, category_col, value_col):
        """Performs Tukey HSD post-hoc test."""
        grouped = self.df[[category_col, value_col]].dropna().groupby(category_col)
        group_names = list(grouped.groups.keys())
        group_data = [grouped.get_group(name)[value_col].values for name in group_names]
        
        res = stats.tukey_hsd(*group_data)
        
        results = []
        for i in range(len(group_names)):
            for j in range(i + 1, len(group_names)):
                p_adj = res.pvalue[i, j]
                results.append({
                    'group1': group_names[i],
                    'group2': group_names[j],
                    'mean_diff': round(float(res.statistic[i, j]), 4),
                    'p_adj': float(p_adj),
                    'is_significant': bool(p_adj < 0.05)
                })
        return pd.DataFrame(results)

    # Financial Analysis additions (Point 10)
    def calculate_sharpe_ratio(self, return_col, risk_free_rate=0.0):
        """Calculates the annualized Sharpe Ratio for daily returns."""
        returns = self.df[return_col].dropna() / 100.0  # assuming pct
        mean_return = returns.mean()
        std_return = returns.std()
        if std_return == 0:
            return 0.0
        # Annualize (assuming 252 trading days)
        sharpe = ((mean_return - risk_free_rate) / std_return) * np.sqrt(252)
        return round(float(sharpe), 2)

    def calculate_annualized_volatility(self, return_col):
        """Calculates Annualized Volatility (std dev * sqrt(252))."""
        returns = self.df[return_col].dropna() / 100.0
        return round(float(returns.std() * np.sqrt(252) * 100), 2)
        
    def calculate_sortino_ratio(self, return_col, risk_free_rate=0.0):
        """Calculates Annualized Sortino Ratio using downside deviation."""
        returns = self.df[return_col].dropna() / 100.0
        mean_return = returns.mean()
        downside_returns = returns[returns < 0]
        downside_std = downside_returns.std(ddof=1)
        if pd.isna(downside_std) or downside_std == 0:
            return 0.0
        sortino = ((mean_return - risk_free_rate) / downside_std) * np.sqrt(252)
        return round(float(sortino), 2)

    def calculate_max_drawdown(self, price_col):
        """Calculates Maximum Drawdown (Peak to Trough drop) percentage."""
        prices = self.df[price_col].dropna()
        roll_max = prices.cummax()
        drawdowns = (prices - roll_max) / roll_max
        max_drawdown = drawdowns.min()
        return round(float(max_drawdown * 100), 2)

    def format_hypothesis_report(self, h0, h1, test_used, test_stat_name, stat_val, p_val, interpretation_reject, interpretation_fail, why_it_matters_reject, why_it_matters_fail=None, ci_lower=None, ci_upper=None, effect_size_name=None, effect_size_val=None):
        """Generates a standard formatted string for hypothesis test results."""
        sig = 0.05
        
        if why_it_matters_fail is None:
            why_it_matters_fail = "The result does not provide sufficient statistical evidence for a targeted intervention."
            
        if p_val < sig:
            decision = "Reject H₀"
            interpretation = interpretation_reject
            why = why_it_matters_reject
        else:
            decision = "Fail to Reject H₀"
            interpretation = interpretation_fail
            why = why_it_matters_fail
            
        ci_string = f"[{ci_lower}, {ci_upper}]" if ci_lower is not None and ci_upper is not None else "N/A"
        effect_string = f"\nEffect Size ({effect_size_name}): {effect_size_val}" if effect_size_name and effect_size_val is not None else ""

        report = (
            f"--- FORMAL HYPOTHESIS TEST ---\n"
            f"H₀: {h0}\n"
            f"H₁: {h1}\n"
            f"Test used: {test_used}\n"
            f"Test statistic ({test_stat_name}): {stat_val}\n"
            f"p-value: {p_val:.5f}\n"
            f"95% Confidence Interval: {ci_string}{effect_string}\n"
            f"Significance level: {sig}\n"
            f"Decision: {decision}\n\n"
            f"Business interpretation: {interpretation}\n"
            f"Why this matters: {why}\n"
            f"------------------------------"
        )
        return report
