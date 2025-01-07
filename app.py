import streamlit as st
import cohere
import yfinance as yf

# Initialize Cohere Client
cohere_api_key = st.secrets["LLAMA-API"]
co = cohere.Client(cohere_api_key)

# Streamlit App
def main():
    st.title("CFA Research Challenge Report Assistant")
    st.write("This app generates a comprehensive CFA Research Challenge report for a company based on live data from Yahoo Finance.")

    # Input Section
    st.subheader("Input Company Details")
    company_ticker = st.text_input("Enter the Company Ticker Symbol:")

    # Generate Report Button
    if st.button("Generate Report"):
        if company_ticker:
            try:
                # Fetch data from yfinance
                company_data = yf.Ticker(company_ticker)
                financials = company_data.financials
                balance_sheet = company_data.balance_sheet
                cashflow = company_data.cashflow
                recommendations = company_data.recommendations

                # Generate the report
                report = generate_report(company_ticker, financials, balance_sheet, cashflow, recommendations)
                st.subheader("Generated Report")
                st.write(report)
            except Exception as e:
                st.error(f"Error fetching data for {company_ticker}: {e}")
        else:
            st.error("Please enter a valid company ticker to generate the report.")

# Function to generate the report using Cohere
def generate_report(ticker, financials, balance_sheet, cashflow, recommendations):
    prompt = (
        f"Write a comprehensive CFA Research Challenge report for {ticker}. "
        f"The report should include an analysis of the financials, balance sheet, cash flow, and generate an analyst recommendation based on this data. "
        f"Here are the key details:\n"
        f"Financials:\n{financials.to_string()}\n"
        f"Balance Sheet:\n{balance_sheet.to_string()}\n"
        f"Cash Flow:\n{cashflow.to_string()}\n"
    )
    
    try:
        # Requesting response from Cohere API
        response = co.generate(
            model='command-light',  # Adjust the model name if necessary
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        return response.generations[0].text  # Return the generated text
    except Exception as e:
        return f"Error generating report: {e}"

if __name__ == "__main__":
    main()
