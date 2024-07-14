import matplotlib.pyplot as plt
import io
import base64
import numpy as np

def create_donut_chart(grouped_counts):
    color_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    status_color_map = dict(zip(grouped_counts.index, color_list))

    fig, ax = plt.subplots(figsize=(4, 3))
    wedges, texts, autotexts = ax.pie(grouped_counts.values, labels=grouped_counts.index,
                                      autopct=lambda pct: f'{int(round(pct / 100 * sum(grouped_counts.values)))}',
                                      startangle=120, colors=[status_color_map.get(status, 'gray') for status in grouped_counts.index],
                                      wedgeprops={'edgecolor': 'white'})
    ax.axis('equal')
    centre_circle = plt.Circle((0, 0), 0.70, color='white')
    ax.add_artist(centre_circle)

    plt.setp(texts, size=10)
    plt.setp(autotexts, size=10)

    fig.subplots_adjust(top=0.85)
    ax.set_title('Number of Decisions', fontsize=16, weight='bold', pad=20)
    ax.legend(fontsize=10, loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=1)

    donut_buf = io.BytesIO()
    plt.savefig(donut_buf, format='png', bbox_inches='tight')
    donut_buf.seek(0)
    donut_chart = base64.b64encode(donut_buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return donut_chart

def create_bar_chart(df, st, op, grouped_counts):
    color_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    status_color_map = dict(zip(grouped_counts.index, color_list))

    top_areas = df[op].value_counts().head(5).index.tolist()
    nested_dict = {area: df[df[op] == area][st].value_counts().to_dict() for area in top_areas}

    therapeutic_areas_sorted = sorted(top_areas, key=lambda area: sum(nested_dict[area].values()), reverse=False)

    fig, ax = plt.subplots(figsize=(4, 3))
    bar_width = 0.25
    bar_positions = np.arange(len(therapeutic_areas_sorted))

    for i, status in enumerate(grouped_counts.index):
        counts_sorted = [nested_dict[area].get(status, 0) for area in therapeutic_areas_sorted]
        bars = ax.barh(bar_positions - bar_width / 2 + i * bar_width, counts_sorted, height=bar_width, label=status, color=status_color_map.get(status, 'gray'))
        for bar, value in zip(bars, counts_sorted):
            ax.annotate(f'{value}', xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2), 
                        xytext=(5, 0), textcoords='offset points',
                        ha='left', va='center', fontsize=10)

    ax.set_yticks(bar_positions)
    ax.set_yticklabels(therapeutic_areas_sorted, fontsize=10)
    ax.legend(fontsize=10, loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=1)
    ax.tick_params(axis='x', which='major', labelsize=10, length=3)
    ax.set_xlabel('Count', fontsize=10)

    fig.subplots_adjust(top=0.9)
    ax.set_title("Top 5 "+op+" by Status", fontsize=16, weight='bold', pad=20, loc="left")
    ax.set_aspect('auto')

    bar_buf = io.BytesIO()
    plt.savefig(bar_buf, format='png', bbox_inches='tight')
    bar_buf.seek(0)
    bar_chart = base64.b64encode(bar_buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return bar_chart
