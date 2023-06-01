import dataprep
import pandas as pd
from pandasai.llm.openai import OpenAI
from pandasai import PandasAI
import sweetviz as sv
import openai
from autoviz import AutoViz_Class
from dataprep.eda import create_report
openai.api_key = "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"
def Dataprepared(df1):
    report  = create_report(df1)
    report.save("UberRidesReportDataprep")
def SweeterViz(df1):
    report = sv.analyze(df1)
    report.show_html("Report.html")
def AutomaticViz():
    AV = AutoViz_Class()
    dft = AV.AutoViz("uber-rides-dataset.csv",",","",None,0,0,False,"svg",150000,30)
def main():
    theInput = input("Dataprep, Sweetviz, Autoviz, or PandasProfiling \n")
    df1 = pd.read_csv("uber-rides-dataset.csv")
    if theInput.lower() == "dataprep":
        Dataprepared(df1)
    elif theInput.lower() == "sweetviz":
        SweeterViz(df1)
    elif theInput.lower() == "autoviz":
        AutomaticViz()
    elif theInput.lower() == "pandasprofiling":
        PolarProfiling()
main()