from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Union, Any
from datetime import datetime

class DataAnalysisResult(BaseModel):
    """Output model for the Data Reader task"""
    file_name: str = Field(..., description="Name of the analyzed file")
    file_path: str = Field(..., description="Full path to the analyzed file")
    column_count: int = Field(..., description="Number of columns in the dataset")
    row_count: int = Field(..., description="Number of rows in the dataset")
    columns: Dict[str, str] = Field(..., description="Dictionary mapping column names to their data types")
    null_values: Dict[str, int] = Field(..., description="Dictionary mapping column names to their null value counts")
    null_percentage: Dict[str, float] = Field(..., description="Dictionary mapping column names to their null value percentages")
    description: Dict[str, Dict[str, float]] = Field(..., description="Statistical description of numerical columns")
    sample_data: List[Dict[str, Any]] = Field(..., description="Sample rows from the dataset")
    
    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "file_name": "sales_data.csv",
                "file_path": "u1314-14afsl141-smasdads/sales_data.csv",
                "column_count": 10,
                "row_count": 1000,
                "columns": {"product_id": "int64", "price": "float64", "category": "object"},
                "null_values": {"product_id": 0, "price": 5, "category": 2},
                "null_percentage": {"product_id": 0.0, "price": 0.5, "category": 0.2},
                "description": {"price": {"mean": 45.5, "std": 12.3, "min": 10.0, "max": 100.0}},
                "sample_data": [{"product_id": 1, "price": 45.5, "category": "electronics"}]
            }
        }

class PreprocessingCode(BaseModel):
    """Output model for the Preprocessing Code Writer task"""
    code: str = Field(..., description="Python code for preprocessing the datasets")
    execution_result: Optional[str] = Field(None, description="Result of code execution")
    processed_files: List[str] = Field(..., description="List of files that were processed")
    output_files: List[str] = Field(..., description="List of output files that were created")
    operations_performed: Dict[str, List[str]] = Field(..., description="Dictionary mapping column names to preprocessing operations performed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "import pandas as pd\ndf = pd.read_csv('data.csv')\n...",
                "execution_result": "Execution completed successfully",
                "processed_files": ["u1314-14afsl141-smasdads/sales_data.csv"],
                "output_files": ["u1314-14afsl141-smasdads/updated_sales_data.csv"],
                "operations_performed": {
                    "price": ["filled_nulls_with_mean", "removed_outliers"],
                    "category": ["filled_nulls_with_mode"]
                }
            }
        }

class PlotSuggestion(BaseModel):
    """Model for an individual plot suggestion"""
    plot_number: int = Field(..., description="Sequence number of the plot suggestion")
    plot_type: str = Field(..., description="Type of plot (e.g., scatter, histogram, bar)")
    title: str = Field(..., description="Suggested title for the plot")
    x_axis: str = Field(..., description="Column name for x-axis")
    y_axis: Optional[str] = Field(None, description="Column name for y-axis (if applicable)")
    group_by: Optional[str] = Field(None, description="Column name to group by (if applicable)")
    insights: str = Field(..., description="Expected insights that can be gained from this plot")
    
    class Config:
        json_schema_extra = {
            "example": {
                "plot_number": 1,
                "plot_type": "scatter",
                "title": "Price vs Sales Volume",
                "x_axis": "price",
                "y_axis": "sales_volume",
                "group_by": "category",
                "insights": "Relationship between price and sales volume across different product categories"
            }
        }

class PlotSuggestions(BaseModel):
    """Output model for the Plot Suggestion task"""
    dataset_name: str = Field(..., description="Name of the dataset")
    suggestions: List[PlotSuggestion] = Field(..., description="List of plot suggestions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "dataset_name": "updated_sales_data.csv",
                "suggestions": [
                    {
                        "plot_number": 1,
                        "plot_type": "scatter",
                        "title": "Price vs Sales Volume",
                        "x_axis": "price",
                        "y_axis": "sales_volume",
                        "group_by": "category",
                        "insights": "Relationship between price and sales volume across different product categories"
                    }
                ]
            }
        }

class DatasetPlotSuggestions(BaseModel):
    """Output model for all plot suggestions across datasets"""
    suggestions_by_dataset: List[PlotSuggestions] = Field(..., description="Plot suggestions organized by dataset")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp when suggestions were generated")
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v):
        if v is None:
            return datetime.now()
        return v

class CriticFeedback(BaseModel):
    """Model for feedback on an individual plot suggestion"""
    original_plot_number: int = Field(..., description="Original sequence number of the plot suggestion")
    is_recommended: bool = Field(..., description="Whether the critic recommends this plot")
    feedback: str = Field(..., description="Critique and feedback on the plot suggestion")
    improvements: Optional[Dict[str, str]] = Field(None, description="Suggested improvements to the plot")
    alternative_plot: Optional[PlotSuggestion] = Field(None, description="Alternative plot suggestion if original is not recommended")
    
    class Config:
        json_schema_extra = {
            "example": {
                "original_plot_number": 1,
                "is_recommended": True,
                "feedback": "Good suggestion but consider using a logarithmic scale for price",
                "improvements": {
                    "scale": "Use logarithmic scale for price axis",
                    "title": "Suggest 'Log Price vs Sales Volume' for clarity"
                },
                "alternative_plot": None
            }
        }

