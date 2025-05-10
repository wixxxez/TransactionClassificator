from datetime import datetime
from .TransactionReport import OverallTransactionReport, Dataset
from src.utils.GCSFileManager import save_html_to_gcs

import pandas as pd
import plotly.express as px


class BuildHTMLReport():

    def __init__(self, config):
        self.dataset = Dataset(config)  
        self.transaction_serivce = OverallTransactionReport(self.dataset.create_dataset(), self.dataset.get_balances())
        self.tr_report =  self.transaction_serivce.get_transaction_report() 

    def build_transactions_details(self,tr_report ):
        
        today = datetime.today()
        current_week = today.isocalendar()[1]
        cat_dict = {}
        dataset = self.dataset.create_dataset()
        for category in tr_report.category.unique():

            cat_dict[category]= dataset.query("custom_category == @category and week_number == @current_week").reset_index(drop=True)    

        return cat_dict

    def build_report(self):
    
    
        tr_report = self.tr_report
        # Sample DataFrame (Main Summary)
        df_summary = tr_report.groupby('category').amount.sum().reset_index()

        # Sample Detailed Data for Each Category
        df_details = self.build_transactions_details(df_summary)

        # Create Plotly figure
        fig = px.bar(tr_report, x="category", y="amount", title="Chart of budget usage per user", color='user_name')

        # Convert Plotly figure to HTML div
        plot_html = fig.to_html(full_html=False, include_plotlyjs="cdn")

        _, weekly_limits = self.transaction_serivce.get_Weekly_balance_report(markdown=False)
        _, month_limits  = self.transaction_serivce.get_month_balance_report(markdown=False)
        # Generate collapsible table rows with nested tables
        table_html =f"""
        <table class="table table-striped table-hover">
            <thead class="table-dark">
                <tr>
                    
                    <th>Category</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>

        """
        custom_styles = '\n     .custom-collapse {\n            transition: height 0.5s ease-out, opacity 0.5s ease-out;\n            overflow: hidden;\n            opacity: 0;\n        }\n        \n        .custom-collapse.show {\n            opacity: 1;\n        }\n'

        for index, row in df_summary.iterrows():
            category_id = f"collapse{index}"
            
            # Generate nested table for detailed data
            details_html = "<table class='table table-bordered'><thead><tr><th>Username</th><th>Date</th><th>Description</th><th>Amount</th></tr></thead><tbody>"
            for _, detail_row in df_details[row['category']].iterrows():
                details_html += f"<tr><td>{detail_row['user_name']}</td><td>{detail_row['full_date'].split(" ")[0]}</td><td>{detail_row['description']}</td><td>{detail_row['amount']}</td></tr>"
            details_html += f"</tbody></table>"

            table_html += f"""
                <!-- Main Row -->
                <tr data-bs-toggle="collapse" data-bs-target="#{category_id}" style="cursor: pointer;">
                    <td><strong>{row['category']}</strong></td>
                    <td>{row['amount']}</td>
                </tr>
                <!-- Collapsible Row with Nested Table -->
                <tr>
                    <td colspan="2">
                        <div id="{category_id}" class="collapse custom-collapse">
                            <div class="p-3 border rounded bg-light">
                                {details_html}

                                
                            </div>
                        </div>
                    </td>
                </tr>
                
            """

        table_html += "</tbody></table>"

        # Define HTML report with Bootstrap collapsible rows and smooth transitions
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Data Report</title>
            <link rel="stylesheet" 
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
            
            <style>
                /* Smooth Collapse Transition */
                .custom-collapse {
                custom_styles
                }
            </style>
        </head>
        <body class="bg-light">
            <div class="container mt-4">
                <h1 class="text-center text-primary">Weekly report</h1>
                
                <div class="card shadow-sm p-4 mt-4">
                    <h2 class="text-secondary">Transaction details</h2>
                    {table_html}
                </div>
                <div class="card shadow-sm p-4 mt-4">
                    <h2 class="text-secondary">Budget limits</h2>
                        <h4 class="text-secondary">Weekly limits</h4>
                            {''.join(weekly_limits)}
                            <h4 class="text-secondary">Monthly limits</h4>
                            {''.join(month_limits)}
                </div>  
                
                <div class="card shadow-sm p-4 mt-4">
                    <h2 class="text-secondary">Overall budget usage</h2>
                    {plot_html}
                </div>
                
                </div>
            
            </div>
        </body>
        </html>
        """

        # Save the report as an HTML file
        # with open("index.html", "w", encoding="utf-8") as f:
        #     f.write(html_template)

        save_html_to_gcs(html_template, 'home_bot_web_serivce/index.html')

