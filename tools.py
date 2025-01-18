from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import pandas as pd
import io


class Reader_Tool(BaseTool):
    def Input_param():
        class MyToolInput(BaseModel):
            """Input scheme - file_path"""
            file_path: str = Field(...,description='singel file_path of the excel/csv file')
        return MyToolInput

    name:str = "DatasetReader"
    description:str = "Reads an excel/csv file [can process one file at one time, if multiple files then call individually] from the given file_path and returns information about the dataset -> null-values, description, first 5-10 rows, info, column types etc. "
    args_schema: Type[BaseModel] = Input_param()
    def _run(self, file_path:str) -> str :
        def get_describe(file_path:str,dataframe:pd.DataFrame):
            return f"Description of the Dataframe - {file_path} :- ```{dataframe.describe()}```\n"
        
        def get_info(file_path: str, dataframe: pd.DataFrame):
            buffer = io.StringIO()
            dataframe.info(buf=buffer)
            info_str = buffer.getvalue()
            buffer.close()
            return f"Information of the Dataframe - {file_path} :- ```{info_str}```\n"

        def get_null(file_path: str, dataframe: pd.DataFrame):
            total_missing = dataframe.isnull().sum().sum()
            missing_by_column = dataframe.isnull().sum().to_dict()
            missing_percentage = (dataframe.isnull().sum() / len(dataframe) * 100).to_dict()

            return (
                f"Null values of the Dataframe - ```{file_path} :-\n"
                f"Total Missing: {total_missing}\n"
                f"Missing by Column: {missing_by_column}\n"
                f"Missing Percentage: {missing_percentage}```\n"
            )

        def get_head(file_path:str,dataframe:pd.DataFrame):
            return f"Head of the Dataframe - {file_path} :- ```{dataframe.head(5)}```\n" 
        
        # file_path = file_path[0]
        print(file_path)
        df = pd.read_excel(file_path)
        return f"""After reading the file {file_path}:\n \
            {get_describe(file_path=file_path,dataframe=df)} \
            {get_info(file_path=file_path,dataframe=df)} \
            {get_null(file_path=file_path,dataframe=df)}\
            {get_head(file_path=file_path,dataframe=df)}
            """

    
    