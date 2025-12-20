"""
Visualization and plotting module
"""
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import io
import base64
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

# Set style for matplotlib
plt.style.use('seaborn-v0_8-darkgrid')

class SkinAnalysisVisualizer:
    """Creates visualizations for skin condition tracking"""
    
    def __init__(self, theme: str = "dark"):
        self.theme = theme
        self.set_theme(theme)
    
    def set_theme(self, theme: str):
        """Set color theme for plots"""
        if theme == "dark":
            self.bg_color = "#0e1117"
            self.plot_bg_color = "#1e2128"
            self.grid_color = "#2a2d36"
            self.text_color = "#ffffff"
            self.colors = ['#6366f1', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b', '#ef4444']
        else:
            self.bg_color = "#ffffff"
            self.plot_bg_color = "#f8f9fa"
            self.grid_color = "#e9ecef"
            self.text_color = "#212529"
            self.colors = ['#4c6ef5', '#be4bdb', '#fa5252', '#40c057', '#fd7e14', '#fab005']
    
    def create_severity_timeline(self, timeline_data: List[Dict]) -> go.Figure:
        """Create severity timeline plot"""
        if not timeline_data:
            return self._create_empty_plot("No timeline data available")
        
        # Prepare data
        dates = [datetime.strptime(d['date'], "%Y-%m-%d") for d in timeline_data]
        scores = [d['score'] for d in timeline_data]
        severities = [d['severity'] for d in timeline_data]
        
        # Create color mapping for severities
        severity_colors = {
            "Mild": "#10b981",    # Green
            "Moderate": "#f59e0b", # Yellow
            "Severe": "#ef4444"    # Red
        }
        
        colors = [severity_colors.get(s, "#6366f1") for s in severities]
        
        # Create figure
        fig = go.Figure()
        
        # Add line trace
        fig.add_trace(go.Scatter(
            x=dates,
            y=scores,
            mode='lines+markers',
            name='Severity Score',
            line=dict(color=self.colors[0], width=3),
            marker=dict(
                size=10,
                color=colors,
                line=dict(color='white', width=2)
            ),
            hovertemplate='<b>Date</b>: %{x}<br>' +
                         '<b>Score</b>: %{y:.2f}<br>' +
                         '<b>Severity</b>: %{customdata}<extra></extra>',
            customdata=severities
        ))
        
        # Add severity zones
        fig.add_hrect(y0=0, y1=3, line_width=0, fillcolor="rgba(16, 185, 129, 0.1)", 
                     annotation_text="Mild", annotation_position="top left")
        fig.add_hrect(y0=3, y1=6, line_width=0, fillcolor="rgba(245, 158, 11, 0.1)", 
                     annotation_text="Moderate", annotation_position="top left")
        fig.add_hrect(y0=6, y1=10, line_width=0, fillcolor="rgba(239, 68, 68, 0.1)", 
                     annotation_text="Severe", annotation_position="top left")
        
        # Update layout
        fig.update_layout(
            title=dict(
                text="Severity Progression Timeline",
                font=dict(size=20, color=self.text_color),
                x=0.5
            ),
            xaxis=dict(
                title="Date",
                gridcolor=self.grid_color,
                tickfont=dict(color=self.text_color)
            ),
            yaxis=dict(
                title="Severity Score (0-10)",
                range=[0, 10],
                gridcolor=self.grid_color,
                tickfont=dict(color=self.text_color)
            ),
            plot_bgcolor=self.plot_bg_color,
            paper_bgcolor=self.bg_color,
            font=dict(color=self.text_color),
            hovermode='x unified',
            showlegend=False
        )
        
        return fig
    
    def create_symptom_heatmap(self, symptom_data: Dict, dates: List[str]) -> go.Figure:
        """Create symptom intensity heatmap"""
        if not symptom_data or not dates:
            return self._create_empty_plot("No symptom data available")
        
        # Prepare data for heatmap
        symptoms = list(symptom_data.keys())
        values = np.array([symptom_data[sym] for sym in symptoms])
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=values.reshape(1, -1),
            x=symptoms,
            y=['Intensity'],
            colorscale=['#10b981', '#f59e0b', '#ef4444'],  # Green to red
            zmin=0,
            zmax=10,
            colorbar=dict(
                title="Intensity",
                titleside="right",
                tickfont=dict(color=self.text_color)
            ),
            hovertemplate='<b>Symptom</b>: %{x}<br>' +
                         '<b>Intensity</b>: %{z}/10<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text="Symptom Intensity Analysis",
                font=dict(size=20, color=self.text_color),
                x=0.5
            ),
            xaxis=dict(
                tickfont=dict(color=self.text_color),
                gridcolor=self.grid_color
            ),
            yaxis=dict(
                tickfont=dict(color=self.text_color),
                gridcolor=self.grid_color
            ),
            plot_bgcolor=self.plot_bg_color,
            paper_bgcolor=self.bg_color,
            font=dict(color=self.text_color),
            height=200
        )
        
        return fig
    
    def create_weekly_summary_chart(self, weekly_data: Dict) -> go.Figure:
        """Create weekly summary visualization"""
        if "error" in weekly_data:
            return self._create_empty_plot(weekly_data["error"])
        
        dates = weekly_data.get("dates", [])
        scores = weekly_data.get("scores", [])
        
        if not dates or not scores:
            return self._create_empty_plot("No weekly data available")
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Severity Trend", "Score Distribution", 
                          "Daily Changes", "Progress Overview"),
            specs=[[{"type": "scatter"}, {"type": "box"}],
                   [{"type": "bar"}, {"type": "indicator"}]],
            vertical_spacing=0.15,
            horizontal_spacing=0.15
        )
        
        # 1. Line chart - Severity trend
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=scores,
                mode='lines+markers',
                name='Severity',
                line=dict(color=self.colors[0], width=3),
                marker=dict(size=8, color=self.colors[1]),
                hovertemplate='<b>Date</b>: %{x}<br><b>Score</b>: %{y:.2f}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # 2. Box plot - Score distribution
        fig.add_trace(
            go.Box(
                y=scores,
                name='Distribution',
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8,
                marker=dict(color=self.colors[2]),
                line=dict(color=self.colors[3])
            ),
            row=1, col=2
        )
        
        # 3. Bar chart - Daily changes
        daily_changes = [0] + [scores[i] - scores[i-1] for i in range(1, len(scores))]
        colors_changes = ['#10b981' if x <= 0 else '#ef4444' for x in daily_changes]
        
        fig.add_trace(
            go.Bar(
                x=dates,
                y=daily_changes,
                name='Daily Change',
                marker_color=colors_changes,
                hovertemplate='<b>Date</b>: %{x}<br><b>Change</b>: %{y:+.2f}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # 4. Gauge chart - Progress overview
        delta = weekly_data.get("delta", 0)
        trend = weekly_data.get("trend", "Stable")
        
        fig.add_trace(
            go.Indicator(
                mode="delta",
                value=delta,
                delta={'reference': 0, 'relative': False},
                title={"text": f"Weekly Trend: {trend}"},
                domain={'row': 1, 'column': 1}
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=600,
            plot_bgcolor=self.plot_bg_color,
            paper_bgcolor=self.bg_color,
            font=dict(color=self.text_color),
            showlegend=False,
            title=dict(
                text=f"Weekly Summary - {weekly_data.get('condition', 'Unknown')}",
                font=dict(size=24, color=self.text_color),
                x=0.5
            )
        )
        
        # Update axes
        fig.update_xaxes(gridcolor=self.grid_color, tickfont=dict(color=self.text_color))
        fig.update_yaxes(gridcolor=self.grid_color, tickfont=dict(color=self.text_color))
        
        return fig
    
    def create_medication_timeline(self, timeline_data: List[Dict]) -> go.Figure:
        """Create medication timeline visualization"""
        if not timeline_data:
            return self._create_empty_plot("No medication data available")
        
        # Extract medication data
        dates = []
        medications_list = []
        
        for entry in timeline_data:
            if 'medications' in entry and entry['medications']:
                dates.append(entry['date'])
                medications_list.append(entry['medications'])
        
        if not dates:
            return self._create_empty_plot("No medication history found")
        
        # Create a list of all unique medications
        all_meds = set()
        for meds in medications_list:
            all_meds.update(meds)
        all_meds = sorted(list(all_meds))
        
        # Create binary matrix (date x medication)
        matrix = np.zeros((len(dates), len(all_meds)))
        for i, meds in enumerate(medications_list):
            for j, med in enumerate(all_meds):
                if med in meds:
                    matrix[i][j] = 1
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=matrix.T,
            x=dates,
            y=all_meds,
            colorscale=[[0, self.plot_bg_color], [1, self.colors[0]]],
            showscale=False,
            hovertemplate='<b>Date</b>: %{x}<br>' +
                         '<b>Medication</b>: %{y}<br>' +
                         '<b>Used</b>: %{z}<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text="Medication Usage Timeline",
                font=dict(size=20, color=self.text_color),
                x=0.5
            ),
            xaxis=dict(
                title="Date",
                gridcolor=self.grid_color,
                tickfont=dict(color=self.text_color)
            ),
            yaxis=dict(
                title="Medication",
                gridcolor=self.grid_color,
                tickfont=dict(color=self.text_color)
            ),
            plot_bgcolor=self.plot_bg_color,
            paper_bgcolor=self.bg_color,
            font=dict(color=self.text_color),
            height=300 + len(all_meds) * 20
        )
        
        return fig
    
    def create_dashboard_summary(self, user_data: Dict) -> go.Figure:
        """Create comprehensive dashboard summary"""
        # Create subplots
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=("Overall Severity", "Conditions Overview", "Recent Scores",
                          "Progress Trend", "Symptom Distribution", "Weekly Activity"),
            specs=[[{"type": "indicator"}, {"type": "bar"}, {"type": "scatter"}],
                   [{"type": "scatter"}, {"type": "pie"}, {"type": "heatmap"}]],
            vertical_spacing=0.15,
            horizontal_spacing=0.15
        )
        
        # 1. Overall severity indicator
        avg_score = user_data.get("overall_statistics", {}).get("avg_score", 0)
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=avg_score,
                title={"text": "Average Severity"},
                gauge={
                    'axis': {'range': [0, 10]},
                    'bar': {'color': self._get_severity_color(avg_score)},
                    'steps': [
                        {'range': [0, 3], 'color': 'rgba(16, 185, 129, 0.2)'},
                        {'range': [3, 6], 'color': 'rgba(245, 158, 11, 0.2)'},
                        {'range': [6, 10], 'color': 'rgba(239, 68, 68, 0.2)'}
                    ]
                }
            ),
            row=1, col=1
        )
        
        # 2. Conditions bar chart
        conditions = list(user_data.get("conditions", {}).keys())
        condition_scores = []
        for cond in conditions:
            stats = user_data["conditions"][cond].get("statistics", {})
            condition_scores.append(stats.get("latest_score", 0))
        
        if conditions:
            fig.add_trace(
                go.Bar(
                    x=conditions,
                    y=condition_scores,
                    marker_color=[self._get_severity_color(s) for s in condition_scores],
                    hovertemplate='<b>Condition</b>: %{x}<br><b>Score</b>: %{y:.2f}<extra></extra>'
                ),
                row=1, col=2
            )
        
        # Update layout
        fig.update_layout(
            height=700,
            plot_bgcolor=self.plot_bg_color,
            paper_bgcolor=self.bg_color,
            font=dict(color=self.text_color),
            showlegend=False,
            title=dict(
                text="Skin Health Dashboard",
                font=dict(size=24, color=self.text_color),
                x=0.5
            )
        )
        
        # Update axes
        fig.update_xaxes(gridcolor=self.grid_color, tickfont=dict(color=self.text_color))
        fig.update_yaxes(gridcolor=self.grid_color, tickfont=dict(color=self.text_color))
        
        return fig
    
    def _get_severity_color(self, score: float) -> str:
        """Get color based on severity score"""
        if score <= 3:
            return "#10b981"  # Green
        elif score <= 6:
            return "#f59e0b"  # Yellow
        else:
            return "#ef4444"  # Red
    
    def _create_empty_plot(self, message: str) -> go.Figure:
        """Create an empty plot with a message"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color=self.text_color)
        )
        fig.update_layout(
            plot_bgcolor=self.plot_bg_color,
            paper_bgcolor=self.bg_color,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=300
        )
        return fig
    
    def plot_to_base64(self, fig: go.Figure) -> str:
        """Convert plotly figure to base64 string"""
        try:
            img_bytes = fig.to_image(format="png", width=800, height=400)
            b64_string = base64.b64encode(img_bytes).decode()
            return f"data:image/png;base64,{b64_string}"
        except:
            return ""