import pandas as pd
from atlassian import Confluence

def read_excel_as_html(file_path):
    try:
        df = pd.read_excel(file_path)
        html_data = df.to_html()
        return html_data
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return None

def update_confluence_page(confluence, page_id, html_data):
    try:
        confluence.update_page(
            page_id=page_id,
            title="Updated Page",
            body=html_data,
        )
        print("Successfully updated the Confluence page.")
    except Exception as e:
        print(f"An error occurred while updating the Confluence page: {e}")

def main():
    # Define the path to your Excel file
    file_path = "<YOUR_EXCEL_FILE_PATH>"
    html_data = read_excel_as_html(file_path)

    if html_data is not None:
        # Initialize the Confluence instance
        confluence = Confluence(
            url="<YOUR_CONFLUENCE_URL>",
            username="<YOUR_USERNAME>",
            token="<YOUR_API_TOKEN>",
        )

        # Define the page ID of the Confluence page you want to update
        page_id = "<YOUR_PAGE_ID>"

        # Update the Confluence page with the HTML data
        update_confluence_page(confluence, page_id, html_data)

if __name__ == "__main__":
    main()