class PlotSuggestionCritique(BaseModel):
    """Output model for critique of plot suggestions for a dataset"""
    dataset_name: str = Field(..., description="Name of the dataset")
    original_suggestions_count: int = Field(..., description="Number of original plot suggestions")
    feedback: List[CriticFeedback] = Field(..., description="Feedback on each plot suggestion")
    recommended_plots: List[PlotSuggestion] = Field(..., description="Final list of recommended plots after critique")
    
    class Config:
        json_schema_extra = {
            "example": {
                "dataset_name": "updated_sales_data.csv",
                "original_suggestions_count": 3,
                "feedback": [
                    {
                        "original_plot_number": 1,
                        "is_recommended": True,
                        "feedback": "Good suggestion but consider using a logarithmic scale for price",
                        "improvements": {
                            "scale": "Use logarithmic scale for price axis"
                        },
                        "alternative_plot": None
                    }
                ],
                "recommended_plots": [
                    {
                        "plot_number": 1,
                        "plot_type": "scatter",
                        "title": "Log Price vs Sales Volume",
                        "x_axis": "price",
                        "y_axis": "sales_volume",
                        "group_by": "category",
                        "insights": "Relationship between price and sales volume across different product categories"
                    }
                ]
            }
        }

class DatasetCritiques(BaseModel):
    """Output model for the Plot Suggestion Critic task"""
    critiques_by_dataset: List[PlotSuggestionCritique] = Field(..., description="Critiques organized by dataset")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp when critique was generated")

class GeneratedPlot(BaseModel):
    """Model for an individual generated plot"""
    plot_number: int = Field(..., description="Sequence number of the plot")
    plot_type: str = Field(..., description="Type of plot (e.g., scatter, histogram, bar)")
    title: str = Field(..., description="Title of the plot")
    file_name: str = Field(..., description="Name of the file where the plot was saved")
    file_path: str = Field(..., description="Full path to the saved plot file")
    dataset_source: str = Field(..., description="Source dataset used for the plot")
    columns_used: List[str] = Field(..., description="List of columns used in the plot")
    
class PlotGenerationResult(BaseModel):
    """Output model for the Plot Generator task"""
    code: str = Field(..., description="Python code that generated the plots")
    plots_generated: List[GeneratedPlot] = Field(..., description="List of generated plots")
    execution_result: Optional[str] = Field(None, description="Result of code execution")
    success_count: int = Field(..., description="Number of successfully generated plots")
    error_count: int = Field(0, description="Number of plots that failed to generate")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp when plots were generated")
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v):
        if v is None:
            return datetime.now()
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "import pandas as pd\nimport matplotlib.pyplot as plt\n...",
                "plots_generated": [
                    {
                        "plot_number": 1,
                        "plot_type": "scatter",
                        "title": "Log Price vs Sales Volume",
                        "file_name": "price_vs_sales_scatter.png",
                        "file_path": "u1314-14afsl141-smasdads/price_vs_sales_scatter.png",
                        "dataset_source": "updated_sales_data.csv",
                        "columns_used": ["price", "sales_volume", "category"]
                    }
                ],
                "execution_result": "All plots generated successfully",
                "success_count": 1,
                "error_count": 0,
                "timestamp": "2023-06-15T14:30:00"
            }
        }

class PlotAnalysis(BaseModel):
    """Model for analysis of an individual plot"""
    plot_type: str = Field(..., description="Type of plot identified")
    variables_visualized: List[str] = Field(..., description="List of variables/columns visualized in the plot")
    key_patterns: List[str] = Field(..., description="Key patterns or trends identified in the plot")
    notable_outliers: Optional[List[str]] = Field(None, description="Notable outliers or interesting data points")
    relation_to_dataset: str = Field(..., description="How this visualization relates to the dataset context")
    business_implications: List[str] = Field(..., description="Business implications or actionable insights from this plot")


class VisualizationReport(BaseModel):
    """Output model for the Visualization Report task"""
    plots_analyzed: List[PlotAnalysis] = Field(..., description="Analysis of individual plots")
    dataset_context: Dict[str, Any] = Field(..., description="Context information about the datasets")
    overall_insights: List[str] = Field(..., description="Overall insights from all visualizations")
    recommendations: List[str] = Field(..., description="Actionable recommendations based on visualizations")
    
    
# Factory function to create the appropriate output model based on task name
def create_output_model(task_name: str, output_data: Dict[str, Any]):
    """
    Creates the appropriate Pydantic model instance based on the task name
    
    Args:
        task_name: Name of the task
        output_data: Dictionary with the output data
        
    Returns:
        Instance of the appropriate Pydantic model
    """
    task_to_model = {
        "Data Reader": DataAnalysisResult,
        "Preprocessing code writter": PreprocessingCode,
        "Plot Suggestion Task": DatasetPlotSuggestions,
        "Plot Suggestor Critic Task": DatasetCritiques,
        "Plot Generator Task": PlotGenerationResult,
        "Visualization Report Task": VisualizationReport
    }
    
    if task_name not in task_to_model:
        raise ValueError(f"Unknown task name: {task_name}")
    
    model_class = task_to_model[task_name]
    return model_class(**output_data)