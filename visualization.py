import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set global publication visual style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['figure.titlesize'] = 14

class Visualizer:
    """
    Visualization Module for Generating Publication-Quality Charts
    """

    def __init__(self, output_dir='visualizations'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

    def plot_time_series(self, df, date_col, value_col, title, ylabel, filename, ma_cols=None):
        """Plots time series line chart with optional moving averages."""
        fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
        
        ax.plot(df[date_col], df[value_col], label=ylabel, color='#1f77b4', linewidth=2, alpha=0.85)

        if ma_cols:
            colors = ['#ff7f0e', '#2ca02c', '#d62728']
            for idx, ma_col in enumerate(ma_cols):
                if ma_col in df.columns:
                    ax.plot(df[date_col], df[ma_col], label=ma_col, color=colors[idx % len(colors)], linewidth=2, linestyle='--')

        ax.set_title(title, pad=15, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel(ylabel)
        ax.legend(frameon=True, facecolor='white', edgecolor='none')
        fig.tight_layout()
        
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, dpi=300)
        plt.close(fig)
        return filepath

    def plot_bar_chart(self, categories, values, title, xlabel, ylabel, filename, color='#1f77b4'):
        """Plots structured bar chart with data labels."""
        fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
        bars = ax.bar(categories, values, color=color, edgecolor='none', alpha=0.85, width=0.55)
        
        # Add value labels above bars
        max_val = max(values) if len(values) > 0 else 1
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:,.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

        ax.set_title(title, pad=15, fontweight='bold')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylim(0, max_val * 1.15)
        plt.xticks(rotation=25 if len(str(categories[0])) > 8 else 0)
        fig.tight_layout()

        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, dpi=300)
        plt.close(fig)
        return filepath

    def plot_scatter_with_regression(self, df, x_col, y_col, hue_col, title, xlabel, ylabel, filename):
        """Plots scatter chart with linear trendline."""
        fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
        
        if hue_col and hue_col in df.columns:
            sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue_col, palette='Set2', alpha=0.7, ax=ax)
        else:
            sns.scatterplot(data=df, x=x_col, y=y_col, color='#1f77b4', alpha=0.7, ax=ax)

        sns.regplot(data=df, x=x_col, y=y_col, scatter=False, ax=ax, color='#d62728', line_kws={'linewidth': 2, 'linestyle': '--'})

        ax.set_title(title, pad=15, fontweight='bold')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.tight_layout()

        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, dpi=300)
        plt.close(fig)
        return filepath

    def plot_box_plot(self, df, category_col, value_col, title, xlabel, ylabel, filename):
        """Plots publication box plot for comparing distributions across categories."""
        fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
        sns.boxplot(data=df, x=category_col, y=value_col, hue=category_col, legend=False, palette='Blues_r', ax=ax, width=0.5)

        ax.set_title(title, pad=15, fontweight='bold')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.tight_layout()

        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, dpi=300)
        plt.close(fig)
        return filepath

    def plot_cumulative_return_drawdown(self, df, date_col, return_col, title, filename):
        """Plots cumulative return against maximum drawdown for financial time series."""
        fig, ax1 = plt.subplots(figsize=(10, 5), dpi=300)
        
        # Calculate Cumulative Return
        # Ensure data is sorted by date
        df_sorted = df.sort_values(by=date_col)
        # Convert percent to decimal for cumprod
        rets = df_sorted[return_col].dropna() / 100.0
        cum_ret = (1 + rets).cumprod() - 1
        
        # Calculate Drawdown
        roll_max = (1 + rets).cumprod().cummax()
        drawdown = ((1 + rets).cumprod() - roll_max) / roll_max
        
        # Plot Cumulative Return on left axis
        ax1.plot(df_sorted.loc[rets.index, date_col], cum_ret * 100, color='#2ca02c', linewidth=2, label='Cumulative Return (%)')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Cumulative Return (%)', color='#2ca02c')
        ax1.tick_params(axis='y', labelcolor='#2ca02c')
        
        # Plot Drawdown on right axis
        ax2 = ax1.twinx()
        ax2.fill_between(df_sorted.loc[rets.index, date_col], drawdown * 100, 0, color='#d62728', alpha=0.3, label='Drawdown (%)')
        ax2.set_ylabel('Drawdown (%)', color='#d62728')
        ax2.tick_params(axis='y', labelcolor='#d62728')
        
        # Combine legends
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc='upper left', frameon=True)
        
        plt.title(title, pad=15, fontweight='bold')
        fig.tight_layout()
        
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, dpi=300)
        plt.close(fig)
        return filepath

    def plot_heatmap(self, corr_df, title, filename):
        """Plots correlation heatmap."""
        fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
        sns.heatmap(corr_df, annot=True, fmt=".2f", cmap='Blues', cbar=True, ax=ax, linewidths=0.5)

        ax.set_title(title, pad=15, fontweight='bold')
        fig.tight_layout()

        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, dpi=300)
        plt.close(fig)
        return filepath
