import streamlit as st
import cohere
import yfinance as yf

# Initialize Cohere Client
cohere_api_key = st.secrets["LLAMA-API"]
co = cohere.Client(cohere_api_key)

# Streamlit App
def main():
    st.title("CFA Research Challenge Report Assistant")
    st.write("This app generates a detailed CFA Research Challenge report for a company based on live data from Yahoo Finance.")

    # Input Section
    st.subheader("Input Company Details")
    company_ticker = st.text_input("Enter the Company Ticker Symbol:")

    # Dropdown for selecting sections to include in the report
    sections = st.multiselect(
        "Select the sections to include in the report:",
        options=["Financials", "Balance Sheet", "Cash Flow", "Analyst Recommendations"]
    )

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

                # Generate report based on selected sections
                report = generate_report(company_ticker, sections, financials, balance_sheet, cashflow, recommendations)
                st.subheader("Generated Report")
                st.write(report)
            except Exception as e:
                st.error(f"Error fetching data for {company_ticker}: {e}")
        else:
            st.error("Please enter a valid company ticker to generate the report.")

# Function to generate the report using Cohere
def generate_report(ticker, sections, financials, balance_sheet, cashflow, recommendations):
    final_report = []

    # Add financials if selected
    if "Financials" in sections:
        financial_report = generate_section_report(ticker, "Financials", financials)
        final_report.append(financial_report)

    # Add balance sheet if selected
    if "Balance Sheet" in sections:
        balance_sheet_report = generate_section_report(ticker, "Balance Sheet", balance_sheet)
        final_report.append(balance_sheet_report)

    # Add cash flow if selected
    if "Cash Flow" in sections:
        cashflow_report = generate_section_report(ticker, "Cash Flow", cashflow)
        final_report.append(cashflow_report)

    # Add analyst recommendations if selected
    if "Analyst Recommendations" in sections:
        recommendations_report = generate_section_report(ticker, "Analyst Recommendations", recommendations)
        final_report.append(recommendations_report)

    return "\n\n".join(final_report)

# Function to generate a section report using Cohere
def generate_section_report(ticker, section, data):
    prompt = (
        f"You're an analyst at BlackRock. Write a detailed CFA Research Challenge section report for {ticker}. "
        f"Section: {section}\n"
        f"Include an analysis of the key metrics in the following data:\n"
        f"{data}\n"
        f"Go into very great detail, mention numbers, data, calculate key ratios, and ensure that the reader has a clear view of what's going on, and the reader here is a CFA Charterholder.\n"
        f"Make it hella long and detailed."
    )
    
    try:
        # Requesting response from Cohere API
        response = co.generate(
            model='command-light',  # Adjust the model name if necessary
            prompt=prompt,
            max_tokens=1000,  # Increase token limit if you need longer responses
            temperature=0.7
        )
        return f"**{section}**\n\n{response.generations[0].text}"  # Return the section report
    except Exception as e:
        return f"Error generating {section} report: {e}"

if __name__ == "__main__":
    main()
