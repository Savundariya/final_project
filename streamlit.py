import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import re
import openai

# ---------- PDF Extraction ----------
def extract_pdf_text(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# ---------- Transaction Parser ----------
def parse_multiline_transactions(text):
    lines = text.split('\n')
    data = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if re.match(r'\d{2}/\d{2}/\d{4}', line):
            date = line
            desc_lines = []
            i += 1
            while i < len(lines) and not re.match(r'^\d{1,3}(,\d{3})*(\.\d{2})?$', lines[i].strip()):
                if lines[i].strip():
                    desc_lines.append(lines[i].strip())
                i += 1
            if i < len(lines):
                amount_line = lines[i].strip()
                try:
                    amount = float(amount_line.replace(",", ""))
                except:
                    amount = 0.0
                i += 3
                description = " ".join(desc_lines)
                data.append([date, amount, description])
        else:
            i += 1

    return pd.DataFrame(data, columns=["Date", "Amount", "Description"])

# ---------- Categorizer ----------
def categorize(description):
    desc = description.lower()
    if any(x in desc for x in ["swiggy", "zomato", "blinkit", "zepto"]):
        return "Food Delivery"
    elif any(x in desc for x in ["redbus", "uber", "ola"]):
        return "Travel"
    elif "jio" in desc or "recharge" in desc:
        return "Recharge"
    elif "insurance" in desc:
        return "Insurance"
    elif "amazon" in desc:
        return "Shopping"
    elif "life science" in desc:
        return "Healthcare"
    elif "grand fresh" in desc or "bigbasket" in desc:
        return "Groceries"
    elif "maintenance" in desc:
        return "Utilities"
    else:
        return "Others"

# ---------- Streamlit Interface ----------
st.title("📊 UPI Usage & Financial Analyzer (LLM Powered)")

uploaded_file = st.file_uploader("Upload your UPI PDF Statement", type="pdf")

if uploaded_file:
    with st.spinner("Extracting data..."):
        raw_text = extract_pdf_text(uploaded_file)
        df = parse_multiline_transactions(raw_text)
        df["Category"] = df["Description"].apply(categorize)
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
        df["Month"] = df["Date"].dt.strftime("%b-%Y")

        monthly_spending = df.groupby("Month")["Amount"].sum()
        category_spending = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

    st.success("Transactions parsed and categorized!")

    st.subheader("📄 Parsed Transactions")
    st.dataframe(df)

    st.subheader("📅 Monthly Spending")
    st.bar_chart(monthly_spending)

    st.subheader("🏷️ Category-wise Spending")
    st.bar_chart(category_spending)

    # ---------- LLM Prompt ----------
    monthly_spending_str = "\n".join(
        [f"{month}    ₹{amount:,.2f}" for month, amount in monthly_spending.items()]
    )
    category_spending_str = "\n".join(
        [f"{category}: ₹{amount:,.2f}" for category, amount in category_spending.items()]
    )

    prompt = f"""
    You are a financial advisor. Based on the following monthly and category-wise spending in Indian Rupees (₹), provide 3 personalized financial tips.

    Monthly Spend:
    {monthly_spending_str}

    Category-wise Spend:
    {category_spending_str}
    """

    st.subheader("💡 Personalized Financial Advice")

    if st.button("Generate Advice with LLM"):
        with st.spinner("Consulting financial advisor (LLM)..."):
            client = openai.OpenAI(
                api_key="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",  # 🔁 Replace with your key
                base_url="https://openrouter.ai/api/v1"
            )

            try:
                response = client.chat.completions.create(
                    model="openrouter/auto",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error("Failed to get advice from LLM.")
                st.exception(e)
